import clsx from "clsx";

const TONES: Record<string, string> = {
  danger: "bg-danger-bg text-danger-text",
  warn: "bg-warn-bg text-warn-text",
  ok: "bg-ok-bg text-ok-text",
  neutral: "bg-canvas text-muted",
};

export function Badge({ tone = "neutral", children }: { tone?: keyof typeof TONES; children: React.ReactNode }) {
  return (
    <span className={clsx("inline-flex items-center rounded-full px-2.5 py-1 text-[11.5px] font-semibold", TONES[tone])}>
      {children}
    </span>
  );
}

export function statusTone(status: string): keyof typeof TONES {
  const s = status.toLowerCase();
  if (["blocked", "at risk", "at_risk", "delayed", "high", "critical"].includes(s)) return "danger";
  if (["medium", "review", "in progress"].includes(s)) return "warn";
  if (["on track", "on_track", "shipped", "done", "low", "adopted"].includes(s)) return "ok";
  return "neutral";
}
