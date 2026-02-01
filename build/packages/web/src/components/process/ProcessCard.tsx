"use client";

import { ChevronRight, AlertCircle, CheckCircle, MinusCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Process, RagStatus } from "@/types/api";

interface ProcessCardProps {
  process: Process;
  onClick?: () => void;
  isSelected?: boolean;
  showChildren?: boolean;
  size?: "sm" | "md" | "lg";
}

const sizeClasses = {
  sm: "p-2",
  md: "p-3",
  lg: "p-4",
};

const levelColors: Record<string, string> = {
  L0: "border-l-brand-500",
  L1: "border-l-blue-500",
  L2: "border-l-green-500",
  L3: "border-l-purple-500",
  L4: "border-l-orange-500",
  L5: "border-l-gray-500",
};

function RagIndicator({ status }: { status?: RagStatus }) {
  if (!status) return null;

  const icons = {
    red: <AlertCircle className="h-4 w-4 text-rag-red" />,
    amber: <MinusCircle className="h-4 w-4 text-rag-amber" />,
    green: <CheckCircle className="h-4 w-4 text-rag-green" />,
  };

  return icons[status] || null;
}

export function ProcessCard({
  process,
  onClick,
  isSelected = false,
  showChildren = false,
  size = "md",
}: ProcessCardProps) {
  const hasChildren = process.children && process.children.length > 0;

  return (
    <div
      className={cn(
        "rounded-lg border bg-card shadow-sm transition-all cursor-pointer hover:shadow-md border-l-4",
        levelColors[process.level] || "border-l-gray-400",
        isSelected && "ring-2 ring-primary",
        sizeClasses[size]
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-xs shrink-0">
              {process.code}
            </Badge>
            <RagIndicator status={process.metadata_extra?.rag_status as RagStatus} />
          </div>
          <h3 className="font-medium mt-1 truncate" title={process.name}>
            {process.name}
          </h3>
          {process.description && size !== "sm" && (
            <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
              {process.description}
            </p>
          )}
        </div>
        {hasChildren && (
          <ChevronRight className="h-4 w-4 text-muted-foreground shrink-0" />
        )}
      </div>

      {size !== "sm" && (
        <div className="flex items-center gap-2 mt-2">
          <Badge
            variant={process.status === "active" ? "success" : "secondary"}
            className="text-xs"
          >
            {process.status}
          </Badge>
          <Badge variant="outline" className="text-xs">
            {process.level}
          </Badge>
          {process.current_automation !== "manual" && (
            <Badge variant="outline" className="text-xs">
              {process.current_automation.replace("_", " ")}
            </Badge>
          )}
        </div>
      )}
    </div>
  );
}

export function ProcessCardSkeleton({ size = "md" }: { size?: "sm" | "md" | "lg" }) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-card shadow-sm border-l-4 border-l-gray-200 animate-pulse",
        sizeClasses[size]
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <div className="h-5 w-16 bg-muted rounded" />
          </div>
          <div className="h-5 w-3/4 bg-muted rounded mt-2" />
          {size !== "sm" && <div className="h-4 w-full bg-muted rounded mt-2" />}
        </div>
      </div>
      {size !== "sm" && (
        <div className="flex items-center gap-2 mt-2">
          <div className="h-5 w-16 bg-muted rounded" />
          <div className="h-5 w-12 bg-muted rounded" />
        </div>
      )}
    </div>
  );
}
