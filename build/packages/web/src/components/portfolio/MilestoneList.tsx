"use client";

import * as React from "react";
import { format } from "date-fns";
import { Plus, Edit, Trash2, CheckCircle2, Circle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MilestoneForm } from "@/components/portfolio/MilestoneForm";
import {
  useCreateMilestone,
  useUpdateMilestone,
  useDeleteMilestone,
} from "@/hooks/usePortfolioMilestones";
import type { PortfolioMilestone } from "@/types/api";

const statusConfig: Record<string, { icon: typeof Circle; variant: "success" | "secondary" | "warning" }> = {
  pending: { icon: Circle, variant: "secondary" },
  in_progress: { icon: Circle, variant: "warning" },
  completed: { icon: CheckCircle2, variant: "success" },
};

interface MilestoneListProps {
  portfolioItemId: string;
  milestones: PortfolioMilestone[];
}

export function MilestoneList({ portfolioItemId, milestones }: MilestoneListProps) {
  const [showCreate, setShowCreate] = React.useState(false);
  const [editing, setEditing] = React.useState<PortfolioMilestone | null>(null);

  const createMilestone = useCreateMilestone();
  const updateMilestone = useUpdateMilestone();
  const deleteMilestone = useDeleteMilestone();

  function handleCreate(values: { name: string; description?: string; due_date?: string }) {
    createMilestone.mutate(
      { portfolio_item_id: portfolioItemId, ...values },
      { onSuccess: () => setShowCreate(false) }
    );
  }

  function handleUpdate(values: { name: string; description?: string; due_date?: string }) {
    if (!editing) return;
    updateMilestone.mutate(
      { id: editing.id, data: values },
      { onSuccess: () => setEditing(null) }
    );
  }

  function handleToggleStatus(ms: PortfolioMilestone) {
    const newStatus = ms.status === "completed" ? "pending" : "completed";
    const data: Record<string, string> = { status: newStatus };
    if (newStatus === "completed") {
      data.completed_date = new Date().toISOString().split("T")[0];
    }
    updateMilestone.mutate({ id: ms.id, data });
  }

  return (
    <div className="space-y-3">
      {milestones.length === 0 ? (
        <p className="text-sm text-muted-foreground py-4 text-center">No milestones yet.</p>
      ) : (
        <div className="space-y-2">
          {milestones.map((ms) => {
            const config = statusConfig[ms.status] || statusConfig.pending;
            const StatusIcon = config.icon;
            return (
              <div key={ms.id} className="flex items-center gap-3 py-2 px-3 border rounded-md group">
                <button onClick={() => handleToggleStatus(ms)} className="shrink-0">
                  <StatusIcon className={`h-5 w-5 ${ms.status === "completed" ? "text-green-600" : "text-muted-foreground"}`} />
                </button>
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-medium ${ms.status === "completed" ? "line-through text-muted-foreground" : ""}`}>
                    {ms.name}
                  </p>
                  {ms.due_date && (
                    <p className="text-xs text-muted-foreground">
                      Due {format(new Date(ms.due_date), "MMM d, yyyy")}
                    </p>
                  )}
                </div>
                <Badge variant={config.variant} className="text-xs capitalize shrink-0">
                  {ms.status.replace("_", " ")}
                </Badge>
                <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <Button variant="ghost" size="sm" className="h-7 w-7 p-0" onClick={() => setEditing(ms)}>
                    <Edit className="h-3.5 w-3.5" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-7 w-7 p-0 text-destructive"
                    onClick={() => deleteMilestone.mutate(ms.id)}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <Button variant="outline" size="sm" onClick={() => setShowCreate(true)}>
        <Plus className="h-4 w-4 mr-2" />
        Add Milestone
      </Button>

      <MilestoneForm
        open={showCreate}
        onOpenChange={setShowCreate}
        onSubmit={handleCreate}
        isPending={createMilestone.isPending}
      />

      {editing && (
        <MilestoneForm
          open={!!editing}
          onOpenChange={(open) => !open && setEditing(null)}
          onSubmit={handleUpdate}
          initialData={editing}
          isPending={updateMilestone.isPending}
        />
      )}
    </div>
  );
}
