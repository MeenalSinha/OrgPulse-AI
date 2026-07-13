import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { api } from "@/lib/api";
import { DependencyGraphExplorer } from "@/components/DependencyGraphExplorer";

export default async function DependencyGraphPage() {
  const [graph, criticalPath] = await Promise.all([api.dependencyGraph(), api.criticalPath()]);

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Explore how projects, services, and teams depend on each other." />
      <div className="mt-8 px-8">
        {criticalPath && (
          <Card className="mb-5 border-[#F3C6C2] bg-danger-bg">
            <div className="text-[13px] font-semibold text-danger-text">Active blocker chain</div>
            <div className="mt-1 text-[13.5px] text-danger-text">
              {criticalPath.labels.join(" -> ")} &middot; risk score {criticalPath.risk_score}/100
            </div>
          </Card>
        )}
        <Card className="p-0 overflow-hidden">
          <DependencyGraphExplorer graph={graph} />
        </Card>
      </div>
    </div>
  );
}
