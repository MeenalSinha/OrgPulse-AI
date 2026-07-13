"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import {
  LayoutGrid, Share2, GitBranch, FolderKanban, Scale, Users, ShieldAlert,
  Rocket, LineChart, Plug, Settings, History, Slack, Database, Sparkles, Sun
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutGrid },
  { href: "/ai-chat", label: "AI Chat", icon: Sparkles },
  { href: "/knowledge-graph", label: "Knowledge Graph", icon: Share2 },
  { href: "/dependency-graph", label: "Dependency Graph", icon: GitBranch },
  { href: "/projects", label: "Projects", icon: FolderKanban },
  { href: "/decisions", label: "Decisions", icon: Scale },
  { href: "/experts", label: "Experts", icon: Users },
  { href: "/risks", label: "Risks & Alerts", icon: ShieldAlert },
  { href: "/releases", label: "Releases", icon: Rocket },
  { href: "/timeline", label: "Timeline", icon: History },
  { href: "/analytics", label: "Analytics", icon: LineChart },
  { href: "/integrations", label: "Integrations", icon: Plug },
  { href: "/slack-config", label: "Slack App", icon: Slack },
  { href: "/demo-data", label: "Demo Data", icon: Database },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:flex w-[260px] shrink-0 flex-col bg-white dark:bg-[#1E221D] border-r border-line/50">
      <Link href="/" className="focus-ring flex items-center gap-3 px-8 py-8">
        <Sparkles className="h-7 w-7 text-[#5C7C65]" fill="currentColor" strokeWidth={1} />
        <span className="text-[17px] font-semibold tracking-tight text-ink dark:text-white">OrgPulse AI</span>
      </Link>

      <nav className="flex-1 space-y-1.5 px-5">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href || pathname?.startsWith(item.href + "/");
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "focus-ring flex items-center gap-3.5 rounded-2xl px-4 py-3.5 text-[14px] transition-colors",
                active
                  ? "bg-ink text-white font-medium shadow-md shadow-ink/10 dark:bg-white/10 dark:text-white"
                  : "text-muted hover:bg-canvas hover:text-ink font-medium dark:hover:bg-white/5 dark:hover:text-white"
              )}
            >
              <Icon className="h-4 w-4" strokeWidth={2} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="mx-5 mb-8 flex items-center gap-3 rounded-2xl px-2 py-2 hover:bg-canvas cursor-pointer transition-colors">
        <div className="h-10 w-10 overflow-hidden rounded-full border border-line/50">
          <img src="https://ui-avatars.com/api/?name=Carl+Brown&background=random&color=fff" alt="Carl Brown" className="h-full w-full object-cover" />
        </div>
        <div className="min-w-0">
          <div className="truncate text-[14px] font-medium text-ink">Carl Brown</div>
          <div className="truncate text-[12px] text-muted">Engineering Manager</div>
        </div>
      </div>
    </aside>
  );
}
