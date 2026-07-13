# OrgPulse AI - Frontend

Next.js 15 (App Router) + TypeScript + Tailwind CSS. Matches the reference
dashboard layout: sidebar navigation, stat cards, dependency risk overview,
knowledge graph highlights, AI insights, and top experts.

## Run

```bash
npm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_BASE_URL
npm run dev
```

Visits to any page work even without the backend running - every request in
`src/lib/api.ts` falls back to the bundled fixtures in `src/lib/fixtures`.

## Pages

`/dashboard`, `/knowledge-graph`, `/dependency-graph`, `/projects`,
`/decisions`, `/experts`, `/risks`, `/releases`, `/timeline`, `/analytics`,
`/integrations`, `/ai-chat`, `/settings`.

## Notable components

- `DependencyGraphExplorer.tsx` / `KnowledgeGraphExplorer.tsx` - React Flow
  canvases with zoom, pan, search/filter.
- `AnalyticsCharts.tsx` - Recharts bar/pie charts.
- `DependencyRiskOverview.tsx` - the mini blocker-chain visual on the
  dashboard, mirroring the reference design.
