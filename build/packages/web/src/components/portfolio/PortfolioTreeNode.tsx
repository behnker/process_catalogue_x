"use client";

import * as React from "react";
import { ChevronRight, ChevronDown } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { PortfolioItem, PortfolioLevel, PortfolioStatus, RagStatus } from "@/types/api";
import { cn } from "@/lib/utils";

export const levelColors: Record<PortfolioLevel, string> = {
  strategy: "bg-purple-500",
  portfolio: "bg-blue-500",
  programme: "bg-green-500",
  project: "bg-orange-500",
  workstream: "bg-yellow-500",
  epic: "bg-pink-500",
  task: "bg-gray-500",
};

export const statusVariants: Record<PortfolioStatus, "success" | "warning" | "secondary" | "danger"> = {
  proposed: "secondary",
  approved: "success",
  in_progress: "warning",
  on_hold: "secondary",
  completed: "success",
  cancelled: "danger",
};

export const ragColors: Record<RagStatus, string> = {
  red: "bg-rag-red",
  amber: "bg-rag-amber",
  green: "bg-rag-green",
};

interface PortfolioTreeNodeProps {
  item: PortfolioItem;
  depth: number;
  onSelect: (item: PortfolioItem) => void;
  selectedId?: string;
}

export function PortfolioTreeNode({ item, depth, onSelect, selectedId }: PortfolioTreeNodeProps) {
  const [expanded, setExpanded] = React.useState(depth < 2);
  const hasChildren = item.children && item.children.length > 0;

  return (
    <div>
      <div
        className={cn(
          "flex items-center gap-2 py-2 px-3 cursor-pointer hover:bg-muted rounded-md transition-colors",
          selectedId === item.id && "bg-muted"
        )}
        style={{ paddingLeft: `${depth * 24 + 12}px` }}
        onClick={() => onSelect(item)}
      >
        {hasChildren ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setExpanded(!expanded);
            }}
            className="p-0.5 hover:bg-accent rounded"
          >
            {expanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        ) : (
          <span className="w-5" />
        )}

        <div className={cn("w-2 h-2 rounded-full", levelColors[item.level])} />
        <span className="font-mono text-xs text-muted-foreground">{item.code}</span>
        <span className="font-medium flex-1">{item.name}</span>

        {item.rag_status && (
          <div className={cn("w-3 h-3 rounded-full", ragColors[item.rag_status])} />
        )}

        <Badge variant={statusVariants[item.status]} className="text-xs capitalize">
          {item.status.replace("_", " ")}
        </Badge>
      </div>

      {expanded && hasChildren && (
        <div>
          {item.children!.map((child) => (
            <PortfolioTreeNode
              key={child.id}
              item={child}
              depth={depth + 1}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
}
