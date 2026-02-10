"use client";

import { useRouter } from "next/navigation";
import { format } from "date-fns";
import { Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SlideOver, SlideOverSection, SlideOverField, SlideOverGrid } from "@/components/shared/SlideOver";
import { statusVariants, ragColors } from "@/components/portfolio/PortfolioTreeNode";
import type { PortfolioItem } from "@/types/api";
import { cn } from "@/lib/utils";

interface PortfolioDetailPanelProps {
  item: PortfolioItem | null;
  onClose: () => void;
}

export function PortfolioDetailPanel({ item, onClose }: PortfolioDetailPanelProps) {
  const router = useRouter();

  return (
    <SlideOver
      open={!!item}
      onOpenChange={(open) => !open && onClose()}
      title={item?.name || ""}
      description={item ? `${item.code} — ${item.level}` : ""}
      size="lg"
    >
      {item && (
        <div className="space-y-6">
          <div className="flex justify-end">
            <Button variant="outline" size="sm" onClick={() => router.push(`/portfolio/${item.id}/edit`)}>
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </Button>
          </div>

          <SlideOverSection title="Status">
            <SlideOverGrid>
              <SlideOverField
                label="Status"
                value={
                  <Badge variant={statusVariants[item.status]} className="capitalize">
                    {item.status.replace("_", " ")}
                  </Badge>
                }
              />
              <SlideOverField
                label="RAG"
                value={
                  item.rag_status ? (
                    <div className="flex items-center gap-2">
                      <div className={cn("w-4 h-4 rounded-full", ragColors[item.rag_status])} />
                      <span className="capitalize">{item.rag_status}</span>
                    </div>
                  ) : (
                    "—"
                  )
                }
              />
            </SlideOverGrid>
          </SlideOverSection>

          {item.description && (
            <SlideOverSection title="Description">
              <p className="text-sm">{item.description}</p>
            </SlideOverSection>
          )}

          <SlideOverSection title="Timeline">
            <SlideOverGrid>
              <SlideOverField
                label="Planned Start"
                value={item.planned_start ? format(new Date(item.planned_start), "MMM d, yyyy") : "—"}
              />
              <SlideOverField
                label="Planned End"
                value={item.planned_end ? format(new Date(item.planned_end), "MMM d, yyyy") : "—"}
              />
              <SlideOverField
                label="Actual Start"
                value={item.actual_start ? format(new Date(item.actual_start), "MMM d, yyyy") : "—"}
              />
              <SlideOverField
                label="Actual End"
                value={item.actual_end ? format(new Date(item.actual_end), "MMM d, yyyy") : "—"}
              />
            </SlideOverGrid>
          </SlideOverSection>

          {(item.budget_approved || item.budget_spent) && (
            <SlideOverSection title="Budget">
              <SlideOverGrid cols={3}>
                <SlideOverField
                  label="Approved"
                  value={item.budget_approved ? `${item.budget_currency} ${item.budget_approved.toLocaleString()}` : "—"}
                />
                <SlideOverField
                  label="Spent"
                  value={item.budget_spent ? `${item.budget_currency} ${item.budget_spent.toLocaleString()}` : "—"}
                />
                <SlideOverField
                  label="Forecast"
                  value={item.budget_forecast ? `${item.budget_currency} ${item.budget_forecast.toLocaleString()}` : "—"}
                />
              </SlideOverGrid>
            </SlideOverSection>
          )}

          {item.wsvf_score && (
            <SlideOverSection title="WSVF Prioritization">
              <SlideOverGrid>
                <SlideOverField label="Business Value" value={item.business_value || "—"} />
                <SlideOverField label="Time Criticality" value={item.time_criticality || "—"} />
                <SlideOverField label="Risk Reduction" value={item.risk_reduction || "—"} />
                <SlideOverField label="Job Size" value={item.job_size || "—"} />
              </SlideOverGrid>
              <div className="mt-4 p-3 bg-muted rounded-md">
                <span className="text-sm text-muted-foreground">WSVF Score</span>
                <p className="text-2xl font-semibold">{item.wsvf_score.toFixed(2)}</p>
              </div>
            </SlideOverSection>
          )}

          {item.milestones && item.milestones.length > 0 && (
            <SlideOverSection title="Milestones">
              <div className="space-y-2">
                {item.milestones.map((ms) => (
                  <div key={ms.id} className="flex items-center justify-between py-2 px-3 border rounded-md">
                    <div>
                      <p className="text-sm font-medium">{ms.name}</p>
                      {ms.due_date && (
                        <p className="text-xs text-muted-foreground">
                          Due {format(new Date(ms.due_date), "MMM d, yyyy")}
                        </p>
                      )}
                    </div>
                    <Badge variant={ms.status === "completed" ? "success" : "secondary"} className="text-xs capitalize">
                      {ms.status.replace("_", " ")}
                    </Badge>
                  </div>
                ))}
              </div>
            </SlideOverSection>
          )}
        </div>
      )}
    </SlideOver>
  );
}
