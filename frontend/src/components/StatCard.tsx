import { Card } from "./Card";
import clsx from "clsx";

export function StatCard({
  label, value, delta, icon, tone = "default", chart
}: {
  label: string; value: string | number; delta?: string;
  icon?: React.ReactNode; tone?: "default" | "danger" | "warn" | "ok" | "dark";
  chart?: React.ReactNode;
}) {
  const isDark = tone === "dark";
  return (
    <Card
      className={clsx(
        "flex flex-col justify-between",
        isDark && "!bg-[#6B8F76] !border-[#6B8F76] text-white shadow-md shadow-[#6B8F76]/20"
      )}
    >
      <div className="flex items-start justify-between">
        <span className={clsx("text-[14px] font-medium", isDark ? "text-white/90" : "text-ink")}>
          {label}
        </span>
        {icon && (
          <span
            className={clsx(
              "flex h-10 w-10 items-center justify-center rounded-full",
              isDark ? "bg-white/20" : tone === "danger" ? "bg-danger-bg" : tone === "warn" ? "bg-warn-bg" : "bg-ok-bg"
            )}
          >
            {icon}
          </span>
        )}
      </div>
      <div className="mt-5 text-[32px] font-semibold tracking-tight">{value}</div>
      <div className="flex items-end justify-between mt-1.5">
        {delta && (
          <div className={clsx("text-[13px] font-medium", isDark ? "text-white/90" : "text-muted")}>{delta}</div>
        )}
        {chart && (
          <div className="flex-1 ml-4 h-8 flex items-end justify-end">
            {chart}
          </div>
        )}
      </div>
    </Card>
  );
}
