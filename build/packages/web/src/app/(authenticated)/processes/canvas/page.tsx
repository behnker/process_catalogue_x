"use client";

import * as React from "react";
import { ProcessCanvas } from "@/components/process/ProcessCanvas";
import { ProcessDetailModal } from "@/components/process/ProcessDetailModal";
import { ProcessForm } from "@/components/process/ProcessForm";
import { useProcessTree, useCreateProcess, useDeleteProcess, useUpdateProcess } from "@/hooks/useProcesses";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import type { Process, ProcessLevel } from "@/types/api";

export default function ProcessCanvasPage() {
  const { data: processes, isLoading } = useProcessTree();
  const createProcess = useCreateProcess();
  const deleteProcess = useDeleteProcess();
  const updateProcess = useUpdateProcess();

  const [selectedProcess, setSelectedProcess] = React.useState<Process | null>(null);
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false);
  const [createLevel, setCreateLevel] = React.useState<ProcessLevel>("L0");
  const [createParentId, setCreateParentId] = React.useState<string | undefined>();
  const [deleteDialogOpen, setDeleteDialogOpen] = React.useState(false);
  const [processToDelete, setProcessToDelete] = React.useState<Process | null>(null);
  const [editDialogOpen, setEditDialogOpen] = React.useState(false);
  const [processToEdit, setProcessToEdit] = React.useState<Process | null>(null);

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

  const handleDeleteClick = (process: Process) => {
    setProcessToDelete(process);
    setDeleteDialogOpen(true);
    setSelectedProcess(null);
  };

  const handleDeleteConfirm = async () => {
    if (processToDelete) {
      await deleteProcess.mutateAsync(processToDelete.id);
      setDeleteDialogOpen(false);
      setProcessToDelete(null);
    }
  };

  const handleEditClick = (process: Process) => {
    setProcessToEdit(process);
    setEditDialogOpen(true);
    setSelectedProcess(null);
  };

  const handleEditSubmit = async (data: Parameters<typeof createProcess.mutateAsync>[0]) => {
    if (processToEdit) {
      await updateProcess.mutateAsync({
        id: processToEdit.id,
        data: {
          name: data.name,
          description: data.description,
          status: data.status,
          current_automation: data.current_automation,
          target_automation: data.target_automation,
        },
      });
      setEditDialogOpen(false);
      setProcessToEdit(null);
    }
  };

  const handleAddChild = (level: string, parentId: string) => {
    setCreateLevel(level as ProcessLevel);
    setCreateParentId(parentId);
    setCreateDialogOpen(true);
    setSelectedProcess(null);
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

      {/* Detail Modal */}
      <ProcessDetailModal
        process={selectedProcess}
        open={!!selectedProcess}
        onClose={() => setSelectedProcess(null)}
        onEdit={handleEditClick}
        onDelete={handleDeleteClick}
        onAddChild={handleAddChild}
        onSelectProcess={handleProcessClick}
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

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Process</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{processToDelete?.name}" ({processToDelete?.code})?
              This will archive the process and renumber its siblings.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteConfirm}
              disabled={deleteProcess.isPending}
            >
              {deleteProcess.isPending ? "Deleting..." : "Delete"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Edit Process: {processToEdit?.code}</DialogTitle>
          </DialogHeader>
          {processToEdit && (
            <ProcessForm
              defaultValues={{
                name: processToEdit.name,
                description: processToEdit.description || undefined,
                level: processToEdit.level as ProcessLevel,
                parent_id: processToEdit.parent_id || undefined,
                process_type: processToEdit.process_type as "primary" | "secondary",
                status: processToEdit.status as any,
                current_automation: processToEdit.current_automation as any,
                target_automation: processToEdit.target_automation as any,
              }}
              onSubmit={handleEditSubmit}
              onCancel={() => setEditDialogOpen(false)}
              isSubmitting={updateProcess.isPending}
              lockLevel
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
