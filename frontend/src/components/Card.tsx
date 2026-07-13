import clsx from "clsx";

export function Card({
  className, children,
}: { className?: string; children: React.ReactNode }) {
  return (
    <div className={clsx("rounded-3xl border border-line/60 bg-white p-6 shadow-card dark:border-white/10 dark:bg-[#1E221D]", className)}>
      {children}
    </div>
  );
}

export function CardHeader({
  title, action,
}: { title: string; action?: React.ReactNode }) {
  return (
    <div className="mb-5 flex items-center justify-between">
      <h3 className="text-[16px] font-semibold tracking-tight dark:text-white">{title}</h3>
      {action}
    </div>
  );
}
