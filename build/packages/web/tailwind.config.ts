import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // shadcn/ui colors
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Surity theme (Blueprint §10.12.1)
        brand: {
          50: "#FFFBEB",
          100: "#FEF3C7",
          200: "#FDE68A",
          300: "#FCD34D",
          400: "#FBBF24",
          500: "#F59E0B", // Primary
          600: "#D97706", // Primary Hover
          700: "#B45309",
          800: "#92400E",
          900: "#78350F",
        },
        surface: {
          DEFAULT: "#FFFFFF",
          muted: "#F9FAFB",
          sidebar: "#F3F4F6",
        },
        // RAG colors (Blueprint §10.12.6: never color alone)
        rag: {
          red: "#EF4444",
          amber: "#F59E0B",
          green: "#22C55E",
        },
      },
      fontFamily: {
        // Nunito — self-hosted for China compatibility (Blueprint §10.12.2)
        sans: ["Nunito", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      fontSize: {
        // Blueprint §10.12.2 type scale
        h1: ["30px", { lineHeight: "1.3", fontWeight: "700" }],
        h2: ["24px", { lineHeight: "1.3", fontWeight: "600" }],
        h3: ["20px", { lineHeight: "1.4", fontWeight: "600" }],
        h4: ["16px", { lineHeight: "1.4", fontWeight: "600" }],
        body: ["14px", { lineHeight: "1.5", fontWeight: "400" }],
        "body-sm": ["13px", { lineHeight: "1.5", fontWeight: "400" }],
        caption: ["12px", { lineHeight: "1.4", fontWeight: "400" }],
      },
      spacing: {
        // Blueprint §10.12.3 spacing tokens
        xs: "4px",
        sm: "8px",
        md: "16px",
        lg: "24px",
        xl: "32px",
        "2xl": "48px",
        sidebar: "256px",
        "sidebar-collapsed": "64px",
      },
      borderRadius: {
        DEFAULT: "8px",
        sm: "6px",
        lg: "12px",
      },
      animation: {
        "sidebar-expand": "sidebar-expand 200ms ease-in-out",
        "sidebar-collapse": "sidebar-collapse 200ms ease-in-out",
        "fade-in": "fade-in 150ms ease-out",
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      keyframes: {
        "sidebar-expand": {
          from: { width: "64px" },
          to: { width: "256px" },
        },
        "sidebar-collapse": {
          from: { width: "256px" },
          to: { width: "64px" },
        },
        "fade-in": {
          from: { opacity: "0", transform: "translateY(4px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
