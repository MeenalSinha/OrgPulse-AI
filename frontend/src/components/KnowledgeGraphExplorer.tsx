"use client";

import { useMemo, useState } from "react";
import ReactFlow, { Background, Controls, MiniMap, Node, Edge } from "reactflow";
import "reactflow/dist/style.css";
import clsx from "clsx";

const TYPE_COLORS: Record<string, string> = {
  team: "#3E5B45",
  person: "#6B7268",
  decision: "#B7791F",
  doc: "#2F6B8A",
};

const TYPES = ["team", "person", "decision", "doc"];

export function KnowledgeGraphExplorer({ graph }: { graph: { nodes: any[]; edges: any[] } }) {
  const [activeTypes, setActiveTypes] = useState<string[]>(TYPES);

  const filteredNodes = useMemo(
    () => graph.nodes.filter((n) => activeTypes.includes(n.type)),
    [graph.nodes, activeTypes]
  );
  const visibleIds = useMemo(() => new Set(filteredNodes.map((n) => n.id)), [filteredNodes]);

  const { nodes, edges } = useMemo(() => {
    const cols = 6;
    const nodes: Node[] = filteredNodes.map((n, i) => ({
      id: n.id,
      data: { label: n.label },
      position: { x: (i % cols) * 190 + 30, y: Math.floor(i / cols) * 110 + 30 },
      style: {
        border: `2px solid ${TYPE_COLORS[n.type] ?? "#E6E8E3"}`,
        borderRadius: n.type === "person" ? 999 : 10,
        padding: 8,
        fontSize: 11,
        fontWeight: 600,
        background: "#FFFFFF",
        width: 160,
        textAlign: "center" as const,
      },
    }));

    const edges: Edge[] = graph.edges
      .filter((e: any) => visibleIds.has(e.source) && visibleIds.has(e.target))
      .map((e: any, i: number) => ({
        id: `e-${i}`,
        source: e.source,
        target: e.target,
        style: { stroke: "#D9DED5" },
      }));

    return { nodes, edges };
  }, [filteredNodes, visibleIds, graph.edges]);

  return (
    <div className="relative" style={{ height: 560 }}>
      <div className="absolute left-4 top-4 z-10 flex gap-2">
        {TYPES.map((t) => (
          <button
            key={t}
            onClick={() =>
              setActiveTypes((prev) => (prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]))
            }
            className={clsx(
              "focus-ring rounded-full border px-3 py-1 text-[11.5px] font-medium capitalize shadow-sm",
              activeTypes.includes(t) ? "border-transparent text-white" : "border-line bg-white text-muted"
            )}
            style={activeTypes.includes(t) ? { backgroundColor: TYPE_COLORS[t] } : {}}
          >
            {t}
          </button>
        ))}
      </div>
      <ReactFlow nodes={nodes} edges={edges} fitView minZoom={0.2} maxZoom={1.5}>
        <Background gap={16} color="#E6E8E3" />
        <Controls />
        <MiniMap nodeColor={() => "#6B8F76"} maskColor="rgba(245,246,244,0.7)" />
      </ReactFlow>
    </div>
  );
}
