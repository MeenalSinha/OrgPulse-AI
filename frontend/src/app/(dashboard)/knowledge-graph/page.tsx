import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { api } from "@/lib/api";
import { KnowledgeGraphExplorer } from "@/components/KnowledgeGraphExplorer";

export default async function KnowledgeGraphPage() {
  const [graph, highlights] = await Promise.all([api.knowledgeGraph(), api.knowledgeHighlights()]);

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="The organizational memory graph: people, teams, decisions, and documents, connected." />
      <div className="mt-8 grid grid-cols-1 gap-5 px-8 md:grid-cols-4">
        {[
          ["Documents", highlights.documents],
          ["Conversations", highlights.conversations],
          ["Decisions", highlights.decisions],
          ["People", highlights.people],
        ].map(([label, value]) => (
          <Card key={label as string}>
            <div className="text-[12.5px] text-muted">{label}</div>
            <div className="mt-1 text-[22px] font-semibold">{(value as number).toLocaleString()}</div>
          </Card>
        ))}
      </div>
      <div className="mt-5 px-8">
        <Card className="p-0 overflow-hidden">
          <KnowledgeGraphExplorer graph={graph} />
        </Card>
      </div>
    </div>
  );
}
