"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { ProcessCanvas } from "@/components/process/ProcessCanvas";
import { ProcessDetailPanel } from "@/components/process/ProcessDetailPanel";
import { ProcessForm } from "@/components/process/ProcessForm";
import { useProcessTree, useCreateProcess } from "@/hooks/useProcesses";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import type { Process, ProcessLevel } from "@/types/api";

export default function ProcessCanvasPage() {
  const router = useRouter();
  const { data: processes, isLoading } = useProcessTree();
  const createProcess = useCreateProcess();

  const [selectedProcess, setSelectedProcess] = React.useState<Process | null>(null);
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false);
  const [createLevel, setCreateLevel] = React.useState<ProcessLevel>("L0");
  const [createParentId, setCreateParentId] = React.useState<string | undefined>();

  const handleProcessClick = (process: Process) => {
    setSelectedProcess(process);
  };

  const handleCreateProcess = (level: string, parentId?: string) => {
    setCreateLevel(level as ProcessLevel);
    setCreateParentId(parentId);
    setCreateDialogOpen(true);
  };

  const handleFormSubmit = async (data: Parameters<typeof createProcess.mutateAsync>[0]) => {
    await createProcess.mutateAsync(data);
    setCreateDialogOpen(false);
  };

  return (
    <div className="h-[calc(100vh-var(--header-height))] flex flex-col">
      <ProcessCanvas
        processes={processes || []}
        isLoading={isLoading}
        onProcessClick={handleProcessClick}
        onCreateProcess={handleCreateProcess}
        selectedProcessId={selectedProcess?.id}
      />

      {/* Detail Panel */}
      <ProcessDetailPanel
        process={selectedProcess}
        open={!!selectedProcess}
        onOpenChange={(open) => !open && setSelectedProcess(null)}
      />

      {/* Create Dialog */}
      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Create {createLevel} Process</DialogTitle>
          </DialogHeader>
          <ProcessForm
            defaultValues={{
              level: createLevel,
              parent_id: createParentId,
            }}
            onSubmit={handleFormSubmit}
            onCancel={() => setCreateDialogOpen(false)}
            isSubmitting={createProcess.isPending}
          />
        </DialogContent>
      </Dialog>
    </div>
  );
}
