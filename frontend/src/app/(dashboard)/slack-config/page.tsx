import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { Badge } from "@/components/Badge";

const SCOPES = [
  "app_mentions:read", "chat:write", "commands", "channels:history", "im:history", "users:read",
];

const COMMANDS = [
  { cmd: "@OrgPulse <question>", desc: "Ask anything about your organization, answered with citations." },
  { cmd: "/orgpulse status", desc: "Posts the daily intelligence digest." },
  { cmd: "/orgpulse risks", desc: "Posts the current highest-risk blocker chain." },
  { cmd: "/orgpulse experts <topic>", desc: "Finds top experts on a topic." },
];

export default function SlackConfigPage() {
  const configured = false; // becomes true once SLACK_BOT_TOKEN / SLACK_APP_TOKEN are set server-side

  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Connect and configure the OrgPulse Slack app." />
      <div className="mt-8 grid grid-cols-1 gap-5 px-8 xl:grid-cols-2">
        <Card>
          <CardHeader title="Connection Status" action={<Badge tone={configured ? "ok" : "neutral"}>{configured ? "Connected" : "Not connected"}</Badge>} />
          <p className="text-[13.5px] leading-relaxed text-muted">
            The Slack app runs as a separate Bolt process (see <code className="rounded bg-canvas px-1.5 py-0.5 text-[12px]">slack-app/</code>).
            Set <code className="rounded bg-canvas px-1.5 py-0.5 text-[12px]">SLACK_BOT_TOKEN</code> and{" "}
            <code className="rounded bg-canvas px-1.5 py-0.5 text-[12px]">SLACK_APP_TOKEN</code> in your environment and run{" "}
            <code className="rounded bg-canvas px-1.5 py-0.5 text-[12px]">python slack-app/app.py</code>, or{" "}
            <code className="rounded bg-canvas px-1.5 py-0.5 text-[12px]">docker compose --profile slack up</code>.
          </p>
          <div className="mt-5">
            <div className="mb-2 text-[12px] font-semibold text-muted">Bot token scopes</div>
            <div className="flex flex-wrap gap-2">
              {SCOPES.map((s) => (
                <span key={s} className="rounded-full bg-canvas px-3 py-1 font-mono text-[11.5px]">{s}</span>
              ))}
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader title="Commands" />
          <div className="space-y-4">
            {COMMANDS.map((c) => (
              <div key={c.cmd}>
                <div className="font-mono text-[12.5px] font-semibold text-sage-700">{c.cmd}</div>
                <div className="text-[12.5px] text-muted">{c.desc}</div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="xl:col-span-2">
          <CardHeader title="Proactive Alerts" />
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {["Daily intelligence digest", "Dependency warnings", "Release readiness alerts"].map((f) => (
              <div key={f} className="rounded-xl border border-line p-4">
                <div className="text-[13px] font-medium">{f}</div>
                <div className="mt-1 text-[12px] text-muted">Posted via Block Kit to a configured channel on a schedule (Celery beat / cron).</div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
