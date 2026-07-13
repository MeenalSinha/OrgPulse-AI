import Link from "next/link";
import {
  Share2, GitBranch, ShieldAlert, Scale, Users, ArrowRight, Sparkles,
} from "lucide-react";
import { Card } from "@/components/Card";

const CAPABILITIES = [
  {
    icon: Share2,
    title: "Organizational Memory",
    body: "Ask why a decision was made and get a cited answer reconstructed from PRs, docs, Slack threads, and tickets - never a guess.",
  },
  {
    icon: GitBranch,
    title: "Cross-Team Dependency Graph",
    body: "OrgPulse continuously maps what blocks what across projects, services, and teams, and predicts risk propagation before it hits a deadline.",
  },
  {
    icon: ShieldAlert,
    title: "Predictive Risk Engine",
    body: "Delay probabilities, bottleneck detection, and knowledge silo alerts, posted proactively in Slack before anyone has to ask.",
  },
  {
    icon: Scale,
    title: "Decision Provenance",
    body: "Every architecture and product decision keeps its timeline, alternatives considered, participants, and evidence.",
  },
  {
    icon: Users,
    title: "Expert Discovery",
    body: "Find who actually knows a system, ranked by real PR history, incident participation, and code ownership - not who talks the most.",
  },
  {
    icon: Sparkles,
    title: "Slack-Native AI",
    body: "@mention OrgPulse or run /orgpulse for rich, cited, thread-friendly Block Kit answers, right where engineering already works.",
  },
];

export default function LandingPage() {
  return (
    <main>
      <section className="mx-auto max-w-5xl px-6 pb-16 pt-20 text-center">
        <span className="inline-flex items-center gap-2 rounded-full border border-line bg-white px-4 py-1.5 text-[12.5px] font-medium text-muted">
          <Sparkles className="h-3.5 w-3.5 text-sage-600" /> The Organizational Intelligence Graph
        </span>
        <h1 className="mx-auto mt-6 max-w-3xl text-[42px] font-semibold leading-tight tracking-tight md:text-[52px]">
          The AI that remembers your company and prevents delays before they happen.
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-[15.5px] leading-relaxed text-muted">
          OrgPulse builds a living graph of your people, teams, services, decisions, and dependencies -
          then reasons over relationships instead of keyword search, right inside Slack.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/dashboard"
            className="focus-ring flex items-center gap-2 rounded-full bg-ink px-6 py-3 text-[14px] font-semibold text-white hover:bg-sage-700"
          >
            Open Demo Workspace <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/features"
            className="focus-ring rounded-full border border-line bg-white px-6 py-3 text-[14px] font-semibold text-ink hover:bg-canvas"
          >
            See Features
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {CAPABILITIES.map((c) => {
            const Icon = c.icon;
            return (
              <Card key={c.title}>
                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-sage-50 text-sage-700">
                  <Icon className="h-4.5 w-4.5" />
                </span>
                <h3 className="mt-4 text-[15px] font-semibold">{c.title}</h3>
                <p className="mt-2 text-[13.5px] leading-relaxed text-muted">{c.body}</p>
              </Card>
            );
          })}
        </div>
      </section>

      <section className="mx-auto max-w-4xl px-6 pb-24">
        <Card className="bg-sage-700 text-white">
          <div className="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
            <div>
              <h3 className="text-[18px] font-semibold">See the scripted demo scenario</h3>
              <p className="mt-1 text-[13.5px] text-white/80">
                A security review blocks Payments API, which blocks Backend, which blocks Mobile -
                watch OrgPulse predict, explain, and recommend a fix.
              </p>
            </div>
            <Link
              href="/dependency-graph"
              className="focus-ring shrink-0 rounded-full bg-white px-5 py-2.5 text-[13.5px] font-semibold text-sage-700 hover:bg-canvas"
            >
              View Dependency Graph
            </Link>
          </div>
        </Card>
      </section>
    </main>
  );
}
