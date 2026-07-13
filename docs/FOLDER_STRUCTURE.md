# Folder Structure

```
orgpulse-ai/
│
├── README.md                        Quickstart + feature status matrix
├── docker-compose.yml                Full stack: frontend, backend, slack-app, postgres, redis, neo4j
├── .env.example                      All environment variables, documented
│
├── frontend/                         Next.js 15 (App Router) + TypeScript + Tailwind
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            Root layout
│   │   │   ├── page.tsx              Redirects to /dashboard
│   │   │   └── (dashboard)/          Route group sharing the sidebar shell
│   │   │       ├── layout.tsx        Sidebar + content shell
│   │   │       ├── dashboard/        Main dashboard (matches reference design)
│   │   │       ├── knowledge-graph/  Organizational memory graph explorer
│   │   │       ├── dependency-graph/ Cross-team dependency graph explorer
│   │   │       ├── projects/         List + [id] detail
│   │   │       ├── decisions/        List + [id] detail (decision provenance)
│   │   │       ├── experts/          Expert discovery with live search
│   │   │       ├── risks/            Predictive risk + bottleneck ranking
│   │   │       ├── releases/         Release readiness list
│   │   │       ├── timeline/         Merged org timeline
│   │   │       ├── analytics/        Recharts dashboards
│   │   │       ├── integrations/     MCP connector status grid
│   │   │       ├── ai-chat/          Conversational AI chat with citations
│   │   │       └── settings/         Workspace + notification settings
│   │   ├── components/               Sidebar, Topbar, Card, Badge, StatCard,
│   │   │                             DependencyGraphExplorer, KnowledgeGraphExplorer,
│   │   │                             DependencyRiskOverview, AnalyticsCharts
│   │   └── lib/
│   │       ├── api.ts                Backend client with fixture fallback
│   │       ├── fixtureIndex.ts       Typed re-export of bundled fixtures
│   │       ├── types.ts              Shared TypeScript types
│   │       └── fixtures/             Copy of data/fixtures for offline demo mode
│   ├── package.json / tsconfig.json / tailwind.config.ts / next.config.mjs
│   └── Dockerfile
│
├── backend/                          FastAPI
│   ├── app/
│   │   ├── main.py                   App factory, router registration, CORS
│   │   ├── core/
│   │   │   ├── config.py             Settings loaded from environment
│   │   │   └── security.py           JWT issue/verify, demo-mode auth
│   │   ├── routers/                  One file per feature area (see docs/API.md)
│   │   ├── services/
│   │   │   ├── data_loader.py        Single facade over all data access
│   │   │   ├── graph_service.py      networkx-based dependency reasoning
│   │   │   ├── rag_service.py        Organizational memory retrieval + citations
│   │   │   └── risk_engine.py        Predictive risk heuristics
│   │   └── fixtures/                 Copy of data/fixtures used at runtime
│   ├── tests/                        pytest unit tests for graph + RAG logic
│   ├── requirements.txt
│   └── Dockerfile
│
├── mcp_connectors/                   Shared MCP connector layer (used by backend + slack-app)
│   ├── base.py                       BaseConnector: mock/live mode switch
│   ├── github_connector.py, jira_connector.py, notion_connector.py,
│   │   confluence_connector.py, gdrive_connector.py, slack_connector.py,
│   │   calendar_connector.py, linear_connector.py, figma_connector.py,
│   │   gitlab_connector.py, azure_devops_connector.py
│   └── registry.py                   Single source of truth: CONNECTOR_REGISTRY
│
├── slack-app/                        Bolt for Python (Socket Mode)
│   ├── app.py                        Entrypoint
│   ├── config.py                     Environment variables
│   ├── blocks.py                     Block Kit builders (answers, alerts, digest, experts)
│   ├── handlers/
│   │   ├── mentions.py               @OrgPulse -> /api/chat -> cited thread reply
│   │   ├── commands.py                /orgpulse status | risks | experts <topic>
│   │   └── home_tab.py                App Home personal snapshot
│   ├── manifest.yaml                 Slack app manifest (scopes, events, socket mode)
│   ├── requirements.txt
│   └── Dockerfile
│
├── data/
│   ├── generate_mock_data.py         Generates the full realistic dataset
│   └── fixtures/                     10 teams, 120 employees, 40 repos, 150 PRs,
│                                      300 tickets, 50 docs, 100 conversations,
│                                      60 decisions, 30 incidents, 25 releases,
│                                      cross-team dependency graph with the
│                                      Security Review -> Payments API -> Backend
│                                      Core -> Mobile App blocker chain baked in
│
└── docs/
    ├── ARCHITECTURE.md               System design + production migration path
    ├── API.md                        Full endpoint reference + scoring formulas
    ├── FOLDER_STRUCTURE.md           This file
    └── DEMO_SCRIPT.md                The scripted 8-beat demo scenario
```
