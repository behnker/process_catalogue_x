"use client";

import { cn } from "@/lib/utils";
import type { IssueClassification } from "@/types/issue.types";

interface ClassificationIconProps {
  classification: IssueClassification;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
  className?: string;
}

// Simple SVG icons for each classification
const icons: Record<IssueClassification, React.ReactNode> = {
  people: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
    </svg>
  ),
  process: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="3" width="7" height="7" rx="1" />
      <rect x="3" y="14" width="7" height="7" rx="1" />
      <rect x="14" y="14" width="7" height="7" rx="1" />
      <path d="M10 6.5h4M6.5 10v4M17.5 10v4M10 17.5h4" />
    </svg>
  ),
  system: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="2" y="4" width="20" height="14" rx="2" />
      <path d="M8 21h8M12 18v3" />
    </svg>
  ),
  data: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
      <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" />
    </svg>
  ),
};

const labels: Record<IssueClassification, string> = {
  people: "People",
  process: "Process",
  system: "System",
  data: "Data",
};

const colors: Record<IssueClassification, { bg: string; icon: string }> = {
  people: {
    bg: "bg-blue-100 dark:bg-blue-900/30",
    icon: "text-blue-600 dark:text-blue-400",
  },
  process: {
    bg: "bg-purple-100 dark:bg-purple-900/30",
    icon: "text-purple-600 dark:text-purple-400",
  },
  system: {
    bg: "bg-cyan-100 dark:bg-cyan-900/30",
    icon: "text-cyan-600 dark:text-cyan-400",
  },
  data: {
    bg: "bg-amber-100 dark:bg-amber-900/30",
    icon: "text-amber-600 dark:text-amber-400",
  },
};

const sizeConfig = {
  sm: { container: "w-5 h-5", icon: "w-3 h-3" },
  md: { container: "w-6 h-6", icon: "w-4 h-4" },
  lg: { container: "w-8 h-8", icon: "w-5 h-5" },
};

export function ClassificationIcon({
  classification,
  size = "md",
  showLabel = false,
  className,
}: ClassificationIconProps) {
  const color = colors[classification];
  const sizes = sizeConfig[size];

  return (
    <div
      className={cn("inline-flex items-center gap-1.5", className)}
      title={labels[classification]}
    >
      <span
        className={cn(
          "inline-flex items-center justify-center rounded",
          color.bg,
          sizes.container
        )}
      >
        <span className={cn(color.icon, sizes.icon)}>
          {icons[classification]}
        </span>
      </span>
      {showLabel && (
        <span className="text-sm text-muted-foreground">
          {labels[classification]}
        </span>
      )}
    </div>
  );
}

// Row of all four classification icons with counts
interface ClassificationCountsProps {
  people?: number;
  process?: number;
  system?: number;
  data?: number;
  size?: "sm" | "md" | "lg";
}

export function ClassificationCounts({
  people = 0,
  process = 0,
  system = 0,
  data = 0,
  size = "sm",
}: ClassificationCountsProps) {
  const items: { key: IssueClassification; count: number }[] = [
    { key: "people", count: people },
    { key: "process", count: process },
    { key: "system", count: system },
    { key: "data", count: data },
  ];

  return (
    <div className="flex items-center gap-2">
      {items.map(({ key, count }) => (
        <div key={key} className="flex items-center gap-0.5">
          <ClassificationIcon classification={key} size={size} />
          <span className="text-xs text-muted-foreground">{count}</span>
        </div>
      ))}
    </div>
  );
}
