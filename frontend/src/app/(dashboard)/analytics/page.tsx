import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { api } from "@/lib/api";
import { AnalyticsCharts } from "@/components/AnalyticsCharts";

export const dynamic = "force-dynamic";

export default async function AnalyticsPage() {
  const [velocity, prThroughput, incidentTrend] = await Promise.all([
    api.velocity(), api.prThroughput(), api.incidentTrend(),
  ]);

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Engineering velocity, PR throughput, and incident trends." />
      <div className="mt-8 px-8">
        <AnalyticsCharts velocity={velocity} prThroughput={prThroughput} incidentTrend={incidentTrend} />
      </div>
    </div>
  );
}
