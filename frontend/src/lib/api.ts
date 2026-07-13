/**
 * API client for the OrgPulse backend.
 *
 * Every function tries the live FastAPI backend first. If the backend is
 * unreachable (e.g. exploring the UI without `docker compose up` running),
 * it falls back to the bundled fixtures in src/lib/fixtures so the demo
 * always renders something meaningful instead of an error screen.
 */
import fixtures from "./fixtureIndex";

const BASE_URL = typeof window === "undefined" 
  ? process.env.API_BASE_URL_SERVER || "http://backend:8000"
  : process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function get<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${BASE_URL}${path}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return (await res.json()) as T;
  } catch (error) {
    console.error(`[API Fetch Error] GET ${path}:`, error);
    return fallback;
  }
}

async function post<T>(path: string, body: unknown, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export const api = {
  dashboardSummary: () => get("/api/dashboard/summary", fixtures.dashboardSummaryFallback),
  recentDecisions: () => get("/api/dashboard/recent-decisions", fixtures.decisions.slice(0, 3)),
  upcomingDeadlines: () => get("/api/dashboard/upcoming-deadlines", fixtures.releases.slice(0, 3)),
  aiInsights: () => get("/api/dashboard/ai-insights", fixtures.aiInsights),
  topExperts: () => get("/api/dashboard/top-experts", fixtures.employees.slice(0, 4)),

  dependencyGraph: () => get("/api/dependency-graph/graph", fixtures.dependencyGraph),
  blockerChains: () => get("/api/dependency-graph/blocker-chains", []),
  criticalPath: () => get<any>("/api/dependency-graph/critical-path", null),

  knowledgeGraph: () => get("/api/knowledge-graph/graph", { nodes: [], edges: [] }),
  knowledgeHighlights: () =>
    get("/api/knowledge-graph/highlights", fixtures.dashboardSummaryFallback.knowledge_graph_highlights),

  projects: () => get("/api/projects", fixtures.projects),
  decisions: () => get("/api/decisions", fixtures.decisions),
  decision: (id: string) =>
    get(`/api/decisions/${id}`, fixtures.decisions.find((d: any) => d.id === id) ?? null),

  experts: () => get("/api/experts", fixtures.employees.slice(0, 20)),
  searchExperts: (topic: string) =>
    get(`/api/experts/search?topic=${encodeURIComponent(topic)}`, []),

  risks: () => get("/api/risks", fixtures.risks),
  bottlenecks: () => get("/api/risks/bottlenecks", []),

  releases: () => get("/api/releases", fixtures.releases),
  timeline: () => get("/api/timeline", []),

  velocity: () => get("/api/analytics/velocity", []),
  prThroughput: () => get("/api/analytics/pr-throughput", []),
  incidentTrend: () => get("/api/analytics/incident-trend", []),

  integrations: () => get("/api/integrations", []),

  chat: (query: string) =>
    post("/api/chat", { query }, {
      answer: "OrgPulse could not reach the backend. Start the FastAPI server to enable live answers.",
      citations: [],
      confidence: 0,
      synthesized_by: "none",
      release_readiness: null,
    }),
};
