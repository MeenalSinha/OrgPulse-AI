import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";

export default function SettingsPage() {
  return (
    <div>
      <Topbar greetingName="Carl" subtitle="Workspace, notification, and access settings." />
      <div className="mt-8 grid grid-cols-1 gap-5 px-8 xl:grid-cols-2">
        <Card>
          <CardHeader title="Workspace" />
          <div className="space-y-4 text-[13.5px]">
            <div className="flex items-center justify-between">
              <span className="text-muted">Organization</span>
              <span className="font-medium">NeuroIgniter</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Slack workspace</span>
              <span className="font-medium">Not connected</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted">Plan</span>
              <span className="font-medium">Prototype / Demo</span>
            </div>
          </div>
        </Card>
        <Card>
          <CardHeader title="Notifications" />
          <div className="space-y-4 text-[13.5px]">
            <label className="flex items-center justify-between">
              <span>Daily intelligence digest</span>
              <input type="checkbox" defaultChecked className="h-4 w-4 accent-[#3E5B45]" />
            </label>
            <label className="flex items-center justify-between">
              <span>Dependency warnings</span>
              <input type="checkbox" defaultChecked className="h-4 w-4 accent-[#3E5B45]" />
            </label>
            <label className="flex items-center justify-between">
              <span>Release readiness alerts</span>
              <input type="checkbox" defaultChecked className="h-4 w-4 accent-[#3E5B45]" />
            </label>
          </div>
        </Card>
      </div>
    </div>
  );
}
