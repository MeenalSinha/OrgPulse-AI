import Link from "next/link";
import { ArrowRight, ArrowLeftRight, AlertTriangle } from "lucide-react";
import clsx from "clsx";
import { PulseBadge } from "./Motion";

const STATUS_STYLES: Record<string, string> = {
  on_track: "border-line bg-white text-ink",
  blocked: "border-[#F3C6C2] bg-danger-bg text-danger-text",
  delayed: "border-[#F5DDA6] bg-warn-bg text-warn-text",
  at_risk: "border-[#F3C6C2] bg-danger-bg text-danger-text",
};

function Node({ label, status }: { label: string; status: string }) {
  const statusLabel: Record<string, string> = {
    on_track: "On Track",
    blocked: "Blocked",
    delayed: "Delayed",
    at_risk: "At Risk",
  };
  return (
    <div className={clsx("rounded-xl border px-4 py-2.5 text-center text-[12.5px] font-medium shadow-sm", STATUS_STYLES[status] ?? STATUS_STYLES.on_track)}>
      <div className="font-semibold text-ink">{label}</div>
      <div className={clsx("mt-0.5 text-[11px]", status === "on_track" ? "text-ok-text" : "opacity-90")}>
        {statusLabel[status] ?? "On Track"}
      </div>
    </div>
  );
}

export function DependencyRiskOverview() {
  return (
    <div>
      <div className="flex justify-center">
        <Node label="User Service" status="on_track" />
      </div>
      <div className="my-2 flex justify-center text-muted">
        <ArrowRight className="h-4 w-4 rotate-90" />
      </div>
      <div className="grid grid-cols-3 items-center gap-3">
        <Node label="Mobile App" status="at_risk" />
        <div className="flex items-center justify-center gap-2">
          <ArrowLeftRight className="h-4 w-4 text-danger-text" />
        </div>
        <Node label="Payments API" status="blocked" />
      </div>
      <div className="mt-3 grid grid-cols-3 items-center gap-3">
        <Node label="Analytics Pipeline" status="on_track" />
        <div />
        <Node label="Security Review" status="delayed" />
      </div>
      <div className="mt-3 grid grid-cols-3 items-center gap-3">
        <div />
        <div />
        <Node label="Database Migration" status="on_track" />
      </div>

      <div className="mt-5 flex items-start gap-3 rounded-xl bg-danger-bg px-4 py-3">
        <PulseBadge className="mt-0.5 flex shrink-0">
          <AlertTriangle className="h-4 w-4 text-danger-text" />
        </PulseBadge>
        <p className="flex-1 text-[13px] text-danger-text">
          Payments API is blocked by Security Review. This may delay 3 dependent projects.
        </p>
        <Link href="/dependency-graph" className="focus-ring shrink-0 rounded-lg border border-line bg-white px-3 py-1.5 text-[12.5px] font-medium text-ink hover:bg-canvas">
          See Details
        </Link>
      </div>
    </div>
  );
}
