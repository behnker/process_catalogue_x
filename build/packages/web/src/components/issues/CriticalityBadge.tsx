"use client";

import { cn } from "@/lib/utils";
import type { IssueCriticality } from "@/types/issue.types";

interface CriticalityBadgeProps {
  criticality: IssueCriticality;
  className?: string;
}

const criticalityConfig: Record<
  IssueCriticality,
  { bg: string; text: string; label: string; icon: string }
> = {
  high: {
    bg: "bg-red-100 dark:bg-red-900/30",
    text: "text-red-800 dark:text-red-400",
    label: "High",
    icon: "!!",
  },
  medium: {
    bg: "bg-amber-100 dark:bg-amber-900/30",
    text: "text-amber-800 dark:text-amber-400",
    label: "Medium",
    icon: "!",
  },
  low: {
    bg: "bg-green-100 dark:bg-green-900/30",
    text: "text-green-800 dark:text-green-400",
    label: "Low",
    icon: "-",
  },
};

export function CriticalityBadge({
  criticality,
  className,
}: CriticalityBadgeProps) {
  const config = criticalityConfig[criticality] || criticalityConfig.medium;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium",
        config.bg,
        config.text,
        className
      )}
    >
      <span className="font-bold">{config.icon}</span>
      {config.label}
    </span>
  );
}

// Compact icon-only version
export function CriticalityIcon({
  criticality,
  className,
}: CriticalityBadgeProps) {
  const config = criticalityConfig[criticality] || criticalityConfig.medium;

  return (
    <span
      className={cn(
        "inline-flex items-center justify-center w-5 h-5 rounded-full text-xs font-bold",
        config.bg,
        config.text,
        className
      )}
      title={`${config.label} Criticality`}
    >
      {config.icon}
    </span>
  );
}
