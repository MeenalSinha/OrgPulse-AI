import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { Badge, statusTone } from "@/components/Badge";
import { api } from "@/lib/api";
import { Rocket } from "lucide-react";

export default async function ReleasesPage() {
  const releases = await api.releases();
  const sorted = [...releases].sort((a: any, b: any) => (a.date < b.date ? 1 : -1));

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Release readiness across the organization." />
      <div className="mt-8 space-y-3 px-8">
        {sorted.map((r: any) => (
          <Card key={r.id} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-sage-50 text-sage-700">
                <Rocket className="h-4 w-4" />
              </span>
              <div>
                <div className="text-[14px] font-semibold">{r.name}</div>
                <div className="text-[12.5px] text-muted">{r.project} &middot; {r.date}</div>
              </div>
            </div>
            <Badge tone={statusTone(r.status)}>{r.status}</Badge>
          </Card>
        ))}
      </div>
    </div>
  );
}
