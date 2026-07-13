# Demo Script

This is the scripted scenario baked into the mock dataset. It exercises the
dependency graph, predictive risk, organizational memory, and the Slack
experience in one continuous flow.

## Setup

```bash
docker compose up --build
```

Open the dashboard at http://localhost:3000/dashboard.

## Beat 1 - The dashboard surfaces the problem without being asked

The dashboard's **Dependency Risk Overview** card already shows Payments API
as `Blocked`, Mobile App as `At Risk`, and the callout: *"Payments API is
blocked by Security Review. This may delay 3 dependent projects."* This is
computed live by `graph_service.critical_path()`, not hardcoded copy.

## Beat 2 - Drill into the dependency graph

Click **View Graph** to open `/dependency-graph`. The banner at the top shows
the active blocker chain and its risk score. The graph itself is a real,
zoomable/pannable React Flow canvas driven by `/api/dependency-graph/graph`.

## Beat 3 - Ask why, in the AI Chat

Go to `/ai-chat` (or `@OrgPulse` in Slack) and ask:

> Why is Mobile App at risk?

The response is graph-grounded: it walks the `blocks` edges
(`Security Review -> Payments API -> Backend Core -> Mobile App`), states the
computed risk score, and cites `dependency_graph` plus any related decisions.

## Beat 4 - Check the release risk (the "wow moment")

In `/ai-chat`, ask the blunt question a real engineering manager would ask:

> Can we ship the Mobile App on Friday?

OrgPulse answers **"No."** immediately, then renders the causal chain
top-to-bottom (Security Review -> Payments API -> Backend Core -> Mobile
App), the computed delay probability, why, a concrete mitigation, and the
specific person best positioned to unblock it - all derived live from
`graph_service.critical_path()`, `risk_engine.release_delay_probability()`,
and `rag_service.find_experts()`. Nothing here is scripted text: ask about a
different, healthy release and you'll get "Yes" instead, because the
verdict is computed, not hardcoded (see
`backend/tests/test_release_readiness.py`).

The same rich card renders in Slack when you `@mention` OrgPulse with the
same question - see `slack_app/blocks.py::release_readiness_blocks`.

## Beat 5 - Ask why Payments was architected this way

In the same chat, ask:

> Why did we migrate to PostgreSQL?

The organizational memory service retrieves the matching decision record
(`dec-001`), returns its rationale, alternatives considered, and evidence
IDs, and links to the full decision provenance page at `/decisions/dec-001`.

## Beat 6 - Find who can unblock it

Ask:

> Who understands the Payments API?

or visit `/experts` and search "Payments API". Results are ranked by a
transparent confidence score combining declared expertise, PR history on
impacted services, and incident participation.

## Beat 7 - See the recommendation

`/risks` lists the same blocker as a structured risk record with a concrete
recommendation ("Fast-track Security Review scope for Payments API v2 or
descope the dependent Mobile release items shipping this cycle").

## Beat 8 - The Slack-native version of all of this

In Slack:
```
/orgpulse risks
```
posts a Block Kit risk alert with the blocker chain and recommendation.
```
@OrgPulse why is mobile app at risk?
```
replies in-thread with the same cited answer as the web chat.

---

This single scenario touches: dependency graph reasoning, predictive risk
scoring, organizational memory with citations, decision provenance, expert
discovery, and the Slack-native experience - the full breadth of the spec in
one coherent story.
