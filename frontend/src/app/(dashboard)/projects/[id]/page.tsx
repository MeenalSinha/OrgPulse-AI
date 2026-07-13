import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { Badge, statusTone } from "@/components/Badge";
import { api } from "@/lib/api";

export default async function ProjectDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const BASE_URL = process.env.API_BASE_URL_SERVER || "http://backend:8000";
  let data: any = null;
  try {
    const res = await fetch(`${BASE_URL}/api/projects/${id}`, { cache: "no-store" });
    if (res.ok) data = await res.json();
  } catch {}

  if (!data) {
    return (
      <div>
        <Topbar greetingName="Carl" subtitle="Project detail" />
        <div className="mt-8 px-8">
          <Card>Project data is unavailable offline. Start the backend to view project detail.</Card>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Topbar greetingName="Carl" subtitle={data.project.name} />
      <div className="mt-8 grid grid-cols-1 gap-5 px-8 xl:grid-cols-2">
        <Card>
          <CardHeader title="Releases" />
          <div className="space-y-3">
            {data.releases.map((r: any) => (
              <div key={r.id} className="flex items-center justify-between">
                <div className="text-[13.5px] font-medium">{r.name}</div>
                <Badge tone={statusTone(r.status)}>{r.status}</Badge>
              </div>
            ))}
            {data.releases.length === 0 && <p className="text-[13px] text-muted">No releases linked yet.</p>}
          </div>
        </Card>
        <Card>
          <CardHeader title="Open Tickets" />
          <div className="space-y-3">
            {data.open_tickets.map((t: any) => (
              <div key={t.id} className="flex items-center justify-between">
                <div className="text-[13.5px] font-medium">{t.title}</div>
                <Badge tone={statusTone(t.priority)}>{t.priority}</Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
