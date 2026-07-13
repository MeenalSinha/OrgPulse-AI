import Link from "next/link";
import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { api } from "@/lib/api";
import { FolderKanban, ArrowRight } from "lucide-react";

export default async function ProjectsPage() {
  const projects = await api.projects();

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Every project the organization is currently tracking." />
      <div className="mt-8 grid grid-cols-1 gap-5 px-8 md:grid-cols-2 xl:grid-cols-3">
        {projects.map((p: any) => (
          <Link key={p.id} href={`/projects/${p.id}`}>
            <Card className="h-full transition-shadow hover:shadow-md">
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-sage-50 text-sage-700">
                  <FolderKanban className="h-4.5 w-4.5" />
                </span>
                <div className="text-[14.5px] font-semibold">{p.name}</div>
              </div>
              <div className="mt-4 flex items-center gap-1 text-[12.5px] font-medium text-sage-600">
                View project <ArrowRight className="h-3.5 w-3.5" />
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
