import Link from "next/link";
import { Card, CardHeader } from "@/components/Card";
import { ArrowRight } from "lucide-react";

const SECTIONS = [
  {
    title: "Organizational Memory Graph",
    href: "/ai-chat",
    points: [
      "Ask why a migration, removal, or architecture choice happened",
      "Every answer reconstructs timeline, participants, tradeoffs, and evidence",
      "Citations point to real PRs, Slack threads, docs, and tickets - never fabricated",
    ],
  },
  {
    title: "Cross-Team Dependency Graph",
    href: "/dependency-graph",
    points: [
      "Continuously mapped depends-on / blocks / uses / owns relationships",
      "Blocker chain detection and downstream impact analysis",
      "Interactive zoom, pan, search, and filter",
    ],
  },
  {
    title: "Predictive Risk Engine",
    href: "/risks",
    points: [
      "Release delay probability grounded in live dependency risk",
      "Bottleneck ranking across services, teams, and processes",
      "Knowledge silo and approval bottleneck detection",
    ],
  },
  {
    title: "Decision Provenance",
    href: "/decisions",
    points: [
      "Full timeline: alternatives considered, participants, outcome",
      "60 real decision records spanning architecture, process, and product",
    ],
  },
  {
    title: "Expert Discovery",
    href: "/experts",
    points: [
      "Ranked by expertise tags, PR history, and incident participation",
      "Confidence score shown for every match",
    ],
  },
  {
    title: "Organizational Timeline",
    href: "/timeline",
    points: [
      "Decisions, releases, and incidents merged into one chronological feed",
    ],
  },
  {
    title: "Project Health & Analytics",
    href: "/analytics",
    points: [
      "Team health scores, PR throughput, incident severity trends",
    ],
  },
  {
    title: "MCP Integrations",
    href: "/integrations",
    points: [
      "11 connectors behind a common interface: GitHub, GitLab, Jira, Linear, Azure DevOps, Notion, Confluence, Google Drive, Slack, Google Calendar, Figma",
      "Each one independently swappable from mock to live",
    ],
  },
  {
    title: "Slack-Native Experience",
    href: "/slack-config",
    points: [
      "@mentions, /orgpulse slash command, App Home tab",
      "Proactive daily digest, risk alerts, and expert lookups via Block Kit",
    ],
  },
];

export default function FeaturesPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <h1 className="text-[32px] font-semibold tracking-tight">Everything OrgPulse does</h1>
      <p className="mt-3 max-w-2xl text-[14.5px] text-muted">
        Two graphs - organizational memory and cross-team dependencies - power every feature below.
      </p>

      <div className="mt-10 grid grid-cols-1 gap-5 md:grid-cols-2">
        {SECTIONS.map((s) => (
          <Card key={s.title}>
            <CardHeader
              title={s.title}
              action={
                <Link href={s.href} className="flex items-center gap-1 text-[12.5px] font-medium text-sage-600 hover:underline">
                  Try it <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              }
            />
            <ul className="list-disc space-y-1.5 pl-5 text-[13px] leading-relaxed text-ink">
              {s.points.map((p) => <li key={p}>{p}</li>)}
            </ul>
          </Card>
        ))}
      </div>
    </main>
  );
}
