"use client";

import { Search, Bell, MessageSquare } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";
import { useState } from "react";

export function Topbar({ greetingName = "Carl", subtitle }: { greetingName?: string; subtitle?: string }) {
  const [messagesCount, setMessagesCount] = useState(3);
  const [notificationsCount, setNotificationsCount] = useState(7);
  const [showMessages, setShowMessages] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  return (
    <div className="flex flex-wrap items-center justify-between gap-4 px-8 pt-8">
      <div>
        <h1 className="text-[26px] font-semibold tracking-tight text-ink dark:text-white flex items-center gap-2">
          Hello, {greetingName}! <span className="text-[28px] leading-none">👋</span>
        </h1>
        <p className="mt-1.5 text-[14px] text-muted font-medium">
          {subtitle ?? "Here's what's happening across your organization today."}
        </p>
      </div>

      <div className="flex items-center gap-3">
        <div className="focus-ring flex w-80 items-center gap-3 rounded-full border border-line/60 bg-white shadow-sm px-5 py-3 text-[14px] text-muted dark:border-white/10 dark:bg-[#242822]">
          <Search className="h-4 w-4 text-muted/70" />
          <input
            placeholder="Search anything..."
            aria-label="Search"
            className="w-full bg-transparent outline-none placeholder:text-muted"
          />
        </div>
        <ThemeToggle />
        <div className="relative">
          <button 
            aria-label="Messages" 
            onClick={() => {
              setMessagesCount(0);
              setShowMessages(!showMessages);
              setShowNotifications(false);
            }}
            className="focus-ring relative flex h-11 w-11 items-center justify-center rounded-full bg-transparent text-ink hover:bg-black/5 dark:text-white dark:hover:bg-white/10 transition-colors"
          >
            <MessageSquare className="h-5 w-5" />
            {messagesCount > 0 && (
              <span className="absolute right-1 top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-[#E53E3E] border-2 border-canvas px-1 text-[9px] font-bold text-white">
                {messagesCount}
              </span>
            )}
          </button>
          
          {showMessages && (
            <div className="absolute right-0 top-12 z-50 w-72 rounded-2xl border border-line bg-white p-4 shadow-xl dark:border-white/10 dark:bg-[#1E221D]">
              <h3 className="mb-3 text-[14px] font-semibold text-ink dark:text-white">Messages</h3>
              <div className="flex flex-col gap-3">
                <div className="flex items-start gap-3 rounded-xl p-2 transition-colors hover:bg-black/5 dark:hover:bg-white/5">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-sage-100 text-[12px] font-bold text-sage-700">SA</div>
                  <div>
                    <p className="text-[13px] font-medium text-ink dark:text-white">Sarah Allen</p>
                    <p className="text-[12px] text-muted">Can you review the Q3 roadmap?</p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-xl p-2 transition-colors hover:bg-black/5 dark:hover:bg-white/5">
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-100 text-[12px] font-bold text-blue-700">JD</div>
                  <div>
                    <p className="text-[13px] font-medium text-ink dark:text-white">James Doe</p>
                    <p className="text-[12px] text-muted">The API integration is deployed.</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="relative">
          <button 
            aria-label="Notifications" 
            onClick={() => {
              setNotificationsCount(0);
              setShowNotifications(!showNotifications);
              setShowMessages(false);
            }}
            className="focus-ring relative flex h-11 w-11 items-center justify-center rounded-full bg-transparent text-ink hover:bg-black/5 dark:text-white dark:hover:bg-white/10 transition-colors"
          >
            <Bell className="h-5 w-5" />
            {notificationsCount > 0 && (
              <span className="absolute right-1 top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-[#E53E3E] border-2 border-canvas px-1 text-[9px] font-bold text-white">
                {notificationsCount}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 top-12 z-50 w-72 rounded-2xl border border-line bg-white p-4 shadow-xl dark:border-white/10 dark:bg-[#1E221D]">
              <h3 className="mb-3 text-[14px] font-semibold text-ink dark:text-white">Notifications</h3>
              <div className="flex flex-col gap-3">
                <div className="flex items-start gap-3 rounded-xl p-2 transition-colors hover:bg-black/5 dark:hover:bg-white/5">
                  <div className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-[#C0392B]"></div>
                  <div>
                    <p className="text-[13px] font-medium text-ink dark:text-white">Deployment Failed</p>
                    <p className="text-[12px] text-muted">Production build failed in us-east-1.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3 rounded-xl p-2 transition-colors hover:bg-black/5 dark:hover:bg-white/5">
                  <div className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-sage-500"></div>
                  <div>
                    <p className="text-[13px] font-medium text-ink dark:text-white">New user signup</p>
                    <p className="text-[12px] text-muted">Acme Corp joined the platform.</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
