import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { Badge } from "@/components/Badge";

export default async function DecisionDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const BASE_URL = process.env.API_BASE_URL_SERVER || "http://backend:8000";
  let decision: any = null;
  try {
    const res = await fetch(`${BASE_URL}/api/decisions/${id}`, { cache: "no-store" });
    if (res.ok) decision = await res.json();
  } catch {}

  if (!decision) {
    return (
      <div>
        <Topbar greetingName="Carl" subtitle="Decision detail" />
        <div className="mt-8 px-8">
          <Card>Decision data is unavailable offline. Start the backend to view full provenance.</Card>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Topbar greetingName="Carl" subtitle={decision.title} />
      <div className="mt-8 grid grid-cols-1 gap-5 px-8 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader title="Rationale" action={<Badge tone="neutral">{decision.category}</Badge>} />
          <p className="text-[13.5px] leading-relaxed text-ink">{decision.rationale}</p>

          <div className="mt-6">
            <div className="mb-2 text-[12px] font-semibold text-muted">Alternatives considered</div>
            <ul className="list-disc space-y-1 pl-5 text-[13px]">
              {decision.alternatives_considered.map((a: string) => <li key={a}>{a}</li>)}
            </ul>
          </div>

          <div className="mt-6">
            <div className="mb-2 text-[12px] font-semibold text-muted">Evidence</div>
            <div className="flex flex-wrap gap-2">
              {decision.evidence.map((e: string) => (
                <span key={e} className="rounded-full bg-canvas px-3 py-1 text-[12px] font-mono">{e}</span>
              ))}
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader title="Participants" />
          <div className="space-y-3">
            {decision.participants.map((p: any) => (
              <div key={p.id} className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-sage-100 text-[12px] font-semibold text-sage-700">
                  {p.name.split(" ").map((n: string) => n[0]).join("")}
                </div>
                <div>
                  <div className="text-[13px] font-medium">{p.name}</div>
                  <div className="text-[12px] text-muted">{p.role}</div>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 text-[12px] text-muted">Decided {decision.date} &middot; {decision.outcome}</div>
        </Card>
      </div>
    </div>
  );
}
