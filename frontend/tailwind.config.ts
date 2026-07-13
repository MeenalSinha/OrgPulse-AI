import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#F7F8F9",
        ink: "#1C201D",
        muted: "#8A948C",
        sage: {
          50: "#EEF2ED",
          100: "#DCE6D9",
          400: "#6B8F76",
          600: "#3E5B45",
          700: "#2F4736",
          900: "#1E2E22",
        },
        line: "#E6E8E3",
        danger: { bg: "#FFF4F4", text: "#E53E3E" },
        warn: { bg: "#FFF9F0", text: "#D69E2E" },
        ok: { bg: "#F0FFF4", text: "#38A169" },
      },
      borderRadius: {
        xl: "14px",
        "2xl": "20px",
        "3xl": "28px",
      },
      boxShadow: {
        card: "0 2px 24px rgba(28,32,29,0.03)",
      },
      fontFamily: {
        sans: [
          "Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto",
          "Helvetica Neue", "Arial", "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};
export default config;
