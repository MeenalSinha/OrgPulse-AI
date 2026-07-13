import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { Badge } from "@/components/Badge";
import { api } from "@/lib/api";
import { Plug } from "lucide-react";

const FALLBACK = [
  { id: "github", name: "GitHub", category: "code", status: "mock", mode: "mock" },
  { id: "jira", name: "Jira", category: "project_management", status: "mock", mode: "mock" },
  { id: "notion", name: "Notion", category: "documentation", status: "mock", mode: "mock" },
  { id: "confluence", name: "Confluence", category: "documentation", status: "mock", mode: "mock" },
  { id: "gdrive", name: "Google Drive", category: "documentation", status: "mock", mode: "mock" },
  { id: "slack", name: "Slack", category: "communication", status: "mock", mode: "mock" },
  { id: "calendar", name: "Google Calendar", category: "scheduling", status: "mock", mode: "mock" },
  { id: "linear", name: "Linear", category: "project_management", status: "mock", mode: "mock" },
  { id: "figma", name: "Figma", category: "design", status: "mock", mode: "mock" },
  { id: "gitlab", name: "GitLab", category: "code", status: "mock", mode: "mock" },
  { id: "azure_devops", name: "Azure DevOps", category: "project_management", status: "mock", mode: "mock" },
];

export default async function IntegrationsPage() {
  const list = await api.integrations();
  const integrations = list.length ? list : FALLBACK;

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="MCP connectors: swap any source from mock to live independently." />
      <div className="mt-8 grid grid-cols-1 gap-4 px-8 md:grid-cols-2 xl:grid-cols-3">
        {integrations.map((c: any) => (
          <Card key={c.id} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-sage-50 text-sage-700">
                <Plug className="h-4 w-4" />
              </span>
              <div>
                <div className="text-[14px] font-semibold">{c.name}</div>
                <div className="text-[12px] capitalize text-muted">{c.category.replace("_", " ")}</div>
              </div>
            </div>
            <Badge tone={c.status === "connected" ? "ok" : "neutral"}>{c.status}</Badge>
          </Card>
        ))}
      </div>
    </div>
  );
}
