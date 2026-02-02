"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ColumnDef } from "@tanstack/react-table";
import { MoreHorizontal, Plus, Eye, Edit, Trash2, LayoutGrid } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";
import { ProcessDetailPanel } from "@/components/process/ProcessDetailPanel";
import { ProcessForm } from "@/components/process/ProcessForm";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useProcesses, useCreateProcess, useUpdateProcess, useDeleteProcess } from "@/hooks/useProcesses";
import type { Process, ProcessLevel, ProcessType, LifecycleStatus } from "@/types/api";

const levelColors: Record<ProcessLevel, string> = {
  L0: "bg-brand-100 text-brand-800",
  L1: "bg-blue-100 text-blue-800",
  L2: "bg-green-100 text-green-800",
  L3: "bg-purple-100 text-purple-800",
  L4: "bg-orange-100 text-orange-800",
  L5: "bg-gray-100 text-gray-800",
};

const statusVariants: Record<LifecycleStatus, "success" | "secondary" | "warning" | "danger"> = {
  draft: "secondary",
  active: "success",
  under_review: "warning",
  deprecated: "danger",
  archived: "secondary",
};

export default function ProcessListPage() {
  const router = useRouter();
  const [levelFilter, setLevelFilter] = React.useState<ProcessLevel | "all">("all");
  const [typeFilter, setTypeFilter] = React.useState<ProcessType | "all">("all");
  const [statusFilter, setStatusFilter] = React.useState<LifecycleStatus | "all">("all");

  const filters = {
    level: levelFilter !== "all" ? levelFilter : undefined,
    process_type: typeFilter !== "all" ? typeFilter : undefined,
    status: statusFilter !== "all" ? statusFilter : undefined,
  };

  const { data, isLoading } = useProcesses(filters);
  const createProcess = useCreateProcess();
  const updateProcess = useUpdateProcess();
  const deleteProcess = useDeleteProcess();

  const [selectedProcess, setSelectedProcess] = React.useState<Process | null>(null);
  const [createDialogOpen, setCreateDialogOpen] = React.useState(false);
  const [editProcess, setEditProcess] = React.useState<Process | null>(null);

  const columns: ColumnDef<Process>[] = [
    {
      accessorKey: "code",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Code" />,
      cell: ({ row }) => (
        <span className="font-mono text-sm">{row.getValue("code")}</span>
      ),
    },
    {
      accessorKey: "name",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
      cell: ({ row }) => (
        <span className="font-medium">{row.getValue("name")}</span>
      ),
    },
    {
      accessorKey: "level",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Level" />,
      cell: ({ row }) => {
        const level = row.getValue("level") as ProcessLevel;
        return (
          <Badge className={levelColors[level]} variant="outline">
            {level}
          </Badge>
        );
      },
    },
    {
      accessorKey: "process_type",
      header: "Type",
      cell: ({ row }) => (
        <span className="capitalize">{row.getValue("process_type")}</span>
      ),
    },
    {
      accessorKey: "status",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.getValue("status") as LifecycleStatus;
        return (
          <Badge variant={statusVariants[status]} className="capitalize">
            {status.replace("_", " ")}
          </Badge>
        );
      },
    },
    {
      accessorKey: "current_automation",
      header: "Automation",
      cell: ({ row }) => (
        <span className="capitalize text-sm text-muted-foreground">
          {(row.getValue("current_automation") as string).replace("_", " ")}
        </span>
      ),
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const process = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setSelectedProcess(process)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setEditProcess(process)}>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => deleteProcess.mutate(process.id)}
                className="text-destructive"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const handleCreateSubmit = async (data: Parameters<typeof createProcess.mutateAsync>[0]) => {
    await createProcess.mutateAsync(data);
    setCreateDialogOpen(false);
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Process Catalogue</h1>
          <p className="text-muted-foreground mt-1">
            Manage your organization's process hierarchy
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" asChild>
            <Link href="/processes/canvas">
              <LayoutGrid className="h-4 w-4 mr-2" />
              Canvas View
            </Link>
          </Button>
          <Button onClick={() => setCreateDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Create Process
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <Select
          value={levelFilter}
          onValueChange={(v) => setLevelFilter(v as ProcessLevel | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Level" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Levels</SelectItem>
            <SelectItem value="L0">L0 - Value Stream</SelectItem>
            <SelectItem value="L1">L1 - Process Group</SelectItem>
            <SelectItem value="L2">L2 - Process</SelectItem>
            <SelectItem value="L3">L3 - Sub-Process</SelectItem>
            <SelectItem value="L4">L4 - Variation</SelectItem>
            <SelectItem value="L5">L5 - Task</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={typeFilter}
          onValueChange={(v) => setTypeFilter(v as ProcessType | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="primary">Primary</SelectItem>
            <SelectItem value="secondary">Secondary</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={statusFilter}
          onValueChange={(v) => setStatusFilter(v as LifecycleStatus | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value="draft">Draft</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="under_review">Under Review</SelectItem>
            <SelectItem value="deprecated">Deprecated</SelectItem>
            <SelectItem value="archived">Archived</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={data?.items || []}
        isLoading={isLoading}
        searchKey="name"
        searchPlaceholder="Search processes..."
        enableRowSelection
        enableExport
        onRowClick={setSelectedProcess}
      />

      {/* Detail Panel */}
      <ProcessDetailPanel
        process={selectedProcess}
        open={!!selectedProcess}
        onOpenChange={(open) => !open && setSelectedProcess(null)}
        onEdit={setEditProcess}
        onDelete={(p) => {
          deleteProcess.mutate(p.id);
          setSelectedProcess(null);
        }}
      />

      {/* Create Dialog */}
      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Create Process</DialogTitle>
          </DialogHeader>
          <ProcessForm
            onSubmit={handleCreateSubmit}
            onCancel={() => setCreateDialogOpen(false)}
            isSubmitting={createProcess.isPending}
          />
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={!!editProcess} onOpenChange={(open) => !open && setEditProcess(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Edit Process</DialogTitle>
          </DialogHeader>
          {editProcess && (
            <ProcessForm
              defaultValues={editProcess}
              onSubmit={async (data) => {
                await updateProcess.mutateAsync({ id: editProcess.id, data });
                setEditProcess(null);
              }}
              onCancel={() => setEditProcess(null)}
              isSubmitting={updateProcess.isPending}
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
