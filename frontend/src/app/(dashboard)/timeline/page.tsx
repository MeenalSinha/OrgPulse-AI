import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { Badge } from "@/components/Badge";
import { api } from "@/lib/api";

const TYPE_TONE: Record<string, "ok" | "warn" | "danger"> = {
  decision: "ok",
  release: "warn",
  incident: "danger",
};

export default async function TimelinePage() {
  const events = await api.timeline();

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="The organizational timeline: decisions, releases, and incidents in order." />
      <div className="mt-8 px-8">
        <Card>
          <div className="space-y-5">
            {events.map((e: any, i: number) => (
              <div key={i} className="flex items-start gap-4">
                <div className="w-24 shrink-0 pt-0.5 text-[12px] text-muted">{e.date}</div>
                <div className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-sage-600" />
                <div className="flex-1">
                  <div className="text-[13.5px] font-medium">{e.title}</div>
                </div>
                <Badge tone={TYPE_TONE[e.type] ?? "neutral"}>{e.type}</Badge>
              </div>
            ))}
            {events.length === 0 && <p className="text-[13px] text-muted">Start the backend to load the organizational timeline.</p>}
          </div>
        </Card>
      </div>
    </div>
  );
}
