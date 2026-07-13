import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OrgPulse AI",
  description: "The AI that remembers your company, understands how work flows, and prevents delays before they happen.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
