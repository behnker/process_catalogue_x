"use client";

import * as React from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { ProcessCard } from "./ProcessCard";
import type { OverlayMode } from "./HeatmapOverlayControls";
import type { HeatmapCell } from "@/types/issue.types";
import type { Process } from "@/types/api";

interface ExpandableL2CardProps {
  process: Process;
  onProcessClick?: (process: Process) => void;
  onRaiseIssue?: (process: Process) => void;
  selectedProcessId?: string;
  overlayMode?: OverlayMode;
  heatmapMap?: Map<string, HeatmapCell>;
}

/**
 * Expandable L2 Card with L3+ children as nested items.
 * Used in ProcessCanvas to show the hierarchy below L2.
 */
export function ExpandableL2Card({
  process,
  onProcessClick,
  onRaiseIssue,
  selectedProcessId,
  overlayMode = "off",
  heatmapMap,
}: ExpandableL2CardProps) {
  const [isExpanded, setIsExpanded] = React.useState(false);
  const children = process.children || [];
  const hasChildren = children.length > 0;

  return (
    <div>
      {/* L2 Card - full width */}
      <ProcessCard
        process={process}
        variant="l2"
        isSelected={selectedProcessId === process.id}
        onInfoClick={() => onProcessClick?.(process)}
        onRaiseIssue={onRaiseIssue ? () => onRaiseIssue(process) : undefined}
        expandable={hasChildren}
        isExpanded={isExpanded}
        onExpandToggle={() => setIsExpanded(!isExpanded)}
        overlayMode={overlayMode}
        heatmapCell={heatmapMap?.get(process.id)}
      />

      {/* L3+ Children (expanded) */}
      {isExpanded && hasChildren && (
        <div className="ml-6 mt-1 space-y-0.5 border-l-2 border-slate-200 pl-3">
          {children.map((child) => (
            <ExpandableChildCard
              key={child.id}
              process={child}
              onProcessClick={onProcessClick}
              onRaiseIssue={onRaiseIssue}
              selectedProcessId={selectedProcessId}
              depth={0}
              overlayMode={overlayMode}
              heatmapMap={heatmapMap}
            />
          ))}
        </div>
      )}
    </div>
  );
}

interface ExpandableChildCardProps {
  process: Process;
  onProcessClick?: (process: Process) => void;
  onRaiseIssue?: (process: Process) => void;
  selectedProcessId?: string;
  depth: number;
  overlayMode?: OverlayMode;
  heatmapMap?: Map<string, HeatmapCell>;
}

/**
 * Recursive component for L3+ children.
 * Renders nested process hierarchy with expand/collapse functionality.
 */
export function ExpandableChildCard({
  process,
  onProcessClick,
  onRaiseIssue,
  selectedProcessId,
  depth,
  overlayMode = "off",
  heatmapMap,
}: ExpandableChildCardProps) {
  const [isExpanded, setIsExpanded] = React.useState(false);
  const children = process.children || [];
  const hasChildren = children.length > 0;

  return (
    <div style={{ marginLeft: `${depth * 12}px` }}>
      {/* L3+ Item */}
      <div className="flex items-center gap-1">
        {hasChildren && (
          <button
            type="button"
            className="p-0.5 text-slate-400 hover:text-slate-600 rounded hover:bg-slate-100"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? (
              <ChevronUp className="h-3 w-3" />
            ) : (
              <ChevronDown className="h-3 w-3" />
            )}
          </button>
        )}
        {!hasChildren && <div className="w-4" />}

        <div className="flex-1">
          <ProcessCard
            process={process}
            variant="l3"
            isSelected={selectedProcessId === process.id}
            onClick={() => onProcessClick?.(process)}
            onRaiseIssue={onRaiseIssue ? () => onRaiseIssue(process) : undefined}
            overlayMode={overlayMode}
            heatmapCell={heatmapMap?.get(process.id)}
          />
        </div>
      </div>

      {/* Nested children */}
      {isExpanded && hasChildren && (
        <div className="ml-4">
          {children.map((child) => (
            <ExpandableChildCard
              key={child.id}
              process={child}
              onProcessClick={onProcessClick}
              onRaiseIssue={onRaiseIssue}
              selectedProcessId={selectedProcessId}
              depth={0}
              overlayMode={overlayMode}
              heatmapMap={heatmapMap}
            />
          ))}
        </div>
      )}
    </div>
  );
}
