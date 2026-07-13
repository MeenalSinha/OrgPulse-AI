"use client";

import { useState } from "react";
import { Topbar } from "@/components/Topbar";
import { Card } from "@/components/Card";
import { api } from "@/lib/api";
import { Send, Sparkles } from "lucide-react";
import { ReleaseReadinessCard, ReleaseReadiness } from "@/components/ReleaseReadinessCard";

type Message = {
  role: "user" | "assistant"; text: string; citations?: string[]; confidence?: number;
  synthesizedBy?: string; releaseReadiness?: ReleaseReadiness | null;
};

const SUGGESTIONS = [
  "Can we ship the Mobile App on Friday?",
  "Why is Mobile App at risk?",
  "Why did we migrate to PostgreSQL?",
  "Who understands Payments API?",
];

export default function AIChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", text: "Ask me anything about your organization. I reason over the dependency graph and organizational memory, and every answer is cited." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send(query: string) {
    if (!query.trim()) return;
    setMessages((m) => [...m, { role: "user", text: query }]);
    setInput("");
    setLoading(true);
    const result = await api.chat(query);
    setMessages((m) => [...m, {
      role: "assistant", text: result.answer, citations: result.citations,
      confidence: result.confidence, synthesizedBy: result.synthesized_by,
      releaseReadiness: result.release_readiness,
    }]);
    setLoading(false);
  }

  return (
    <div className="flex flex-col">
      <Topbar greetingName="Carl" subtitle="Ask OrgPulse anything. Answers are grounded in the graph, never guessed." />
      <div className="mt-6 flex flex-col px-8 pb-8">
        <Card className="flex flex-col overflow-hidden">
          <div className="flex-1 space-y-4 overflow-y-auto pr-2" style={{ height: "min(65vh, 620px)" }}>
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                {m.role === "assistant" && m.releaseReadiness ? (
                  <div className="w-full max-w-[420px]">
                    <ReleaseReadinessCard data={m.releaseReadiness} />
                  </div>
                ) : (
                <div className={`max-w-[70%] rounded-2xl px-4 py-3 text-[13.5px] ${
                  m.role === "user" ? "bg-ink text-white" : "bg-canvas text-ink"
                }`}>
                  <p className="leading-relaxed">{m.text}</p>
                  {m.citations && m.citations.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {m.citations.map((c) => (
                        <span key={c} className="rounded-full bg-white px-2 py-0.5 text-[10.5px] font-mono text-muted">{c}</span>
                      ))}
                    </div>
                  )}
                  {typeof m.confidence === "number" && m.confidence > 0 && (
                    <div className="mt-1.5 flex items-center gap-2 text-[11px] text-muted">
                      <span>Confidence: {m.confidence}%</span>
                      {m.synthesizedBy === "claude" && (
                        <span className="rounded-full bg-sage-100 px-2 py-0.5 font-medium text-sage-700">Composed by Claude</span>
                      )}
                    </div>
                  )}
                </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="flex items-center gap-2 rounded-2xl bg-canvas px-4 py-3 text-[13px] text-muted">
                  <Sparkles className="h-3.5 w-3.5 animate-pulse" /> Reasoning over the graph...
                </div>
              </div>
            )}
          </div>

          <div className="mt-4 flex flex-wrap gap-2 border-t border-line pt-4">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => send(s)}
                className="focus-ring rounded-full border border-line px-3 py-1.5 text-[12px] font-medium text-muted hover:bg-canvas"
              >
                {s}
              </button>
            ))}
          </div>

          <form
            onSubmit={(e) => { e.preventDefault(); send(input); }}
            className="mt-3 flex items-center gap-2"
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="@OrgPulse, ask a question..."
              className="focus-ring flex-1 rounded-full border border-line bg-white px-4 py-2.5 text-[13px] outline-none placeholder:text-muted"
            />
            <button
              type="submit"
              disabled={loading}
              className="focus-ring flex h-10 w-10 items-center justify-center rounded-full bg-sage-600 text-white hover:bg-sage-700 disabled:opacity-50"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
}
