import { Inbox } from "lucide-react";

export function EmptyState({
  title = "Nothing here yet",
  description,
  icon,
}: { title?: string; description?: string; icon?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-line px-6 py-12 text-center">
      <span className="flex h-11 w-11 items-center justify-center rounded-full bg-canvas text-muted">
        {icon ?? <Inbox className="h-5 w-5" />}
      </span>
      <p className="mt-3 text-[13.5px] font-medium text-ink">{title}</p>
      {description && <p className="mt-1 max-w-xs text-[12.5px] text-muted">{description}</p>}
    </div>
  );
}
