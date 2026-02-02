"use client";

import { Info, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Process } from "@/types/api";

interface ProcessCardProps {
  process: Process;
  onClick?: () => void;
  isSelected?: boolean;
  variant?: "l0" | "l1" | "l2" | "l3";
  showInfoButton?: boolean;
  onInfoClick?: () => void;
  // For L2 cards with expand/collapse
  expandable?: boolean;
  isExpanded?: boolean;
  onExpandToggle?: () => void;
}

/**
 * Clean process card matching Antigravity design:
 * - L0: Swimlane header with "LEVEL 0" label
 * - L1: ALL CAPS text header (no card)
 * - L2: Card with blue left border, name only
 * - L3+: Simple indented text
 */
export function ProcessCard({
  process,
  onClick,
  isSelected = false,
  variant = "l2",
  showInfoButton = false,
  onInfoClick,
  expandable = false,
  isExpanded = false,
  onExpandToggle,
}: ProcessCardProps) {
  // L0 - Swimlane Header
  if (variant === "l0") {
    return (
      <div
        className={cn(
          "p-4 bg-slate-50 border rounded-lg cursor-pointer",
          isSelected && "ring-2 ring-primary"
        )}
        onClick={onClick}
      >
        <div className="flex items-center justify-between">
          <div>
            <span className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
              Level 0
            </span>
            <h2 className="text-lg font-bold uppercase mt-1 text-slate-900">{process.name}</h2>
          </div>
          {showInfoButton && (
            <button
              type="button"
              className="p-1 text-muted-foreground hover:text-primary rounded-full hover:bg-muted"
              onClick={(e) => {
                e.stopPropagation();
                onInfoClick?.();
              }}
              title="View details"
            >
              <Info className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>
    );
  }

  // L1 - Column Header (ALL CAPS text, no card)
  if (variant === "l1") {
    return (
      <div
        className={cn(
          "pb-2 border-b border-slate-200 cursor-pointer",
          isSelected && "border-primary"
        )}
        onClick={onClick}
      >
        <h3 className="text-sm font-semibold text-slate-600 uppercase tracking-wide truncate" title={process.name}>
          {process.name}
        </h3>
      </div>
    );
  }

  // L3+ - Simple text (no card border)
  if (variant === "l3") {
    return (
      <div
        className={cn(
          "py-2 px-3 cursor-pointer hover:bg-slate-50 rounded transition-colors",
          isSelected && "bg-primary/5"
        )}
        onClick={onClick}
      >
        <span className="text-sm text-slate-700">{process.name}</span>
      </div>
    );
  }

  // L2 - Card with blue left border (default)
  return (
    <div
      className={cn(
        "group bg-white border border-slate-200 rounded-lg transition-all hover:shadow-sm",
        "border-l-[3px] border-l-blue-500",
        isSelected && "ring-2 ring-primary"
      )}
    >
      <div className="flex items-center py-2 px-3 gap-2">
        {/* Expand/Collapse button - inside card */}
        {expandable && (
          <button
            type="button"
            className="p-1 text-slate-400 hover:text-slate-600 rounded hover:bg-slate-100 flex-shrink-0"
            onClick={(e) => {
              e.stopPropagation();
              onExpandToggle?.();
            }}
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </button>
        )}

        {/* Process name */}
        <span
          className="font-medium text-slate-800 truncate cursor-pointer flex-1"
          onClick={onClick}
          title={process.name}
        >
          {process.name}
        </span>

        {/* Info button - visible on hover */}
        <button
          type="button"
          className={cn(
            "p-1 text-muted-foreground hover:text-primary rounded-full hover:bg-muted flex-shrink-0 transition-opacity",
            "opacity-0 group-hover:opacity-100"
          )}
          onClick={(e) => {
            e.stopPropagation();
            onInfoClick?.();
          }}
          title="View details"
        >
          <Info className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}

export function ProcessCardSkeleton({ variant = "l2" }: { variant?: "l0" | "l1" | "l2" | "l3" }) {
  if (variant === "l0") {
    return (
      <div className="p-4 bg-slate-50 border rounded-lg animate-pulse">
        <div className="h-3 w-12 bg-slate-200 rounded mb-2" />
        <div className="h-6 w-32 bg-slate-200 rounded" />
      </div>
    );
  }

  if (variant === "l1") {
    return (
      <div className="pb-2 border-b border-slate-200 animate-pulse">
        <div className="h-4 w-24 bg-slate-200 rounded" />
      </div>
    );
  }

  if (variant === "l3") {
    return (
      <div className="py-2 px-3 animate-pulse">
        <div className="h-4 w-32 bg-slate-200 rounded" />
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-lg border-l-[3px] border-l-slate-200 animate-pulse">
      <div className="p-3">
        <div className="h-5 w-3/4 bg-slate-200 rounded" />
      </div>
    </div>
  );
}
