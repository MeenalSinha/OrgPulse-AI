import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import fixtures from "@/lib/fixtureIndex";

const STATS = [
  { label: "Teams", key: "teams" as const },
  { label: "Employees", key: "employees" as const },
  { label: "Repositories", key: "repos" as const },
  { label: "Pull Requests", key: "pullRequests" as const },
  { label: "Tickets", key: "tickets" as const },
  { label: "Architecture Docs", key: "docs" as const },
  { label: "Slack Conversations", key: "conversations" as const },
  { label: "Decisions", key: "decisions" as const },
  { label: "Incidents", key: "incidents" as const },
  { label: "Releases", key: "releases" as const },
];

export default function DemoDataPage() {
  return (
    <div>
      <Topbar greetingName="Carl" subtitle="The synthetic dataset powering every page in this workspace." />
      <div className="mt-8 px-8">
        <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
          {STATS.map((s) => (
            <Card key={s.key}>
              <div className="text-[12px] text-muted">{s.label}</div>
              <div className="mt-1 text-[22px] font-semibold">
                {(fixtures[s.key] as unknown[]).length}
              </div>
            </Card>
          ))}
        </div>

        <Card className="mt-5">
          <h3 className="text-[15px] font-semibold">Regenerate the dataset</h3>
          <p className="mt-2 text-[13.5px] leading-relaxed text-muted">
            Run the generator to reshuffle names, dependency statuses, and decisions with a new random
            seed. The intentional demo blocker chain (Security Review blocks Payments API blocks
            Backend Core blocks Mobile App) is always preserved.
          </p>
          <pre className="mt-4 overflow-x-auto rounded-xl bg-ink p-4 text-[12.5px] text-white">
            <code>python3 data/generate_mock_data.py</code>
          </pre>
        </Card>
      </div>
    </div>
  );
}
