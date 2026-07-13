"use client";

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from "recharts";
import { Card, CardHeader } from "@/components/Card";

const COLORS = ["#3E5B45", "#6B8F76", "#B7791F", "#C0392B", "#2F6B8A"];

export function AnalyticsChartsInner({
  velocity, prThroughput, incidentTrend,
}: { velocity: any[]; prThroughput: any[]; incidentTrend: any[] }) {
  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      <Card className="xl:col-span-2">
        <CardHeader title="Team Health Score" />
        <div className="w-full overflow-x-auto" style={{ height: 280 }}>
            <BarChart width={800} height={280} data={velocity}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E6E8E3" vertical={false} />
              <XAxis dataKey="team" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip contentStyle={{ borderRadius: 10, border: "1px solid #E6E8E3", fontSize: 12 }} />
              <Bar dataKey="health_score" fill="#3E5B45" radius={[6, 6, 0, 0]} />
            </BarChart>
        </div>
      </Card>

      <Card>
        <CardHeader title="PR Throughput" />
        <div className="flex items-center justify-center w-full" style={{ height: 260 }}>
            <PieChart width={400} height={260}>
              <Pie data={prThroughput} dataKey="count" nameKey="status" innerRadius={50} outerRadius={90} paddingAngle={2}>
                {prThroughput.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Tooltip contentStyle={{ borderRadius: 10, border: "1px solid #E6E8E3", fontSize: 12 }} />
            </PieChart>
        </div>
      </Card>

      <Card>
        <CardHeader title="Incident Severity Trend" />
        <div className="flex items-center justify-center w-full" style={{ height: 260 }}>
            <PieChart width={400} height={260}>
              <Pie data={incidentTrend} dataKey="count" nameKey="severity" innerRadius={50} outerRadius={90} paddingAngle={2}>
                {incidentTrend.map((_, i) => <Cell key={i} fill={COLORS[(i + 2) % COLORS.length]} />)}
              </Pie>
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Tooltip contentStyle={{ borderRadius: 10, border: "1px solid #E6E8E3", fontSize: 12 }} />
            </PieChart>
        </div>
      </Card>
    </div>
  );
}
