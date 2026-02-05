"use client";

import { cn } from "@/lib/utils";
import type { RAGStatusExtended } from "@/types/issue.types";

interface RAGBadgeProps {
  status: RAGStatusExtended;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
  className?: string;
}

const statusConfig: Record<
  RAGStatusExtended,
  { bg: string; text: string; label: string; dot: string }
> = {
  red: {
    bg: "bg-red-100 dark:bg-red-900/30",
    text: "text-red-800 dark:text-red-400",
    label: "Red",
    dot: "bg-red-500",
  },
  amber: {
    bg: "bg-amber-100 dark:bg-amber-900/30",
    text: "text-amber-800 dark:text-amber-400",
    label: "Amber",
    dot: "bg-amber-500",
  },
  green: {
    bg: "bg-green-100 dark:bg-green-900/30",
    text: "text-green-800 dark:text-green-400",
    label: "Green",
    dot: "bg-green-500",
  },
  neutral: {
    bg: "bg-gray-100 dark:bg-gray-800",
    text: "text-gray-600 dark:text-gray-400",
    label: "Neutral",
    dot: "bg-gray-400",
  },
};

const sizeConfig = {
  sm: { badge: "px-1.5 py-0.5 text-xs", dot: "w-1.5 h-1.5" },
  md: { badge: "px-2 py-0.5 text-xs", dot: "w-2 h-2" },
  lg: { badge: "px-2.5 py-1 text-sm", dot: "w-2.5 h-2.5" },
};

export function RAGBadge({
  status,
  size = "md",
  showLabel = true,
  className,
}: RAGBadgeProps) {
  const config = statusConfig[status] || statusConfig.neutral;
  const sizes = sizeConfig[size];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full font-medium",
        config.bg,
        config.text,
        sizes.badge,
        className
      )}
    >
      <span className={cn("rounded-full", config.dot, sizes.dot)} />
      {showLabel && <span>{config.label}</span>}
    </span>
  );
}

// Compact dot-only version for heatmaps
export function RAGDot({
  status,
  size = "md",
  className,
}: Omit<RAGBadgeProps, "showLabel">) {
  const config = statusConfig[status] || statusConfig.neutral;
  const dotSize = size === "sm" ? "w-2 h-2" : size === "lg" ? "w-4 h-4" : "w-3 h-3";

  return (
    <span
      className={cn("rounded-full inline-block", config.dot, dotSize, className)}
      title={config.label}
    />
  );
}

// Four-dimension RAG indicator row
interface RAGDimensionsProps {
  people?: RAGStatusExtended;
  process?: RAGStatusExtended;
  system?: RAGStatusExtended;
  data?: RAGStatusExtended;
  size?: "sm" | "md" | "lg";
  showLabels?: boolean;
}

export function RAGDimensions({
  people = "neutral",
  process = "neutral",
  system = "neutral",
  data = "neutral",
  size = "sm",
  showLabels = false,
}: RAGDimensionsProps) {
  const dimensions = [
    { key: "people", status: people, label: "P" },
    { key: "process", status: process, label: "Pr" },
    { key: "system", status: system, label: "S" },
    { key: "data", status: data, label: "D" },
  ];

  return (
    <div className="flex items-center gap-1">
      {dimensions.map((dim) => (
        <div key={dim.key} className="flex items-center gap-0.5" title={dim.key}>
          <RAGDot status={dim.status} size={size} />
          {showLabels && (
            <span className="text-xs text-muted-foreground">{dim.label}</span>
          )}
        </div>
      ))}
    </div>
  );
}
