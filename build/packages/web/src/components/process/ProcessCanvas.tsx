"use client";

import * as React from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProcessCard, ProcessCardSkeleton } from "./ProcessCard";
import { ProcessCanvasToolbar } from "./ProcessCanvasToolbar";
import { ExpandableL2Card } from "./ExpandableProcessCards";
import type { Process, ProcessType, LifecycleStatus } from "@/types/api";

interface ProcessCanvasProps {
  processes: Process[];
  isLoading?: boolean;
  onProcessClick?: (process: Process) => void;
  onCreateProcess?: (level: string, parentId?: string) => void;
  selectedProcessId?: string;
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

  // Filter L0 processes
  const filteredL0 = React.useMemo(() => {
    return processes
      .filter((p) => p.level === "L0")
      .filter((p) => {
        if (search && !p.name.toLowerCase().includes(search.toLowerCase()) && !p.code.toLowerCase().includes(search.toLowerCase())) {
          return false;
        }
        if (processType !== "all" && p.process_type !== processType) {
          return false;
        }
        if (statusFilter.length > 0 && !statusFilter.includes(p.status as LifecycleStatus)) {
          return false;
        }
        return true;
      });
  }, [processes, search, processType, statusFilter]);

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
        <div className="flex-1 overflow-x-auto p-6 bg-slate-50">
          <div className="flex gap-8">
            {[1, 2].map((i) => (
              <div key={i} className="min-w-[700px]">
                <ProcessCardSkeleton variant="l0" />
                <div className="flex gap-6 mt-4">
                  {[1, 2, 3].map((j) => (
                    <div key={j} className="w-64 space-y-3">
                      <ProcessCardSkeleton variant="l1" />
                      <ProcessCardSkeleton variant="l2" />
                      <ProcessCardSkeleton variant="l2" />
                    </div>
                  ))}
                </div>
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

      {/* Main canvas area */}
      <div
        className="flex-1 overflow-x-auto p-6 bg-slate-50"
        style={{ transform: `scale(${zoom})`, transformOrigin: "top left" }}
      >
        {filteredL0.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-center">
            <p className="text-slate-500 mb-4">No processes found</p>
            {onCreateProcess && (
              <Button onClick={() => onCreateProcess("L0")}>
                <Plus className="h-4 w-4 mr-2" />
                Create Value Stream
              </Button>
            )}
          </div>
        ) : (
          <div className="flex gap-8">
            {/* L0 Swimlanes */}
            {filteredL0.map((l0Process) => {
              const l1Children = l0Process.children || [];

              return (
                <div key={l0Process.id} className="min-w-[700px] flex-shrink-0">
                  {/* L0 Header */}
                  <ProcessCard
                    process={l0Process}
                    variant="l0"
                    isSelected={selectedProcessId === l0Process.id}
                    showInfoButton
                    onInfoClick={() => onProcessClick?.(l0Process)}
                  />

                  {/* L1 Columns */}
                  <div className="flex gap-6 mt-4">
                    {l1Children.map((l1Process) => {
                      const l2Children = l1Process.children || [];

                      return (
                        <div key={l1Process.id} className="w-64 flex-shrink-0">
                          {/* L1 Header */}
                          <div className="mb-3">
                            <ProcessCard
                              process={l1Process}
                              variant="l1"
                              isSelected={selectedProcessId === l1Process.id}
                              onClick={() => onProcessClick?.(l1Process)}
                            />
                          </div>

                          {/* L2 Cards */}
                          <div className="space-y-2">
                            {l2Children.map((l2Process) => (
                              <ExpandableL2Card
                                key={l2Process.id}
                                process={l2Process}
                                onProcessClick={onProcessClick}
                                selectedProcessId={selectedProcessId}
                              />
                            ))}

                            {/* Add L2 button */}
                            {onCreateProcess && (
                              <button
                                className="w-full py-2 px-3 text-sm text-slate-400 hover:text-slate-600 hover:bg-white rounded-lg border border-dashed border-slate-200 transition-colors"
                                onClick={() => onCreateProcess("L2", l1Process.id)}
                              >
                                <Plus className="h-4 w-4 inline mr-1" />
                                Add Process
                              </button>
                            )}
                          </div>
                        </div>
                      );
                    })}

                    {/* Add L1 Column */}
                    {onCreateProcess && (
                      <div className="w-64 flex-shrink-0">
                        <button
                          className="w-full pb-2 border-b border-dashed border-slate-200 text-sm text-slate-400 hover:text-slate-600 uppercase tracking-wide transition-colors"
                          onClick={() => onCreateProcess("L1", l0Process.id)}
                        >
                          <Plus className="h-4 w-4 inline mr-1" />
                          Add Column
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {/* Add L0 Swimlane */}
            {onCreateProcess && (
              <div className="min-w-[700px] flex-shrink-0">
                <button
                  className="w-full p-4 text-slate-400 hover:text-slate-600 hover:bg-white rounded-lg border border-dashed border-slate-200 transition-colors"
                  onClick={() => onCreateProcess("L0")}
                >
                  <Plus className="h-5 w-5 inline mr-2" />
                  <span className="text-lg font-bold uppercase">Add Value Stream</span>
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
