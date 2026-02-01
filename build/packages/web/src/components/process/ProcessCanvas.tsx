"use client";

import * as React from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProcessCard, ProcessCardSkeleton } from "./ProcessCard";
import { ProcessCanvasToolbar } from "./ProcessCanvasToolbar";
import { cn } from "@/lib/utils";
import type { Process, ProcessType, LifecycleStatus } from "@/types/api";

interface ProcessCanvasProps {
  processes: Process[];
  isLoading?: boolean;
  onProcessClick?: (process: Process) => void;
  onCreateProcess?: (level: string, parentId?: string) => void;
  selectedProcessId?: string;
}

// Group processes by level and parent
function groupProcesses(processes: Process[]) {
  const l0 = processes.filter((p) => p.level === "L0");
  const l1ByParent = new Map<string, Process[]>();
  const l2ByParent = new Map<string, Process[]>();

  processes
    .filter((p) => p.level === "L1")
    .forEach((p) => {
      const parentId = p.parent_id || "root";
      if (!l1ByParent.has(parentId)) l1ByParent.set(parentId, []);
      l1ByParent.get(parentId)!.push(p);
    });

  processes
    .filter((p) => p.level === "L2")
    .forEach((p) => {
      const parentId = p.parent_id || "root";
      if (!l2ByParent.has(parentId)) l2ByParent.set(parentId, []);
      l2ByParent.get(parentId)!.push(p);
    });

  return { l0, l1ByParent, l2ByParent };
}

export function ProcessCanvas({
  processes,
  isLoading = false,
  onProcessClick,
  onCreateProcess,
  selectedProcessId,
}: ProcessCanvasProps) {
  const [search, setSearch] = React.useState("");
  const [processType, setProcessType] = React.useState<ProcessType | "all">("all");
  const [statusFilter, setStatusFilter] = React.useState<LifecycleStatus[]>([]);
  const [cardSize, setCardSize] = React.useState<"sm" | "md" | "lg">("md");
  const [zoom, setZoom] = React.useState(1);

  // Filter processes
  const filteredProcesses = React.useMemo(() => {
    return processes.filter((p) => {
      // Search filter
      if (search && !p.name.toLowerCase().includes(search.toLowerCase()) && !p.code.toLowerCase().includes(search.toLowerCase())) {
        return false;
      }
      // Type filter
      if (processType !== "all" && p.process_type !== processType) {
        return false;
      }
      // Status filter
      if (statusFilter.length > 0 && !statusFilter.includes(p.status as LifecycleStatus)) {
        return false;
      }
      return true;
    });
  }, [processes, search, processType, statusFilter]);

  const { l0, l1ByParent, l2ByParent } = React.useMemo(
    () => groupProcesses(filteredProcesses),
    [filteredProcesses]
  );

  const handleZoomIn = () => setZoom((z) => Math.min(z + 0.1, 2));
  const handleZoomOut = () => setZoom((z) => Math.max(z - 0.1, 0.5));
  const handleResetZoom = () => setZoom(1);

  if (isLoading) {
    return (
      <div className="flex flex-col h-full">
        <ProcessCanvasToolbar
          search={search}
          onSearchChange={setSearch}
          processType={processType}
          onProcessTypeChange={setProcessType}
          statusFilter={statusFilter}
          onStatusFilterChange={setStatusFilter}
          cardSize={cardSize}
          onCardSizeChange={setCardSize}
          zoom={zoom}
          onZoomIn={handleZoomIn}
          onZoomOut={handleZoomOut}
          onResetZoom={handleResetZoom}
        />
        <div className="flex-1 overflow-auto p-4">
          <div className="flex gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="w-[300px] space-y-4">
                <ProcessCardSkeleton size={cardSize} />
                <ProcessCardSkeleton size={cardSize} />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <ProcessCanvasToolbar
        search={search}
        onSearchChange={setSearch}
        processType={processType}
        onProcessTypeChange={setProcessType}
        statusFilter={statusFilter}
        onStatusFilterChange={setStatusFilter}
        cardSize={cardSize}
        onCardSizeChange={setCardSize}
        zoom={zoom}
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onResetZoom={handleResetZoom}
      />

      <div
        className="flex-1 overflow-auto p-4"
        style={{ transform: `scale(${zoom})`, transformOrigin: "top left" }}
      >
        {l0.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-center">
            <p className="text-muted-foreground mb-4">No processes found</p>
            {onCreateProcess && (
              <Button onClick={() => onCreateProcess("L0")}>
                <Plus className="h-4 w-4 mr-2" />
                Create Value Stream
              </Button>
            )}
          </div>
        ) : (
          <div className="flex gap-6">
            {/* L0 Swimlanes */}
            {l0.map((l0Process) => {
              const l1Children = l1ByParent.get(l0Process.id) || [];

              return (
                <div
                  key={l0Process.id}
                  className="flex-shrink-0 w-[320px] bg-muted/30 rounded-lg border"
                >
                  {/* L0 Header */}
                  <div className="p-3 border-b bg-muted/50 rounded-t-lg">
                    <ProcessCard
                      process={l0Process}
                      onClick={() => onProcessClick?.(l0Process)}
                      isSelected={selectedProcessId === l0Process.id}
                      size="sm"
                    />
                  </div>

                  {/* L1 / L2 Content */}
                  <div className="p-3 space-y-3 max-h-[calc(100vh-300px)] overflow-y-auto">
                    {l1Children.map((l1Process) => {
                      const l2Children = l2ByParent.get(l1Process.id) || [];

                      return (
                        <div key={l1Process.id} className="space-y-2">
                          <ProcessCard
                            process={l1Process}
                            onClick={() => onProcessClick?.(l1Process)}
                            isSelected={selectedProcessId === l1Process.id}
                            size={cardSize}
                          />

                          {/* L2 nested under L1 */}
                          {l2Children.length > 0 && (
                            <div className="ml-4 space-y-2 border-l-2 border-muted pl-3">
                              {l2Children.map((l2Process) => (
                                <ProcessCard
                                  key={l2Process.id}
                                  process={l2Process}
                                  onClick={() => onProcessClick?.(l2Process)}
                                  isSelected={selectedProcessId === l2Process.id}
                                  size="sm"
                                />
                              ))}
                            </div>
                          )}
                        </div>
                      );
                    })}

                    {/* Add L1 button */}
                    {onCreateProcess && (
                      <Button
                        variant="ghost"
                        size="sm"
                        className="w-full border-2 border-dashed"
                        onClick={() => onCreateProcess("L1", l0Process.id)}
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Add Process Group
                      </Button>
                    )}
                  </div>
                </div>
              );
            })}

            {/* Add L0 Column */}
            {onCreateProcess && (
              <div className="flex-shrink-0 w-[320px] h-64 flex items-center justify-center border-2 border-dashed rounded-lg">
                <Button variant="ghost" onClick={() => onCreateProcess("L0")}>
                  <Plus className="h-4 w-4 mr-2" />
                  Add Value Stream
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
