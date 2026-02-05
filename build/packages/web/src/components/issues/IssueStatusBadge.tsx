"use client";

import { cn } from "@/lib/utils";
import type { IssueStatus } from "@/types/issue.types";

interface IssueStatusBadgeProps {
  status: IssueStatus;
  className?: string;
}

const statusConfig: Record<
  IssueStatus,
  { bg: string; text: string; label: string }
> = {
  open: {
    bg: "bg-blue-100 dark:bg-blue-900/30",
    text: "text-blue-800 dark:text-blue-400",
    label: "Open",
  },
  in_progress: {
    bg: "bg-amber-100 dark:bg-amber-900/30",
    text: "text-amber-800 dark:text-amber-400",
    label: "In Progress",
  },
  resolved: {
    bg: "bg-green-100 dark:bg-green-900/30",
    text: "text-green-800 dark:text-green-400",
    label: "Resolved",
  },
  closed: {
    bg: "bg-gray-100 dark:bg-gray-800",
    text: "text-gray-600 dark:text-gray-400",
    label: "Closed",
  },
  deferred: {
    bg: "bg-purple-100 dark:bg-purple-900/30",
    text: "text-purple-800 dark:text-purple-400",
    label: "Deferred",
  },
};

export function IssueStatusBadge({ status, className }: IssueStatusBadgeProps) {
  const config = statusConfig[status] || statusConfig.open;

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        config.bg,
        config.text,
        className
      )}
    >
      {config.label}
    </span>
  );
}
