# Architecture

## System overview

```
                    ┌──────────────────────────┐
                    │        Slack App          │
                    │  (Bolt, Socket Mode)      │
                    │  @mentions / slash cmd /  │
                    │  home tab / proactive     │
                    └────────────┬───────────────┘
                                 │ HTTPS (BACKEND_URL)
┌──────────────┐                │
│   Frontend    │  HTTPS         │
│  Next.js 15   ├────────────────┤
│  (dashboard,  │                │
│  graphs, chat)│         ┌──────▼───────────────────────────┐
└──────────────┘          │           FastAPI Backend         │
                           │  routers -> services -> data_loader│
                           │                                    │
                           │  services/                         │
                           │   graph_service   (networkx)       │
                           │   rag_service      (retrieval +    │
                           │                     optional Claude)│
                           │   risk_engine       (heuristic)     │
                           └───────────────┬────────────────────┘
                                            │
                          ┌─────────────────┴─────────────────┐
                          │        mcp_connectors/              │
                          │  base.py (mock/live interface)      │
                          │  github, jira, notion, confluence,  │
                          │  gdrive, slack, calendar, linear,   │
                          │  figma, gitlab, azure_devops        │
                          └─────────────────┬─────────────────┘
                                            │ mock: JSON fixtures
                                            │ live: real MCP servers
                                  data/fixtures/*.json
```

## Why a single `DataStore` facade

`backend/app/services/data_loader.py` is the only place that reads the JSON
fixtures. Every router and service goes through `store.<collection>` rather
than touching files directly. That means the production migration is:

1. Point `DataStore` at Neo4j for graph-shaped data (teams, people, decisions,
   dependency edges) using the driver in `NEO4J_URI` / `NEO4J_USER` /
   `NEO4J_PASSWORD` (already read into `Settings`, just unused by the mock
   store).
2. Point `DataStore` at PostgreSQL for relational data (tickets, releases,
   audit history) via `DATABASE_URL`.
3. Nothing in `app/routers/*` or `app/services/graph_service.py` needs to
   change, because they only ever called `store.teams`, `store.decisions`,
   etc.

## Dependency graph reasoning

`graph_service.py` builds a `networkx.DiGraph` from `dependency_graph.json`
and answers three question shapes without any text matching:

- **"What is blocking what?"** - `find_blocker_chains()` walks only the
  `blocks` edges and returns every root-to-leaf chain.
- **"What breaks if X breaks?"** - `downstream_impact(node_id)` uses
  `nx.descendants`.
- **"What does X depend on?"** - `upstream_dependencies(node_id)` uses
  `nx.ancestors`.

`risk_score_for_node` is a transparent heuristic (status weight + downstream
fan-out). `docs/API.md` documents the exact formula. In production this is
the natural place to plug in a model trained on historical release/ticket
outcomes - the interface (`node_id -> int`) would not need to change.

## Organizational memory / RAG

`rag_service.py` implements retrieval today as hybrid lexical scoring across
decisions, docs, conversations, and PRs, plus a graph-grounding step that
detects "why/blocked/risk" style questions and attaches the current critical
blocker chain as evidence. This keeps the demo deterministic and citation-safe
with zero external calls.

If `ANTHROPIC_API_KEY` is set, the intended production extension (see the
`ANTHROPIC_API_KEY` check already threaded through `rag_service.py`) is to
pass the same retrieved evidence set to Claude with a strict "only use the
provided evidence, cite every claim" system prompt, and use the model's
output as `answer` while keeping the same `citations` list. This preserves
the "never hallucinate" guarantee: the model only sees pre-retrieved,
graph-grounded evidence, never open-ended generation.

For a production-grade retrieval layer, replace the lexical scorer with:
- Embeddings (e.g. an Anthropic-compatible or OpenAI embedding model) stored
  in pgvector or Qdrant.
- A GraphRAG-style step that expands the seed set of matched nodes by
  walking 1-2 hops in the knowledge graph before ranking.

## MCP connector layer

Every source system implements `mcp_connectors/base.py::BaseConnector`.
`mode` is computed from `MCP_MODE` and whether an `env_url_var` is set, so
connectors can be flipped to live independently - a team on GitHub can go
live while Notion stays mocked. `connect()` includes the exact MCP client
code (commented) needed to open a real session via `mcp.client.sse` once a
server URL is available.

## Predictive risk engine

`risk_engine.py::release_delay_probability` combines a release's declared
status with the current critical dependency chain's risk score. This is
intentionally simple and auditable for a hackathon judge to inspect; the
natural production upgrade is a gradient-boosted model trained on
`(release features, historical outcome)` pairs, with the current heuristic
kept as a fallback/cold-start estimator.

## Auth

JWT issuing (`core/security.py`) is fully functional. The Slack OAuth
callback (`routers/auth.py`) is a stub - it validates that `SLACK_CLIENT_ID`
is configured and returns a demo JWT; production wiring is a single
`httpx.post` to `https://slack.com/api/oauth.v2.access` documented inline in
that file.

## Frontend data flow

Every page is a React Server Component that calls `src/lib/api.ts`, which
tries the live backend and falls back to bundled fixtures on failure. This
means the frontend is always renderable - useful for judging without a
perfectly configured environment - while still being a real client of the
FastAPI backend when it's running.
