"use client";

import dynamic from "next/dynamic";

export const AnalyticsCharts = dynamic(
  () => import("./AnalyticsChartsInner").then((mod) => mod.AnalyticsChartsInner),
  { ssr: false }
);
