"""
OrgPulse AI - Mock Organizational Data Generator
--------------------------------------------------
Generates a self-consistent, realistic dataset that represents a mid-size
engineering org: teams, employees, repositories, pull requests, tickets,
architecture docs, slack conversations, releases, incidents, decisions and
cross-team dependencies (including an intentional blocker chain used for the
scripted demo scenario).

Run:
    python generate_mock_data.py

Output:
    ./fixtures/*.json

The backend loads these files at startup (see backend/app/services/data_loader.py).
The frontend also ships a copy under frontend/src/lib/fixtures for offline demo mode.
"""
import json
import random
import os
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(OUT_DIR, exist_ok=True)

TEAM_NAMES = [
    "Platform", "Payments", "Mobile", "Web Frontend", "Backend Core",
    "Data Infrastructure", "Security", "DevOps", "Growth", "Analytics",
]

FIRST_NAMES = [
    "Sarah", "Alex", "Priya", "Miguel", "Carl", "Jenna", "Wei", "Fatima",
    "Noah", "Elena", "Ravi", "Grace", "Tomas", "Aisha", "Lucas", "Mei",
    "Omar", "Sofia", "Ivan", "Keiko", "Daniel", "Nadia", "Sam", "Julia",
    "Kenji", "Amara", "Diego", "Hana", "Victor", "Lila",
]
LAST_NAMES = [
    "Chen", "Johnson", "Patel", "Santos", "Brown", "Kim", "Zhang", "Ahmed",
    "Garcia", "Novak", "Sharma", "Lee", "Rossi", "Khan", "Silva", "Wong",
    "Hassan", "Petrov", "Kaur", "Nguyen", "Costa", "Ibrahim", "Weiss", "Park",
]

ROLES = [
    "Backend Engineer", "Frontend Engineer", "DevOps Engineer",
    "Security Engineer", "Data Engineer", "ML Engineer", "Engineering Manager",
    "Product Manager", "QA Engineer", "Site Reliability Engineer",
]

SERVICES = [
    "User Service", "Payments API", "Security Review Service", "Analytics Pipeline",
    "Database Migration Tool", "Mobile Gateway", "Notification Service",
    "Auth Service", "Billing Service", "Search Service", "Recommendation Engine",
    "Cloud Migration Layer", "Reporting Service", "Feature Flag Service",
]

PROJECTS = [
    "Project Atlas", "Mobile App Release 5.0", "Payments API v2", "Analytics Dashboard",
    "Security Hardening Q2", "GraphQL Migration", "Database Sharding",
    "Onboarding Revamp", "Search Relevance 2.0", "Billing Overhaul",
]

DECISION_TOPICS = [
    ("Migrate to PostgreSQL", "Architecture",
     "The team evaluated MySQL vs PostgreSQL for the new Billing Service and chose "
     "PostgreSQL for its native JSONB support and stronger consistency guarantees."),
    ("Adopt GraphQL API", "Tech Stack",
     "Frontend and Backend Core agreed to adopt GraphQL for the Mobile Gateway to "
     "reduce over-fetching and unify the API surface across web and mobile clients."),
    ("Kill Feature: Legacy Reports", "Product",
     "Usage data showed under 2 percent adoption of the legacy reporting module, so "
     "the Analytics team deprecated it in favor of the new Analytics Dashboard."),
    ("Introduce Security Review Gate", "Process",
     "Following an incident in the Payments flow, Security introduced a mandatory "
     "review gate for any service touching payment data before it can ship."),
    ("Split Monolith into Services", "Architecture",
     "Platform and Backend Core agreed to split the monolith into Payments API, "
     "User Service and Notification Service to reduce deploy coupling."),
    ("Move CI to GitHub Actions", "Infrastructure",
     "DevOps migrated the build pipeline off Jenkins to GitHub Actions to cut build "
     "times and simplify onboarding for new repositories."),
    ("Adopt Feature Flags", "Process",
     "Growth and Platform introduced a feature flag service to decouple deploys from "
     "releases and support progressive rollouts."),
    ("Cloud Migration to Multi-Region", "Infrastructure",
     "Platform and Security jointly decided to migrate core services to a multi "
     "region cloud footprint to meet new data residency requirements."),
]

INCIDENT_TITLES = [
    "Payments API elevated error rate", "Auth Service latency spike",
    "Mobile Gateway timeout cascade", "Database Migration data drift",
    "Notification Service duplicate sends", "Search Service index staleness",
    "Billing Service double charge", "Cloud Migration DNS misconfiguration",
]

SLACK_CHANNELS = [
    "#payments", "#backend-core", "#mobile-team", "#security", "#platform",
    "#analytics", "#devops", "#growth", "#incidents", "#architecture",
]


def name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def rand_date(days_back=540):
    return (datetime(2026, 6, 20) - timedelta(days=random.randint(0, days_back))).strftime("%Y-%m-%d")


def gen_teams():
    teams = []
    for i, tname in enumerate(TEAM_NAMES):
        teams.append({
            "id": f"team-{i+1:02d}",
            "name": tname,
            "description": f"Owns systems and delivery for {tname}.",
            "member_count": 0,
            "health_score": random.randint(58, 96),
        })
    return teams


def gen_employees(teams):
    employees = []
    eid = 1
    per_team = 120 // len(teams)
    remainder = 120 - per_team * len(teams)
    for i, team in enumerate(teams):
        count = per_team + (1 if i < remainder else 0)
        for _ in range(count):
            emp = {
                "id": f"emp-{eid:03d}",
                "name": name(),
                "role": random.choice(ROLES),
                "team_id": team["id"],
                "team_name": team["name"],
                "expertise": random.sample(SERVICES, k=random.randint(1, 3)),
                "join_date": rand_date(900),
                "contribution_score": random.randint(40, 99),
            }
            employees.append(emp)
            eid += 1
        team["member_count"] = count
    return employees


def gen_repos(teams):
    repos = []
    for i in range(40):
        team = random.choice(teams)
        repos.append({
            "id": f"repo-{i+1:03d}",
            "name": f"{team['name'].lower().replace(' ', '-')}-{random.choice(['service', 'api', 'app', 'lib', 'worker'])}-{i+1}",
            "team_id": team["id"],
            "team_name": team["name"],
            "language": random.choice(["TypeScript", "Python", "Go", "Java", "Kotlin"]),
            "open_prs": random.randint(0, 12),
            "stars_internal": random.randint(0, 340),
        })
    return repos


def gen_prs(repos, employees):
    prs = []
    for i in range(150):
        repo = random.choice(repos)
        author = random.choice(employees)
        prs.append({
            "id": f"pr-{i+1:04d}",
            "title": f"{random.choice(['Fix', 'Add', 'Refactor', 'Optimize', 'Migrate', 'Harden'])} "
                     f"{random.choice(SERVICES)} {random.choice(['auth flow', 'query layer', 'schema', 'retry logic', 'caching', 'tests'])}",
            "repo_id": repo["id"],
            "repo_name": repo["name"],
            "author_id": author["id"],
            "author_name": author["name"],
            "status": random.choice(["merged", "merged", "merged", "open", "review"]),
            "impacted_services": random.sample(SERVICES, k=random.randint(1, 4)),
            "created_at": rand_date(400),
        })
    return prs


def gen_tickets(teams, employees):
    tickets = []
    for i in range(300):
        team = random.choice(teams)
        assignee = random.choice(employees)
        tickets.append({
            "id": f"JIRA-{1000+i}",
            "title": f"{random.choice(['Investigate', 'Implement', 'Design', 'Test', 'Document'])} "
                     f"{random.choice(SERVICES)} {random.choice(['bug', 'enhancement', 'spike', 'migration task'])}",
            "team_id": team["id"],
            "assignee_id": assignee["id"],
            "assignee_name": assignee["name"],
            "status": random.choice(["Done", "Done", "In Progress", "Blocked", "To Do"]),
            "priority": random.choice(["Low", "Medium", "High", "Critical"]),
            "created_at": rand_date(400),
        })
    return tickets


def gen_docs(teams):
    docs = []
    for i in range(50):
        team = random.choice(teams)
        docs.append({
            "id": f"doc-{i+1:03d}",
            "title": f"{random.choice(SERVICES)} Architecture Overview {i+1}",
            "team_id": team["id"],
            "type": random.choice(["Architecture Doc", "RFC", "Runbook", "Design Doc"]),
            "last_updated": rand_date(400),
            "quality_score": random.randint(50, 98),
        })
    return docs


def gen_conversations(employees):
    convos = []
    for i in range(100):
        participants = random.sample(employees, k=random.randint(2, 5))
        convos.append({
            "id": f"conv-{i+1:03d}",
            "channel": random.choice(SLACK_CHANNELS),
            "summary": f"Discussion about {random.choice(SERVICES)} "
                       f"{random.choice(['rollout', 'incident', 'design tradeoffs', 'ownership', 'on-call handoff'])}.",
            "participant_ids": [p["id"] for p in participants],
            "timestamp": rand_date(300),
        })
    return convos


def gen_decisions(employees):
    decisions = []
    for i, (title, category, rationale) in enumerate(DECISION_TOPICS):
        participants = random.sample(employees, k=random.randint(3, 6))
        decisions.append({
            "id": f"dec-{i+1:03d}",
            "title": title,
            "category": category,
            "date": rand_date(500),
            "rationale": rationale,
            "alternatives_considered": random.sample(
                ["Do nothing", "Third-party vendor", "In-house build", "Partial rollout", "Delay to next quarter"],
                k=2,
            ),
            "participant_ids": [p["id"] for p in participants],
            "outcome": random.choice(["Adopted", "Adopted", "Adopted and later revised"]),
            "evidence": [
                f"PR-{random.randint(1, 150):04d}", f"JIRA-{random.randint(1000, 1300)}",
                f"conv-{random.randint(1, 100):03d}",
            ],
        })
    # pad up to 60 with generated variants
    extra_titles = [
        "Standardize on Terraform", "Consolidate Logging to OpenTelemetry",
        "Retire the Legacy Monolith", "Adopt Trunk-Based Development",
        "Introduce Service Mesh", "Move Secrets to Vault",
        "Adopt Contract Testing", "Unify Design System",
        "Introduce SLOs for Tier-1 Services", "Deprecate REST v1",
        "Adopt Event-Driven Billing", "Consolidate Data Warehouses",
        "Introduce Canary Deployments", "Adopt Feature-Team Model",
        "Standardize Incident Response Runbooks", "Move CI Runners to Self-Hosted",
        "Adopt pgvector for Embeddings", "Introduce API Gateway",
        "Sunset Confluence in Favor of Notion", "Adopt Blue-Green Deploys",
        "Introduce Data Retention Policy", "Consolidate Auth Providers",
        "Adopt Mono-repo for Mobile", "Introduce Chaos Testing",
        "Standardize on gRPC Internally", "Retire Legacy Reporting Warehouse",
        "Adopt Zero Trust Networking", "Introduce Cost Guardrails",
        "Adopt Progressive Delivery", "Consolidate On-Call Rotations",
        "Introduce Design Review Board", "Adopt Semantic Versioning Org-Wide",
        "Move Feature Flags to Native Service", "Retire Third-Party Analytics Vendor",
        "Adopt GraphQL Federation", "Introduce Data Classification Standard",
        "Consolidate Notification Channels", "Adopt Infrastructure Cost Dashboards",
        "Introduce Security Champions Program", "Adopt Backend for Frontend Pattern",
        "Retire Legacy Mobile SDK", "Introduce Org-Wide API Style Guide",
        "Adopt Read Replicas for Reporting", "Consolidate Test Environments",
        "Introduce Dependency Freshness Policy", "Adopt Structured Logging Standard",
        "Retire Manual Release Checklist", "Introduce Data Lineage Tracking",
        "Adopt Platform Team Model", "Consolidate Internal Developer Portal",
        "Introduce Error Budget Policy", "Adopt Config as Code",
        "Retire Legacy VPN in Favor of Zero Trust",
    ]
    for j, title in enumerate(extra_titles[: 60 - len(decisions)]):
        participants = random.sample(employees, k=random.randint(2, 5))
        decisions.append({
            "id": f"dec-{len(decisions)+1:03d}",
            "title": title,
            "category": random.choice(["Architecture", "Process", "Tech Stack", "Product", "Infrastructure"]),
            "date": rand_date(500),
            "rationale": f"{title} was adopted after review by the owning team to reduce operational risk "
                         f"and improve delivery velocity around {random.choice(SERVICES)}.",
            "alternatives_considered": random.sample(
                ["Do nothing", "Third-party vendor", "In-house build", "Partial rollout", "Delay to next quarter"],
                k=2,
            ),
            "participant_ids": [p["id"] for p in participants],
            "outcome": "Adopted",
            "evidence": [f"PR-{random.randint(1, 150):04d}", f"JIRA-{random.randint(1000, 1300)}"],
        })
    return decisions


def gen_incidents(teams, employees):
    incidents = []
    for i, title in enumerate(INCIDENT_TITLES):
        participants = random.sample(employees, k=random.randint(2, 5))
        incidents.append({
            "id": f"inc-{i+1:03d}",
            "title": title,
            "severity": random.choice(["SEV1", "SEV2", "SEV3"]),
            "date": rand_date(300),
            "resolved": True,
            "participant_ids": [p["id"] for p in participants],
            "resolution_summary": f"Root cause identified in {random.choice(SERVICES)}; mitigated with a "
                                   f"rollback and follow-up hardening tickets.",
        })
    # pad to 30
    while len(incidents) < 30:
        i = len(incidents)
        participants = random.sample(employees, k=random.randint(2, 4))
        incidents.append({
            "id": f"inc-{i+1:03d}",
            "title": f"{random.choice(SERVICES)} degraded performance",
            "severity": random.choice(["SEV2", "SEV3"]),
            "date": rand_date(300),
            "resolved": True,
            "participant_ids": [p["id"] for p in participants],
            "resolution_summary": "Mitigated via config rollback and added monitoring alert.",
        })
    return incidents


def gen_releases(projects):
    releases = []
    for i in range(25):
        proj = random.choice(projects)
        releases.append({
            "id": f"rel-{i+1:03d}",
            "name": f"{proj} - Release {round(random.uniform(1.0, 6.0), 1)}",
            "project": proj,
            "date": rand_date(300),
            "status": random.choice(["Shipped", "Shipped", "At Risk", "On Track", "Delayed"]),
        })
    return releases


def gen_dependency_graph():
    """
    Builds the cross-team dependency graph including the intentional
    demo blocker chain:
      Security Review -> Payments API -> Backend -> Mobile App
    """
    nodes = [
        {"id": "user-service", "label": "User Service", "type": "service", "status": "on_track"},
        {"id": "payments-api", "label": "Payments API", "type": "service", "status": "blocked"},
        {"id": "security-review", "label": "Security Review", "type": "process", "status": "delayed"},
        {"id": "mobile-app", "label": "Mobile App", "type": "project", "status": "at_risk"},
        {"id": "backend-core", "label": "Backend Core", "type": "team", "status": "at_risk"},
        {"id": "analytics-pipeline", "label": "Analytics Pipeline", "type": "service", "status": "on_track"},
        {"id": "database-migration", "label": "Database Migration", "type": "project", "status": "on_track"},
        {"id": "notification-service", "label": "Notification Service", "type": "service", "status": "on_track"},
        {"id": "search-service", "label": "Search Service", "type": "service", "status": "on_track"},
        {"id": "billing-service", "label": "Billing Service", "type": "service", "status": "on_track"},
    ]
    edges = [
        {"source": "security-review", "target": "payments-api", "relation": "blocks"},
        {"source": "payments-api", "target": "backend-core", "relation": "blocks"},
        {"source": "backend-core", "target": "mobile-app", "relation": "blocks"},
        {"source": "payments-api", "target": "analytics-pipeline", "relation": "depends_on"},
        {"source": "user-service", "target": "payments-api", "relation": "depends_on"},
        {"source": "database-migration", "target": "security-review", "relation": "depends_on"},
        {"source": "payments-api", "target": "notification-service", "relation": "uses"},
        {"source": "billing-service", "target": "payments-api", "relation": "depends_on"},
        {"source": "search-service", "target": "user-service", "relation": "depends_on"},
        {"source": "mobile-app", "target": "search-service", "relation": "uses"},
    ]
    return {"nodes": nodes, "edges": edges}


def gen_risks():
    return [
        {
            "id": "risk-001",
            "title": "Mobile App release at risk due to Payments API blocker",
            "severity": "High",
            "probability": 68,
            "affected_projects": ["Mobile App Release 5.0"],
            "root_cause": "Security Review delay on Payments API v2 propagates through Backend Core.",
            "recommendation": "Fast-track Security Review scope for Payments API v2 or descope the "
                               "dependent Mobile release items shipping this cycle.",
        },
        {
            "id": "risk-002",
            "title": "Knowledge silo on Search Service",
            "severity": "Medium",
            "probability": 41,
            "affected_projects": ["Search Relevance 2.0"],
            "root_cause": "Only one engineer has merged production changes to Search Service in the last quarter.",
            "recommendation": "Pair a second engineer on the next two Search Service tickets.",
        },
        {
            "id": "risk-003",
            "title": "Approval bottleneck on Security reviews",
            "severity": "High",
            "probability": 74,
            "affected_projects": ["Payments API v2", "Security Hardening Q2"],
            "root_cause": "Security team has 3 open reviews against 1 available reviewer this sprint.",
            "recommendation": "Add a second reviewer or triage lower-risk reviews to async approval.",
        },
    ]


def gen_ai_insights():
    return [
        {"id": "insight-1", "type": "risk", "text": "3 projects are at high risk due to dependencies.", "link": "risks"},
        {"id": "insight-2", "type": "blocker", "text": "Security Review is the top blocker this week.", "link": "dependency-graph"},
        {"id": "insight-3", "type": "knowledge", "text": "A similar issue was resolved in #backend-core 2 weeks ago.", "link": "knowledge-graph"},
    ]


def main():
    teams = gen_teams()
    employees = gen_employees(teams)
    repos = gen_repos(teams)
    prs = gen_prs(repos, employees)
    tickets = gen_tickets(teams, employees)
    docs = gen_docs(teams)
    conversations = gen_conversations(employees)
    decisions = gen_decisions(employees)
    incidents = gen_incidents(teams, employees)
    releases = gen_releases(PROJECTS)
    dependency_graph = gen_dependency_graph()
    risks = gen_risks()
    ai_insights = gen_ai_insights()

    dashboard_summary = {
        "at_risk_projects": 8,
        "at_risk_projects_delta": "2 more than last week",
        "blocked_tasks": 23,
        "blocked_tasks_delta": "-5 from yesterday",
        "team_velocity": 68,
        "team_velocity_delta": "+8% from last week",
        "org_health_score": 82,
        "org_health_score_delta": "+6 from last month",
        "knowledge_graph_highlights": {
            "documents": len(docs) * 25,  # scaled to look like a mature org (~1248 in mock)
            "documents_delta": "+24 this week",
            "conversations": len(conversations) * 86,
            "conversations_delta": "+156 this week",
            "decisions": len(decisions) * 5,
            "decisions_delta": "+8 this week",
            "people": len(employees) * 4,
            "people_delta": "+12 this week",
            "most_active_topics": ["Payments API", "Authentication", "Mobile App", "Security", "Data Pipeline"],
        },
    }

    fixtures = {
        "teams": teams,
        "employees": employees,
        "repos": repos,
        "pull_requests": prs,
        "tickets": tickets,
        "docs": docs,
        "conversations": conversations,
        "decisions": decisions,
        "incidents": incidents,
        "releases": releases,
        "dependency_graph": dependency_graph,
        "risks": risks,
        "ai_insights": ai_insights,
        "dashboard_summary": dashboard_summary,
        "projects": [{"id": f"proj-{i+1:02d}", "name": p} for i, p in enumerate(PROJECTS)],
    }

    for key, value in fixtures.items():
        with open(os.path.join(OUT_DIR, f"{key}.json"), "w") as f:
            json.dump(value, f, indent=2)

    print(f"Generated {len(fixtures)} fixture files in {OUT_DIR}")
    print(f"  teams={len(teams)} employees={len(employees)} repos={len(repos)} "
          f"prs={len(prs)} tickets={len(tickets)} docs={len(docs)} "
          f"conversations={len(conversations)} decisions={len(decisions)} "
          f"incidents={len(incidents)} releases={len(releases)}")


if __name__ == "__main__":
    main()
