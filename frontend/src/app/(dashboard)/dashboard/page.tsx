import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { StatCard } from "@/components/StatCard";
import { Badge, statusTone } from "@/components/Badge";
import { DependencyRiskOverview } from "@/components/DependencyRiskOverview";
import { FadeInStagger, FadeInItem } from "@/components/Motion";
import { api } from "@/lib/api";
import {
  ShieldAlert, Lock, TrendingUp, HeartPulse, FileText, MessagesSquare,
  Scale as ScaleIcon, Users, AlertTriangle, MessageCircle, ArrowRight,
} from "lucide-react";
import Link from "next/link";

export default async function DashboardPage() {
  const BarChart = ({ color }: { color: string }) => (
    <svg width="64" height="24" viewBox="0 0 64 24" className={color}>
      <rect x="0" y="12" width="3" height="12" rx="1.5" fill="currentColor" opacity="0.4" />
      <rect x="6" y="8" width="3" height="16" rx="1.5" fill="currentColor" opacity="0.6" />
      <rect x="12" y="14" width="3" height="10" rx="1.5" fill="currentColor" opacity="0.4" />
      <rect x="18" y="4" width="3" height="20" rx="1.5" fill="currentColor" opacity="0.8" />
      <rect x="24" y="10" width="3" height="14" rx="1.5" fill="currentColor" opacity="0.5" />
      <rect x="30" y="6" width="3" height="18" rx="1.5" fill="currentColor" opacity="0.7" />
      <rect x="36" y="16" width="3" height="8" rx="1.5" fill="currentColor" opacity="0.3" />
      <rect x="42" y="10" width="3" height="14" rx="1.5" fill="currentColor" opacity="0.6" />
      <rect x="48" y="4" width="3" height="20" rx="1.5" fill="currentColor" opacity="0.8" />
      <rect x="54" y="12" width="3" height="12" rx="1.5" fill="currentColor" opacity="0.4" />
      <rect x="60" y="2" width="3" height="22" rx="1.5" fill="currentColor" />
    </svg>
  );

  const WavyLine = () => (
    <svg width="120" height="24" viewBox="0 0 120 24" className="text-white">
      <path d="M0,12 C15,0 35,24 60,12 C85,0 105,24 120,12" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
  );
  const [summary, deadlines, decisions, insights, experts] = await Promise.all([
    api.dashboardSummary(),
    api.upcomingDeadlines(),
    api.recentDecisions(),
    api.aiInsights(),
    api.topExperts(),
  ]);

  const highlights = summary.knowledge_graph_highlights;

  return (
    <div>
      <Topbar greetingName="Carl" />

      <FadeInStagger className="mt-8 grid grid-cols-1 gap-6 px-8 md:grid-cols-2 xl:grid-cols-4">
        <FadeInItem>
          <StatCard
            label="At Risk Projects"
            value={summary.at_risk_projects}
            delta={summary.at_risk_projects_delta}
            tone="danger"
            icon={<ShieldAlert className="h-4 w-4 text-danger-text" />}
            chart={<BarChart color="text-danger-text" />}
          />
        </FadeInItem>
        <FadeInItem>
          <StatCard
            label="Blocked Tasks"
            value={summary.blocked_tasks}
            delta={summary.blocked_tasks_delta}
            tone="warn"
            icon={<Lock className="h-4 w-4 text-warn-text" />}
            chart={<BarChart color="text-warn-text" />}
          />
        </FadeInItem>
        <FadeInItem>
          <StatCard
            label="Team Velocity"
            value={`${summary.team_velocity}%`}
            delta={summary.team_velocity_delta}
            tone="ok"
            icon={<TrendingUp className="h-4 w-4 text-ok-text" />}
            chart={<BarChart color="text-ok-text" />}
          />
        </FadeInItem>
        <FadeInItem>
          <StatCard
            label="Org Health Score"
            value={`${summary.org_health_score}/100`}
            delta={summary.org_health_score_delta}
            tone="dark"
            icon={<HeartPulse className="h-4 w-4 text-white" />}
            chart={<WavyLine />}
          />
        </FadeInItem>
      </FadeInStagger>

      <div className="mt-6 grid grid-cols-1 gap-6 px-8 xl:grid-cols-3">
        <Card className="xl:col-span-1">
          <CardHeader
            title="Dependency Risk Overview"
            action={
              <Link href="/dependency-graph" className="text-[12.5px] font-medium text-muted hover:text-ink">
                View Graph
              </Link>
            }
          />
          <DependencyRiskOverview />
        </Card>

        <Card>
          <CardHeader
            title="Upcoming Deadlines"
            action={<Link href="/releases" className="text-[12.5px] font-medium text-muted hover:text-ink">View Calendar</Link>}
          />
          <div className="space-y-4">
            {deadlines.map((d: any) => (
              <div key={d.id} className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className={`h-2 w-2 shrink-0 rounded-full ${
                    d.status === "At Risk" || d.status === "Delayed" ? "bg-danger-text" :
                    d.status === "On Track" ? "bg-ok-text" : "bg-warn-text"
                  }`} />
                  <div>
                    <div className="text-[13.5px] font-medium leading-tight">{d.name}</div>
                    <div className="text-[12px] text-muted">{d.date}</div>
                  </div>
                </div>
                <Badge tone={statusTone(d.status)}>{d.status}</Badge>
              </div>
            ))}
          </div>
          <Link href="/releases" className="mt-5 flex items-center gap-1 text-[12.5px] font-medium text-sage-600 hover:underline">
            View all deadlines <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </Card>

        <Card>
          <CardHeader
            title="Recent Decisions"
            action={<Link href="/decisions" className="text-[12.5px] font-medium text-muted hover:text-ink">View All</Link>}
          />
          <div className="space-y-4">
            {decisions.map((d: any) => (
              <Link key={d.id} href={`/decisions/${d.id}`} className="flex items-center gap-3 group">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-sage-50 text-sage-700">
                  <ScaleIcon className="h-4 w-4" />
                </span>
                <div className="min-w-0">
                  <div className="truncate text-[13.5px] font-medium group-hover:underline">{d.title}</div>
                  <div className="text-[12px] text-muted">{d.date} &middot; {d.category}</div>
                </div>
              </Link>
            ))}
          </div>
        </Card>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 px-8 xl:grid-cols-3">
        <Card>
          <CardHeader
            title="Knowledge Graph Highlights"
            action={<Link href="/knowledge-graph" className="text-[12.5px] font-medium text-muted hover:text-ink">Explore Graph</Link>}
          />
          <div className="grid grid-cols-2 gap-4">
            <HighlightStat icon={<FileText className="h-4 w-4 text-sage-700" />} label="Documents" value={highlights.documents} delta={highlights.documents_delta} />
            <HighlightStat icon={<MessagesSquare className="h-4 w-4 text-sage-700" />} label="Conversations" value={highlights.conversations} delta={highlights.conversations_delta} />
            <HighlightStat icon={<ScaleIcon className="h-4 w-4 text-sage-700" />} label="Decisions" value={highlights.decisions} delta={highlights.decisions_delta} />
            <HighlightStat icon={<Users className="h-4 w-4 text-sage-700" />} label="People" value={highlights.people} delta={highlights.people_delta} />
          </div>
          <div className="mt-5">
            <div className="mb-2 text-[12px] font-medium text-muted">Most active topics</div>
            <div className="flex flex-wrap gap-2">
              {highlights.most_active_topics.map((topic: string) => (
                <span key={topic} className="rounded-full bg-canvas px-3 py-1 text-[12px] font-medium text-ink">
                  {topic}
                </span>
              ))}
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader title="AI Insights" action={<Link href="/risks" className="text-[12.5px] font-medium text-muted hover:text-ink">View all</Link>} />
          <div className="space-y-4">
            {insights.map((insight: any) => (
              <div key={insight.id} className="flex items-start gap-3">
                <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-warn-bg text-warn-text">
                  {insight.type === "risk" && <AlertTriangle className="h-4 w-4" />}
                  {insight.type === "blocker" && <ShieldAlert className="h-4 w-4" />}
                  {insight.type === "knowledge" && <MessageCircle className="h-4 w-4" />}
                </span>
                <div>
                  <p className="text-[13px] leading-snug">{insight.text}</p>
                  <Link href={`/${insight.link}`} className="mt-0.5 inline-flex items-center gap-1 text-[12px] font-medium text-sage-600 hover:underline">
                    {insight.link === "risks" ? "View projects" : insight.link === "dependency-graph" ? "See details" : "View conversation"}
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <CardHeader title="Top Experts" action={<Link href="/experts" className="text-[12.5px] font-medium text-muted hover:text-ink">View All</Link>} />
          <div className="space-y-4">
            {experts.map((e: any) => (
              <div key={e.id} className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-full bg-sage-100 text-[12px] font-semibold text-sage-700">
                    {e.name.split(" ").map((n: string) => n[0]).join("")}
                  </div>
                  <div>
                    <div className="text-[13.5px] font-medium leading-tight">{e.name}</div>
                    <div className="text-[12px] text-muted">{e.role}</div>
                  </div>
                </div>
                <Badge tone="ok">{e.contribution_score}</Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

function HighlightStat({ icon, label, value, delta }: { icon: React.ReactNode; label: string; value: number; delta: string }) {
  return (
    <div>
      <div className="flex items-center gap-2 text-[12px] text-muted">{label}</div>
      <div className="mt-1 text-[20px] font-semibold">{value.toLocaleString()}</div>
      <div className="mt-1 flex items-center gap-1.5 text-[11.5px] text-muted">
        {icon}
        {delta}
      </div>
    </div>
  );
}
