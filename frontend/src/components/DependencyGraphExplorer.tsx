"use client";

import { useMemo, useState } from "react";
import ReactFlow, {
  Background, Controls, MiniMap, Node, Edge, MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";

const STATUS_COLORS: Record<string, string> = {
  on_track: "#2F6B3A",
  blocked: "#C0392B",
  delayed: "#B7791F",
  at_risk: "#C0392B",
};

const RELATION_COLORS: Record<string, string> = {
  blocks: "#C0392B",
  depends_on: "#6B7268",
  uses: "#3E5B45",
};

export function DependencyGraphExplorer({ graph }: { graph: { nodes: any[]; edges: any[] } }) {
  const [search, setSearch] = useState("");

  const { nodes, edges } = useMemo(() => {
    const cols = 3;
    const nodes: Node[] = graph.nodes.map((n, i) => ({
      id: n.id,
      data: { label: n.label },
      position: { x: (i % cols) * 260 + 40, y: Math.floor(i / cols) * 140 + 40 },
      style: {
        border: `2px solid ${STATUS_COLORS[n.status] ?? "#E6E8E3"}`,
        borderRadius: 12,
        padding: 10,
        fontSize: 12,
        fontWeight: 600,
        background:
          search && n.label.toLowerCase().includes(search.toLowerCase())
            ? "#EEF2ED"
            : "#FFFFFF",
        opacity: search && !n.label.toLowerCase().includes(search.toLowerCase()) ? 0.35 : 1,
        width: 200,
      },
    }));

    const edges: Edge[] = graph.edges.map((e, i) => ({
      id: `e-${i}`,
      source: e.source,
      target: e.target,
      label: e.relation,
      animated: e.relation === "blocks",
      style: { stroke: RELATION_COLORS[e.relation] ?? "#6B7268" },
      markerEnd: { type: MarkerType.ArrowClosed, color: RELATION_COLORS[e.relation] ?? "#6B7268" },
      labelStyle: { fontSize: 10, fill: "#6B7268" },
    }));

    return { nodes, edges };
  }, [graph, search]);

  return (
    <div className="relative" style={{ height: 560 }}>
      <div className="absolute left-4 top-4 z-10">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Highlight a node..."
          className="focus-ring rounded-lg border border-line bg-white px-3 py-1.5 text-[12.5px] shadow-sm outline-none"
        />
      </div>
      <ReactFlow nodes={nodes} edges={edges} fitView minZoom={0.3} maxZoom={1.5}>
        <Background gap={16} color="#E6E8E3" />
        <Controls />
        <MiniMap
          nodeColor={(n) => (n.style?.border as string)?.split(" ")[2] ?? "#6B7268"}
          maskColor="rgba(245,246,244,0.7)"
        />
      </ReactFlow>
    </div>
  );
}
