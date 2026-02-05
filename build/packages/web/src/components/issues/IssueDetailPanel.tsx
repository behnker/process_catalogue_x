import { format } from "date-fns";
import { Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { SlideOverSection, SlideOverField, SlideOverGrid } from "@/components/shared/SlideOver";
import { IssueStatusBadge } from "@/components/issues/IssueStatusBadge";
import { CriticalityBadge } from "@/components/issues/CriticalityBadge";
import { ClassificationIcon } from "@/components/issues/ClassificationIcon";
import type { Issue } from "@/types/issue.types";

interface IssueDetailPanelProps {
  issue: Issue;
  onEdit: (issue: Issue) => void;
}

export function IssueDetailPanel({ issue, onEdit }: IssueDetailPanelProps) {
  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <Button variant="outline" size="sm" onClick={() => onEdit(issue)}>
          <Edit className="h-4 w-4 mr-2" />
          Edit Issue
        </Button>
      </div>

      <SlideOverSection title="Classification">
        <SlideOverGrid>
          <SlideOverField
            label="Classification"
            value={
              <ClassificationIcon
                classification={issue.issue_classification}
                showLabel
              />
            }
          />
          <SlideOverField
            label="Criticality"
            value={<CriticalityBadge criticality={issue.issue_criticality} />}
          />
          <SlideOverField
            label="Complexity"
            value={<Badge variant="outline" className="capitalize">{issue.issue_complexity}</Badge>}
          />
          <SlideOverField
            label="Status"
            value={<IssueStatusBadge status={issue.issue_status} />}
          />
        </SlideOverGrid>
      </SlideOverSection>

      {issue.description && (
        <SlideOverSection title="Description">
          <p className="text-sm whitespace-pre-wrap">{issue.description}</p>
        </SlideOverSection>
      )}

      <SlideOverSection title="Process">
        <SlideOverGrid cols={2}>
          <SlideOverField label="Process Ref" value={issue.process_ref} />
          <SlideOverField label="Process Name" value={issue.process_name} />
        </SlideOverGrid>
      </SlideOverSection>

      <SlideOverSection title="Timeline">
        <SlideOverGrid cols={3}>
          <SlideOverField
            label="Date Raised"
            value={format(new Date(issue.date_raised), "MMMM d, yyyy")}
          />
          <SlideOverField
            label="Target Date"
            value={issue.target_resolution_date
              ? format(new Date(issue.target_resolution_date), "MMMM d, yyyy")
              : "—"
            }
          />
          <SlideOverField
            label="Resolved Date"
            value={issue.actual_resolution_date
              ? format(new Date(issue.actual_resolution_date), "MMMM d, yyyy")
              : "—"
            }
          />
        </SlideOverGrid>
      </SlideOverSection>

      {issue.resolution_summary && (
        <SlideOverSection title="Resolution">
          <p className="text-sm">{issue.resolution_summary}</p>
        </SlideOverSection>
      )}

      {issue.opportunity_flag && (
        <SlideOverSection title="Opportunity">
          <SlideOverGrid>
            <SlideOverField
              label="Status"
              value={
                <Badge variant="outline" className="capitalize">
                  {issue.opportunity_status?.replace("_", " ") || "Identified"}
                </Badge>
              }
            />
          </SlideOverGrid>
          {issue.opportunity_description && (
            <div className="mt-4">
              <span className="text-sm text-muted-foreground">Description</span>
              <p className="text-sm mt-1">{issue.opportunity_description}</p>
            </div>
          )}
          {issue.opportunity_expected_benefit && (
            <div className="mt-4">
              <span className="text-sm text-muted-foreground">Expected Benefit</span>
              <p className="text-sm mt-1">{issue.opportunity_expected_benefit}</p>
            </div>
          )}
        </SlideOverSection>
      )}
    </div>
  );
}
