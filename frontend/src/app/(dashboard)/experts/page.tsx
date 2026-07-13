"use client";

import { useEffect, useState } from "react";
import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { Badge } from "@/components/Badge";
import { Search } from "lucide-react";
import { api } from "@/lib/api";
import { CardSkeleton } from "@/components/Skeleton";
import { EmptyState } from "@/components/EmptyState";
import { Users } from "lucide-react";

export default function ExpertsPage() {
  const [topic, setTopic] = useState("");
  const [results, setResults] = useState<any[] | null>(null);
  const [defaultExperts, setDefaultExperts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.experts().then(setDefaultExperts);
  }, []);

  async function runSearch(q: string) {
    setTopic(q);
    if (!q.trim()) {
      setResults(null);
      return;
    }
    setLoading(true);
    const r = await api.searchExperts(q);
    setResults(r);
    setLoading(false);
  }

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Find who knows what, backed by PRs, docs, and incident history." />
      <div className="mt-8 px-8">
        <div className="focus-ring mb-6 flex max-w-md items-center gap-2 rounded-full border border-line bg-white px-4 py-2.5">
          <Search className="h-4 w-4 text-muted" />
          <input
            value={topic}
            onChange={(e) => runSearch(e.target.value)}
            placeholder="Who knows Kubernetes? Try: Payments API, Security..."
            className="w-full bg-transparent text-[13px] outline-none placeholder:text-muted"
          />
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {loading && Array.from({ length: 6 }).map((_, i) => <CardSkeleton key={i} />)}
          {!loading && (results ?? defaultExperts.map((e: any) => ({ employee: e, confidence_score: e.contribution_score, pr_count: null, incident_count: null }))).map((r: any) => (
            <Card key={r.employee.id}>
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-sage-100 text-[13px] font-semibold text-sage-700">
                  {r.employee.name.split(" ").map((n: string) => n[0]).join("")}
                </div>
                <div className="min-w-0">
                  <div className="truncate text-[14px] font-semibold">{r.employee.name}</div>
                  <div className="truncate text-[12.5px] text-muted">{r.employee.role} &middot; {r.employee.team_name}</div>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between">
                <div className="flex flex-wrap gap-1.5">
                  {r.employee.expertise.slice(0, 2).map((ex: string) => (
                    <span key={ex} className="rounded-full bg-canvas px-2 py-0.5 text-[11px] font-medium">{ex}</span>
                  ))}
                </div>
                <Badge tone="ok">{r.confidence_score}%</Badge>
              </div>
            </Card>
          ))}
        </div>
        {results !== null && results.length === 0 && !loading && (
          <div className="mt-4">
            <EmptyState
              icon={<Users className="h-5 w-5" />}
              title={`No strong matches for "${topic}"`}
              description="Try a broader term like a service name (Payments API) or a technology (Kubernetes)."
            />
          </div>
        )}
      </div>
    </div>
  );
}
