import Link from "next/link";

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-canvas">
      <header className="sticky top-0 z-20 border-b border-line bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-sage-600">
              <span className="block h-3.5 w-3.5 rounded-full border-2 border-white border-t-transparent" />
            </div>
            <span className="text-[15px] font-semibold tracking-tight">OrgPulse AI</span>
          </Link>
          <nav className="hidden items-center gap-8 text-[13.5px] font-medium text-muted md:flex">
            <Link href="/features" className="hover:text-ink">Features</Link>
            <Link href="/dashboard" className="hover:text-ink">Demo Workspace</Link>
            <Link href="/integrations" className="hover:text-ink">Integrations</Link>
          </nav>
          <Link
            href="/dashboard"
            className="focus-ring rounded-full bg-ink px-4 py-2 text-[13px] font-semibold text-white hover:bg-sage-700"
          >
            Open Demo Workspace
          </Link>
        </div>
      </header>
      {children}
      <footer className="border-t border-line px-6 py-10 text-center text-[12.5px] text-muted">
        OrgPulse AI - built for the Slack Hack / Devpost competition. All data on this site is synthetic demo data.
      </footer>
    </div>
  );
}
