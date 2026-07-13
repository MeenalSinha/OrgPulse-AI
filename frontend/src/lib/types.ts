export type Team = { id: string; name: string; description: string; member_count: number; health_score: number };
export type Employee = {
  id: string; name: string; role: string; team_id: string; team_name: string;
  expertise: string[]; join_date: string; contribution_score: number;
};
export type Decision = {
  id: string; title: string; category: string; date: string; rationale: string;
  alternatives_considered: string[]; participant_ids: string[]; outcome: string; evidence: string[];
};
export type Release = { id: string; name: string; project: string; date: string; status: string };
export type Risk = {
  id: string; title: string; severity: string; probability: number;
  affected_projects: string[]; root_cause: string; recommendation: string;
};
export type GraphNode = { id: string; label: string; type: string; status?: string };
export type GraphEdge = { source: string; target: string; relation: string };
export type DependencyGraph = { nodes: GraphNode[]; edges: GraphEdge[] };
export type AIInsight = { id: string; type: string; text: string; link: string };
export type DashboardSummary = {
  at_risk_projects: number; at_risk_projects_delta: string;
  blocked_tasks: number; blocked_tasks_delta: string;
  team_velocity: number; team_velocity_delta: string;
  org_health_score: number; org_health_score_delta: string;
  knowledge_graph_highlights: {
    documents: number; documents_delta: string;
    conversations: number; conversations_delta: string;
    decisions: number; decisions_delta: string;
    people: number; people_delta: string;
    most_active_topics: string[];
  };
  critical_chain?: { chain: string[]; labels: string[]; risk_score: number } | null;
};
