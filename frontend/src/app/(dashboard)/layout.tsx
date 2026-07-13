import { Sidebar } from "@/components/Sidebar";

export const dynamic = "force-dynamic";

export default function DashboardShellLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-canvas dark:bg-[#14170F]">
      <Sidebar />
      <main className="flex-1 pb-12">{children}</main>
    </div>
  );
}
