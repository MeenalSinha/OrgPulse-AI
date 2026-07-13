"use client";

import { motion } from "framer-motion";
import { ArrowDown, ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";
import clsx from "clsx";

type Expert = { name: string; role: string; team_name: string; confidence_score: number };

export type ReleaseReadiness = {
  verdict: "Yes" | "No" | "At Risk";
  release_name: string;
  release_status: string;
  probability: number;
  chain: string[];
  risk_score: number;
  explanation: string;
  recommendation: string;
  recommended_expert: Expert | null;
};

const VERDICT_STYLE = {
  No: { color: "#C0392B", bg: "bg-danger-bg", text: "text-danger-text", Icon: ShieldX },
  "At Risk": { color: "#B7791F", bg: "bg-warn-bg", text: "text-warn-text", Icon: ShieldAlert },
  Yes: { color: "#2F6B3A", bg: "bg-ok-bg", text: "text-ok-text", Icon: ShieldCheck },
} as const;

export function ReleaseReadinessCard({ data }: { data: ReleaseReadiness }) {
  const style = VERDICT_STYLE[data.verdict];
  const Icon = style.Icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="overflow-hidden rounded-2xl border border-line bg-white shadow-card"
    >
      <div className={clsx("flex items-center gap-3 px-5 py-4", style.bg)}>
        <motion.span
          initial={{ scale: 0.6, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.1, type: "spring", stiffness: 300, damping: 20 }}
          className={clsx("flex h-10 w-10 items-center justify-center rounded-full bg-white", style.text)}
        >
          <Icon className="h-5 w-5" />
        </motion.span>
        <div>
          <div className={clsx("text-[22px] font-bold leading-none", style.text)}>{data.verdict}</div>
          <div className="mt-1 text-[12.5px] text-muted">{data.release_name}</div>
        </div>
        <div className="ml-auto text-right">
          <div className={clsx("text-[20px] font-semibold", style.text)}>{data.probability}%</div>
          <div className="text-[11px] text-muted">delay probability</div>
        </div>
      </div>

      {data.chain.length > 0 && (
        <div className="flex flex-col items-center gap-1 px-5 py-5">
          {data.chain.map((node, i) => (
            <motion.div
              key={node}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15 + i * 0.08 }}
              className="flex flex-col items-center"
            >
              <div
                className={clsx(
                  "rounded-xl border px-4 py-2 text-[13px] font-semibold",
                  i === 0 ? "border-[#F3C6C2] bg-danger-bg text-danger-text" : "border-line bg-canvas text-ink"
                )}
              >
                {node}
              </div>
              {i < data.chain.length - 1 && (
                <ArrowDown className="my-1 h-4 w-4 text-muted" strokeWidth={2.5} />
              )}
            </motion.div>
          ))}
        </div>
      )}

      <div className="space-y-3 border-t border-line px-5 py-4">
        <div>
          <div className="text-[11px] font-semibold uppercase tracking-wide text-muted">Why</div>
          <p className="mt-1 text-[13px] leading-relaxed text-ink">{data.explanation}</p>
        </div>
        <div>
          <div className="text-[11px] font-semibold uppercase tracking-wide text-muted">Mitigation</div>
          <p className="mt-1 text-[13px] leading-relaxed text-ink">{data.recommendation}</p>
        </div>
        {data.recommended_expert && (
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-wide text-muted">Recommended expert</div>
            <div className="mt-1.5 flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-sage-100 text-[11px] font-semibold text-sage-700">
                {data.recommended_expert.name.split(" ").map((n) => n[0]).join("")}
              </div>
              <div className="text-[13px]">
                <span className="font-medium">{data.recommended_expert.name}</span>
                <span className="text-muted"> - {data.recommended_expert.role}, {data.recommended_expert.team_name}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}
