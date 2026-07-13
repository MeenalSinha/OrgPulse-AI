# OrgPulse AI - The Organizational Intelligence Graph

**The AI that remembers your company, understands how work flows, and prevents delays before they happen.**

Built for the Slack Hack / Devpost competition. OrgPulse combines an
**Organizational Memory Graph** (why did we decide X, who worked on Y) with a
**Cross-Team Dependency Graph** (what blocks what, what breaks if X breaks) so
that instead of keyword search, the AI reasons over relationships.

This repository is a complete, runnable prototype: Next.js frontend, FastAPI
backend, a Slack Bolt app, an MCP connector layer, and a realistic mock
dataset large enough to demonstrate every feature immediately.

---

## Quickstart (Docker, recommended)

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- The Slack app does not start by default (it needs real Slack tokens).
  Run it with: `docker compose --profile slack up`

## Quickstart (without Docker)

```bash
# 1. Generate the mock dataset (already generated and committed under data/fixtures,
#    re-run any time to reshuffle the demo data)
python3 data/generate_mock_data.py

# 2. Backend
cd backend
pip install -r requirements.txt --break-system-packages
PYTHONPATH=.. uvicorn app.main:app --reload --port 8000

# 3. Frontend (new terminal)
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Open http://localhost:3000 - it redirects to `/dashboard`.

The frontend works even if the backend isn't running: every API call falls
back to the bundled fixtures in `frontend/src/lib/fixtures`, so the UI is
always explorable.

## Slack app

```bash
cd slack-app
pip install -r requirements.txt
cp .env.example .env   # fill in SLACK_BOT_TOKEN / SLACK_APP_TOKEN
python app.py
```

See `slack-app/README.md` for the full Slack app setup (manifest, OAuth
scopes, Socket Mode).

---

## What's implemented vs. mocked

This is a hackathon prototype, built to be honest about what's real:

| Layer | Status |
|---|---|
| Dependency graph reasoning (blocker chains, downstream impact, risk scoring) | **Real** - implemented with `networkx`, covered by unit tests |
| Organizational memory retrieval + citations | **Real** hybrid lexical + graph-grounded retrieval. Synthesis uses a deterministic, fully-cited template by default; wire `ANTHROPIC_API_KEY` to have Claude compose the final answer from the same retrieved evidence |
| REST API (17 route groups) | **Real** - FastAPI, fully wired to the frontend |
| Frontend (20 routes, marketing + app + interactive graph explorers) | **Real** - Next.js 15 + React Flow + Recharts, builds cleanly, includes landing page, features page, dark mode toggle, loading skeletons, and empty states |
| Slack app (@mentions, slash command, App Home) | **Real** Bolt app, calls the live backend |
| MCP connectors (11 sources) | **Interface is real**; each connector ships in mock mode by default and is written so flipping `MCP_MODE=live` + setting a server URL swaps in a real MCP session with zero changes to routers, graph builder, or Slack app |
| Neo4j / pgvector / Qdrant | **Architected for, not wired.** The prototype uses JSON fixtures behind a single `DataStore` facade (`backend/app/services/data_loader.py`) specifically so swapping in real graph/vector stores only touches one file. See `docs/ARCHITECTURE.md` |
| Auth | JWT issuing works end to end; Slack OAuth callback is a stub that needs real `SLACK_CLIENT_ID/SECRET` to exchange a code |

## Repository layout

See `docs/FOLDER_STRUCTURE.md` for the annotated full tree.

```
orgpulse-ai/
  frontend/            Next.js 15 app: landing page, features page, and the app
                        (dashboard, graphs, chat, Slack config, demo data, etc.)
  backend/              FastAPI app (routers, services, tests)
  slack-app/            Bolt for Python app (mentions, slash command, home tab)
  mcp_connectors/       Shared connector layer used by backend + slack-app
  data/                 Mock data generator + generated fixtures
  docs/                 Architecture (+ diagram), API reference, setup, demo script
  .github/workflows/    CI: backend tests, frontend build, slack-app syntax check
  docker-compose.yml
  .env.example
```

## Demo scenario

`docs/DEMO_SCRIPT.md` walks through the scripted blocker chain (Security
Review blocks Payments API blocks Backend Core blocks Mobile App) that
exercises nearly every major feature in one flow.

## Audit

`docs/AUDIT_REPORT.md` documents a real verification pass: 14 concrete
issues found (including a privilege-escalation bug and an undiscoverable
flagship feature) and fixed, each with before/after verification. Read it
before assuming anything works - it's more useful than a status badge.

## Tests

```bash
cd backend
PYTHONPATH=.. python3 -m pytest tests/ -v
```

## CI

`.github/workflows/ci.yml` runs on every push/PR: backend pytest suite,
frontend production build, and a syntax check of the Slack app + MCP
connectors (no live Slack tokens required).

## Pages

Marketing: `/` (landing), `/features`.
App (behind the sidebar shell): `/dashboard`, `/knowledge-graph`,
`/dependency-graph`, `/projects(+[id])`, `/decisions(+[id])`, `/experts`,
`/risks` (includes a risk heatmap), `/releases`, `/timeline`, `/analytics`,
`/integrations`, `/slack-config`, `/demo-data`, `/ai-chat`, `/settings`.
Dark mode toggle lives in the top bar and persists per-browser.
