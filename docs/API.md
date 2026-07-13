# API Reference

Base URL: `http://localhost:8000`. Full interactive docs at `/docs` (Swagger)
and `/redoc` once the backend is running.

All endpoints accept an optional `Authorization: Bearer <token>` header. If
omitted, requests are treated as a read-only `demo` identity so the API is
explorable without logging in.

## Auth
| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/demo-login` | Issues a JWT for `{email, role}` without a real IdP |
| GET | `/api/auth/slack/callback` | Slack OAuth callback stub (needs `SLACK_CLIENT_ID/SECRET`) |

## Dashboard
| Method | Path | Description |
|---|---|---|
| GET | `/api/dashboard/summary` | Top-line stats + current critical blocker chain |
| GET | `/api/dashboard/recent-decisions` | Latest N decisions |
| GET | `/api/dashboard/upcoming-deadlines` | Releases with non-shipped status |
| GET | `/api/dashboard/ai-insights` | Proactive AI insight feed |
| GET | `/api/dashboard/top-experts` | Highest-contribution employees |

## Knowledge Graph
| Method | Path | Description |
|---|---|---|
| GET | `/api/knowledge-graph/graph` | Entity-relationship graph (people, teams, decisions, docs) |
| GET | `/api/knowledge-graph/highlights` | Aggregate counts for the dashboard card |
| GET | `/api/knowledge-graph/search?q=` | Hybrid lexical search over decisions/docs/conversations/PRs |

## Dependency Graph
| Method | Path | Description |
|---|---|---|
| GET | `/api/dependency-graph/graph` | Full graph payload (nodes + edges) |
| GET | `/api/dependency-graph/blocker-chains` | All `blocks`-only chains, longest first |
| GET | `/api/dependency-graph/critical-path` | Highest-risk active blocker chain |
| GET | `/api/dependency-graph/impact/{node_id}` | Downstream impact + upstream dependencies + risk score |

## Projects / Decisions / Experts / Risks / Releases / Timeline
| Method | Path | Description |
|---|---|---|
| GET | `/api/projects` / `/api/projects/{id}` | Project list / detail with linked releases + open tickets |
| GET | `/api/decisions` / `/api/decisions/{id}` | Decision list / full provenance record with participants |
| GET | `/api/experts` | Top contributors org-wide |
| GET | `/api/experts/search?topic=` | Ranked expert discovery for a topic |
| GET | `/api/risks` | Predictive risk list |
| GET | `/api/risks/bottlenecks` | Dependency graph nodes ranked by computed risk score |
| GET | `/api/releases` / `/api/releases/{id}/risk` | Release list / delay probability estimate |
| GET | `/api/timeline` | Merged, sorted feed of decisions + releases + incidents |

## Chat (Organizational Memory)
| Method | Path | Description |
|---|---|---|
| POST | `/api/chat` | `{query}` -> `{answer, citations, confidence}`. Never fabricates a citation - if there's no evidence, says so. |
| GET | `/api/chat/citation/{id}` | Resolves a citation ID back to its source record |

## Analytics
| Method | Path | Description |
|---|---|---|
| GET | `/api/analytics/velocity` | Team health scores |
| GET | `/api/analytics/pr-throughput` | PR counts by status |
| GET | `/api/analytics/incident-trend` | Incident counts by severity |

## Integrations
| Method | Path | Description |
|---|---|---|
| GET | `/api/integrations` | Status of all 11 MCP connectors |
| POST | `/api/integrations/{id}/sync` | Triggers a sync, returns record count + timestamp |

## Risk score formula

```
risk_score(node) = min(99, status_weight(node.status) + 8 * len(downstream_impact(node)))

status_weight = { blocked: 40, delayed: 30, at_risk: 25, on_track: 5 }
```

## Release delay probability formula

```
base = { Shipped: 5, On Track: 20, At Risk: 65, Delayed: 85 }[release.status]
probability = min(97, base + critical_chain.risk_score // 3)
```
