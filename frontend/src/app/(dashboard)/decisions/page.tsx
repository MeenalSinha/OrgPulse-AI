import Link from "next/link";
import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { Badge } from "@/components/Badge";
import { api } from "@/lib/api";
import { Scale } from "lucide-react";

export default async function DecisionsPage() {
  const decisions = await api.decisions();

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Decision provenance: every major call, with rationale and evidence." />
      <div className="mt-8 space-y-3 px-8">
        {decisions.map((d: any) => (
          <Link key={d.id} href={`/decisions/${d.id}`}>
            <Card className="flex items-center justify-between gap-4 transition-shadow hover:shadow-md">
              <div className="flex items-center gap-3 min-w-0">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-sage-50 text-sage-700">
                  <Scale className="h-4 w-4" />
                </span>
                <div className="min-w-0">
                  <div className="truncate text-[14px] font-semibold">{d.title}</div>
                  <div className="text-[12.5px] text-muted">{d.date} &middot; {d.outcome}</div>
                </div>
              </div>
              <Badge tone="neutral">{d.category}</Badge>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
