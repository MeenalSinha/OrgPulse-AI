"use client";

import { useState } from "react";
import { Topbar } from "@/components/Topbar";
import { Card, CardHeader } from "@/components/Card";
import { Badge } from "@/components/Badge";
import {
  Plug, ChevronDown, ChevronRight, Terminal,
  Zap, CheckCircle2, Circle, Loader2, Server
} from "lucide-react";

// Static connector list (backend fills in live status when running)
const CONNECTORS = [
  { id: "github", name: "GitHub", category: "code", icon: "🐙" },
  { id: "jira", name: "Jira", category: "project_management", icon: "🔷" },
  { id: "notion", name: "Notion", category: "documentation", icon: "📋" },
  { id: "confluence", name: "Confluence", category: "documentation", icon: "📚" },
  { id: "gdrive", name: "Google Drive", category: "documentation", icon: "📁" },
  { id: "slack", name: "Slack", category: "communication", icon: "💬" },
  { id: "calendar", name: "Google Calendar", category: "scheduling", icon: "📅" },
  { id: "linear", name: "Linear", category: "project_management", icon: "📐" },
  { id: "figma", name: "Figma", category: "design", icon: "🎨" },
  { id: "gitlab", name: "GitLab", category: "code", icon: "🦊" },
  { id: "azure_devops", name: "Azure DevOps", category: "project_management", icon: "🔵" },
];

interface McpTool {
  name: string;
  description: string;
  input_schema: Record<string, unknown>;
}

interface ToolsResponse {
  connector: string;
  mode: string;
  mcp_protocol: string;
  note?: string;
  tools: McpTool[];
}

interface CallResult {
  type: string;
  text: string;
}

export default function IntegrationsPage() {
  const [selectedConnector, setSelectedConnector] = useState<string | null>(null);
  const [toolsData, setToolsData] = useState<ToolsResponse | null>(null);
  const [loadingTools, setLoadingTools] = useState(false);
  const [selectedTool, setSelectedTool] = useState<McpTool | null>(null);
  const [toolArgs, setToolArgs] = useState("{}");
  const [callResult, setCallResult] = useState<CallResult[] | null>(null);
  const [callingTool, setCallingTool] = useState(false);

  const BASE = typeof window !== "undefined"
    ? (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000")
    : "http://backend:8000";

  async function loadTools(connectorId: string) {
    setSelectedConnector(connectorId);
    setToolsData(null);
    setSelectedTool(null);
    setCallResult(null);
    setLoadingTools(true);
    try {
      const res = await fetch(`${BASE}/api/integrations/${connectorId}/tools`);
      const data = await res.json();
      setToolsData(data);
    } catch {
      setToolsData({ connector: connectorId, mode: "error", mcp_protocol: "-", tools: [] });
    }
    setLoadingTools(false);
  }

  async function callTool() {
    if (!selectedConnector || !selectedTool) return;
    setCallingTool(true);
    setCallResult(null);
    try {
      let args = {};
      try { args = JSON.parse(toolArgs); } catch { /* invalid json, send empty */ }
      const res = await fetch(`${BASE}/api/integrations/${selectedConnector}/call`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool_name: selectedTool.name, arguments: args }),
      });
      const data = await res.json();
      setCallResult(data.result || []);
    } catch {
      setCallResult([{ type: "text", text: "Failed to reach backend." }]);
    }
    setCallingTool(false);
  }

  return (
    <div>
      <Topbar
        greetingName="Carl"
        subtitle="MCP (Model Context Protocol) connectors — discover tools and invoke them live."
      />

      {/* MCP Architecture Badge */}
      <div className="mx-8 mt-6 flex items-center gap-3 rounded-3xl border border-sage-100 bg-sage-50 px-5 py-4">
        <Server className="h-5 w-5 text-sage-600 shrink-0" />
        <div>
          <span className="text-[14px] font-semibold text-sage-700">
            Model Context Protocol (MCP) Integration
          </span>
          <span className="ml-2 text-[13px] text-sage-600">
            — Select any connector to browse its MCP tools and invoke them via{" "}
            <code className="rounded bg-sage-100 px-1 text-[12px]">session.list_tools()</code> /{" "}
            <code className="rounded bg-sage-100 px-1 text-[12px]">session.call_tool()</code>
          </span>
        </div>
        <Badge tone="ok" className="ml-auto shrink-0">MCP SDK Active</Badge>
      </div>

      <div className="mt-4 flex gap-6 px-8">
        {/* Left: Connector List */}
        <div className="w-72 shrink-0 space-y-2">
          <div className="mb-3 text-[12px] font-semibold uppercase tracking-wider text-muted">
            11 MCP Connectors
          </div>
          {CONNECTORS.map((c) => (
            <button
              key={c.id}
              onClick={() => loadTools(c.id)}
              className={`flex w-full items-center gap-3 rounded-2xl border px-4 py-3 text-left transition-all ${
                selectedConnector === c.id
                  ? "border-sage-300 bg-sage-50 shadow-sm"
                  : "border-line/60 bg-white hover:border-sage-200 hover:bg-sage-50/50"
              }`}
            >
              <span className="text-[20px]">{c.icon}</span>
              <div className="min-w-0">
                <div className="text-[13.5px] font-semibold text-ink">{c.name}</div>
                <div className="text-[11.5px] capitalize text-muted">
                  {c.category.replace(/_/g, " ")}
                </div>
              </div>
              {selectedConnector === c.id ? (
                <ChevronDown className="ml-auto h-4 w-4 text-sage-600" />
              ) : (
                <ChevronRight className="ml-auto h-4 w-4 text-muted/50" />
              )}
            </button>
          ))}
        </div>

        {/* Right: MCP Tool Browser */}
        <div className="flex-1 space-y-4">
          {!selectedConnector && (
            <Card className="flex h-64 items-center justify-center text-center">
              <div>
                <Plug className="mx-auto mb-3 h-10 w-10 text-muted/30" />
                <p className="text-[14px] font-medium text-muted">
                  Select a connector to browse its MCP tools
                </p>
                <p className="mt-1 text-[12.5px] text-muted/70">
                  Each connector uses the MCP protocol to expose its capabilities
                </p>
              </div>
            </Card>
          )}

          {selectedConnector && loadingTools && (
            <Card className="flex h-48 items-center justify-center gap-2 text-muted">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span className="text-[14px]">Calling MCP list_tools()…</span>
            </Card>
          )}

          {toolsData && !loadingTools && (
            <>
              {/* Protocol header */}
              <Card>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-[15px] font-semibold text-ink">
                      {toolsData.connector} MCP Server
                    </div>
                    <div className="mt-0.5 flex items-center gap-2 text-[12.5px] text-muted">
                      <code className="rounded bg-canvas px-1.5 py-0.5 text-[11px]">
                        {toolsData.mcp_protocol}
                      </code>
                      <span>·</span>
                      <span>{toolsData.tools.length} tools discovered</span>
                    </div>
                    {toolsData.note && (
                      <p className="mt-2 text-[12px] text-muted/80 italic">{toolsData.note}</p>
                    )}
                  </div>
                  <Badge tone={toolsData.mode === "live" ? "ok" : "neutral"}>
                    {toolsData.mode === "live" ? "🟢 Live MCP" : "🔵 Mock Mode"}
                  </Badge>
                </div>
              </Card>

              {/* Tool List */}
              <Card>
                <CardHeader title="Available Tools" />
                <div className="space-y-2">
                  {toolsData.tools.map((tool) => (
                    <button
                      key={tool.name}
                      onClick={() => { setSelectedTool(tool); setCallResult(null); setToolArgs("{}"); }}
                      className={`w-full rounded-2xl border p-4 text-left transition-all ${
                        selectedTool?.name === tool.name
                          ? "border-sage-300 bg-sage-50"
                          : "border-line/50 hover:border-sage-200 hover:bg-canvas"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        {selectedTool?.name === tool.name ? (
                          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-sage-600" />
                        ) : (
                          <Circle className="mt-0.5 h-4 w-4 shrink-0 text-muted/40" />
                        )}
                        <div>
                          <div className="text-[13.5px] font-semibold text-ink">
                            <code>{tool.name}</code>
                          </div>
                          <div className="mt-0.5 text-[12.5px] text-muted">{tool.description}</div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </Card>

              {/* Tool Invocation Panel */}
              {selectedTool && (
                <Card>
                  <CardHeader
                    title={`Invoke: ${selectedTool.name}`}
                    action={
                      <div className="flex items-center gap-1.5 text-[12px] text-muted">
                        <Terminal className="h-3.5 w-3.5" />
                        <span>call_tool()</span>
                      </div>
                    }
                  />
                  <div className="space-y-3">
                    <div>
                      <label className="mb-1.5 block text-[12px] font-medium text-muted">
                        Arguments (JSON)
                      </label>
                      <textarea
                        value={toolArgs}
                        onChange={(e) => setToolArgs(e.target.value)}
                        rows={4}
                        className="w-full rounded-2xl border border-line/60 bg-canvas p-3 font-mono text-[12.5px] text-ink outline-none focus:border-sage-400"
                        placeholder='{"key": "value"}'
                      />
                    </div>
                    <button
                      onClick={callTool}
                      disabled={callingTool}
                      className="flex items-center gap-2 rounded-full bg-ink px-5 py-2.5 text-[13.5px] font-medium text-white transition-all hover:bg-sage-700 disabled:opacity-60"
                    >
                      {callingTool ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Zap className="h-4 w-4" />
                      )}
                      {callingTool ? "Calling…" : "Invoke Tool via MCP"}
                    </button>

                    {callResult && (
                      <div className="mt-2 space-y-2">
                        <div className="text-[12px] font-medium text-muted">MCP Tool Result:</div>
                        {callResult.map((block, i) => (
                          <div
                            key={i}
                            className="rounded-2xl border border-line/50 bg-canvas p-4 font-mono text-[12.5px] text-ink whitespace-pre-wrap"
                          >
                            {block.text}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </Card>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
