"use client";

import * as React from "react";
import { format } from "date-fns";
import { Edit, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  SlideOver,
  SlideOverSection,
  SlideOverField,
  SlideOverGrid,
} from "@/components/shared/SlideOver";
import { useRiadaByProcess } from "@/hooks/useRiada";
import type { Process, RiadaItem } from "@/types/api";

interface ProcessDetailPanelProps {
  process: Process | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onEdit?: (process: Process) => void;
  onDelete?: (process: Process) => void;
}

function RiadaSummary({ items }: { items: RiadaItem[] }) {
  const byType = {
    risk: items.filter((i) => i.riada_type === "risk"),
    issue: items.filter((i) => i.riada_type === "issue"),
    action: items.filter((i) => i.riada_type === "action"),
    dependency: items.filter((i) => i.riada_type === "dependency"),
    assumption: items.filter((i) => i.riada_type === "assumption"),
  };

  return (
    <div className="space-y-4">
      {Object.entries(byType).map(([type, typeItems]) => {
        if (typeItems.length === 0) return null;
        const openItems = typeItems.filter((i) => i.status === "open" || i.status === "in_progress");

        return (
          <div key={type} className="flex items-center justify-between">
            <span className="capitalize font-medium">{type}s</span>
            <div className="flex items-center gap-2">
              <Badge variant="secondary">{typeItems.length} total</Badge>
              {openItems.length > 0 && (
                <Badge variant={type === "risk" || type === "issue" ? "danger" : "warning"}>
                  {openItems.length} open
                </Badge>
              )}
            </div>
          </div>
        );
      })}
      {items.length === 0 && (
        <p className="text-sm text-muted-foreground">No RIADA items linked</p>
      )}
    </div>
  );
}

export function ProcessDetailPanel({
  process,
  open,
  onOpenChange,
  onEdit,
  onDelete,
}: ProcessDetailPanelProps) {
  const { data: riadaItems } = useRiadaByProcess(process?.id);

  if (!process) return null;

  const tabs = [
    {
      id: "details",
      label: "Details",
      content: (
        <div className="space-y-6">
          <SlideOverSection title="Basic Information">
            <SlideOverGrid>
              <SlideOverField label="Code" value={process.code} />
              <SlideOverField label="Level" value={process.level} />
              <SlideOverField label="Type" value={process.process_type} />
              <SlideOverField
                label="Status"
                value={
                  <Badge
                    variant={process.status === "active" ? "success" : "secondary"}
                  >
                    {process.status}
                  </Badge>
                }
              />
            </SlideOverGrid>
          </SlideOverSection>

          {process.description && (
            <SlideOverSection title="Description">
              <p className="text-sm">{process.description}</p>
            </SlideOverSection>
          )}

          <SlideOverSection title="Automation">
            <SlideOverGrid>
              <SlideOverField
                label="Current"
                value={process.current_automation.replace("_", " ")}
              />
              <SlideOverField
                label="Target"
                value={process.target_automation?.replace("_", " ") || "Not set"}
              />
            </SlideOverGrid>
            {process.automation_notes && (
              <p className="text-sm text-muted-foreground mt-2">
                {process.automation_notes}
              </p>
            )}
          </SlideOverSection>

          {(process.created_at || process.updated_at) && (
            <SlideOverSection title="Metadata">
              <SlideOverGrid>
                {process.created_at && (
                  <SlideOverField
                    label="Created"
                    value={format(new Date(process.created_at), "PPP")}
                  />
                )}
                {process.updated_at && (
                  <SlideOverField
                    label="Updated"
                    value={format(new Date(process.updated_at), "PPP")}
                  />
                )}
              </SlideOverGrid>
            </SlideOverSection>
          )}
        </div>
      ),
    },
    {
      id: "operating-model",
      label: "Operating Model",
      content: (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Operating model components (RACI, KPIs, SIPOC, etc.) will be shown here.
          </p>
          {/* TODO: Fetch and display ProcessOperatingModel components */}
        </div>
      ),
    },
    {
      id: "riada",
      label: "RIADA",
      content: <RiadaSummary items={riadaItems || []} />,
    },
  ];

  return (
    <SlideOver
      open={open}
      onOpenChange={onOpenChange}
      title={process.name}
      description={`${process.code} — ${process.level}`}
      tabs={tabs}
      size="lg"
      footer={
        <div className="flex items-center gap-2 w-full justify-end">
          {onDelete && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onDelete(process)}
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete
            </Button>
          )}
          {onEdit && (
            <Button size="sm" onClick={() => onEdit(process)}>
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </Button>
          )}
        </div>
      }
    />
  );
}
