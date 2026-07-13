import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { Badge, statusTone } from "@/components/Badge";
import { api } from "@/lib/api";
import { AlertTriangle, Server, Cog, Folder, Users, Box } from "lucide-react";

function TypeIcon({ type, className }: { type: string, className?: string }) {
  switch (type) {
    case "service": return <Server className={className} />;
    case "process": return <Cog className={className} />;
    case "project": return <Folder className={className} />;
    case "team": return <Users className={className} />;
    default: return <Box className={className} />;
  }
}

function heatColor(score: number) {
  if (score >= 60) return "bg-[#C0392B]";
  if (score >= 35) return "bg-[#E08B5A]";
  if (score >= 15) return "bg-[#D9B65A]";
  return "bg-ok-text";
}

export default async function RisksPage() {
  const [risks, bottlenecks] = await Promise.all([api.risks(), api.bottlenecks()]);

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Predicted risks and the bottlenecks driving them." />
      <div className="mt-8 px-8">
        <Card className="mb-5">
          <CardHeader title="Risk Heatmap" />
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
            {bottlenecks.map((b: any) => (
              <div key={b.id} className="flex flex-col items-center gap-2 rounded-xl border border-line p-3">
                <div className={`flex h-10 w-10 items-center justify-center rounded-lg text-white ${heatColor(b.risk_score)}`} title={`Risk score ${b.risk_score}`}>
                  <TypeIcon type={b.type} className="h-5 w-5 opacity-90" />
                </div>
                <div className="text-center text-[11.5px] font-medium leading-tight">{b.label}</div>
                <div className="text-[11px] text-muted">{b.risk_score}/100</div>
              </div>
            ))}
          </div>
        </Card>

        <div className="grid grid-cols-1 gap-5 xl:grid-cols-3">
          <div className="space-y-4 xl:col-span-2">
            {risks.map((r: any) => (
              <Card key={r.id}>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3">
                    <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-danger-bg text-danger-text">
                      <AlertTriangle className="h-4 w-4" />
                    </span>
                    <div>
                      <div className="text-[14px] font-semibold">{r.title}</div>
                      <p className="mt-1 text-[13px] text-muted">{r.root_cause}</p>
                      <p className="mt-2 text-[13px]"><span className="font-semibold">Recommendation:</span> {r.recommendation}</p>
                    </div>
                  </div>
                  <Badge tone={statusTone(r.severity)}>{r.probability}%</Badge>
                </div>
              </Card>
            ))}
          </div>
          <Card>
            <CardHeader title="Top Bottlenecks" />
            <div className="space-y-3">
              {bottlenecks.map((b: any) => (
                <div key={b.id} className="flex items-center justify-between">
                  <div className="text-[13px] font-medium">{b.label}</div>
                  <Badge tone={b.risk_score > 50 ? "danger" : b.risk_score > 25 ? "warn" : "ok"}>{b.risk_score}</Badge>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
