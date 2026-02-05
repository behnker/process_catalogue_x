"use client";

import * as React from "react";
import { ColumnDef } from "@tanstack/react-table";
import { format } from "date-fns";
import {
  MoreHorizontal,
  Plus,
  Eye,
  Edit,
  Trash2,
  Download,
  BarChart3,
} from "lucide-react";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";
import { SlideOver, SlideOverSection, SlideOverField, SlideOverGrid } from "@/components/shared/SlideOver";
import { IssueStatusBadge } from "@/components/issues/IssueStatusBadge";
import { CriticalityBadge } from "@/components/issues/CriticalityBadge";
import { ClassificationIcon } from "@/components/issues/ClassificationIcon";
import { useIssues, useDeleteIssue, useIssueSummary, useExportIssues } from "@/hooks/useIssues";
import type { Issue, IssueStatus, IssueClassification, IssueCriticality } from "@/types/issue.types";

export default function IssuesPage() {
  const [statusFilter, setStatusFilter] = React.useState<IssueStatus | "all">("all");
  const [classFilter, setClassFilter] = React.useState<IssueClassification | "all">("all");
  const [critFilter, setCritFilter] = React.useState<IssueCriticality | "all">("all");
  const [selectedIssue, setSelectedIssue] = React.useState<Issue | null>(null);

  const filters = {
    status_filter: statusFilter !== "all" ? statusFilter : undefined,
    classification: classFilter !== "all" ? classFilter : undefined,
    criticality: critFilter !== "all" ? critFilter : undefined,
  };

  const { data, isLoading } = useIssues(filters);
  const { data: summary } = useIssueSummary();
  const deleteIssue = useDeleteIssue();
  const exportIssues = useExportIssues();

  const columns: ColumnDef<Issue>[] = [
    {
      accessorKey: "display_id",
      header: ({ column }) => <DataTableColumnHeader column={column} title="ID" />,
      cell: ({ row }) => (
        <span className="font-mono text-sm font-medium text-brand-600">
          {row.getValue("display_id")}
        </span>
      ),
    },
    {
      accessorKey: "title",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Title" />,
      cell: ({ row }) => (
        <span className="font-medium line-clamp-1">{row.getValue("title")}</span>
      ),
    },
    {
      accessorKey: "issue_classification",
      header: "Classification",
      cell: ({ row }) => (
        <ClassificationIcon
          classification={row.getValue("issue_classification")}
          showLabel
          size="sm"
        />
      ),
    },
    {
      accessorKey: "issue_criticality",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Criticality" />,
      cell: ({ row }) => (
        <CriticalityBadge criticality={row.getValue("issue_criticality")} />
      ),
    },
    {
      accessorKey: "issue_status",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => (
        <IssueStatusBadge status={row.getValue("issue_status")} />
      ),
    },
    {
      accessorKey: "process_ref",
      header: "Process",
      cell: ({ row }) => (
        <span className="text-sm text-muted-foreground">{row.getValue("process_ref")}</span>
      ),
    },
    {
      accessorKey: "date_raised",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Raised" />,
      cell: ({ row }) => {
        const date = row.getValue("date_raised") as string;
        return <span className="text-sm">{format(new Date(date), "MMM d, yyyy")}</span>;
      },
    },
    {
      accessorKey: "target_resolution_date",
      header: "Target",
      cell: ({ row }) => {
        const date = row.getValue("target_resolution_date") as string | null;
        if (!date) return <span className="text-muted-foreground">—</span>;
        const isOverdue = new Date(date) < new Date() &&
          !["resolved", "closed"].includes(row.original.issue_status);
        return (
          <span className={isOverdue ? "text-red-600 font-medium" : "text-sm"}>
            {format(new Date(date), "MMM d")}
          </span>
        );
      },
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const issue = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setSelectedIssue(issue)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => {/* TODO: edit */}}>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => deleteIssue.mutate(issue.id)}
                className="text-destructive"
                disabled={!["open", "deferred"].includes(issue.issue_status)}
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

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Issue Log</h1>
          <p className="text-muted-foreground mt-1">
            Operational issues linked to processes
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            onClick={() => exportIssues.mutate({ format: "csv" })}
            disabled={exportIssues.isPending}
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button onClick={() => {/* TODO: new issue drawer */}}>
            <Plus className="h-4 w-4 mr-2" />
            New Issue
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <SummaryCard
            label="Open"
            value={summary.total_open}
            variant="blue"
          />
          <SummaryCard
            label="In Progress"
            value={summary.total_in_progress}
            variant="amber"
          />
          <SummaryCard
            label="Overdue"
            value={summary.overdue_count}
            variant="red"
          />
          <SummaryCard
            label="Due This Week"
            value={summary.due_this_week}
            variant="purple"
          />
          <SummaryCard
            label="Opportunities"
            value={summary.opportunities_identified}
            variant="green"
          />
        </div>
      )}

      {/* Filters */}
      <div className="flex items-center gap-4">
        <Select
          value={statusFilter}
          onValueChange={(v) => setStatusFilter(v as IssueStatus | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value="open">Open</SelectItem>
            <SelectItem value="in_progress">In Progress</SelectItem>
            <SelectItem value="resolved">Resolved</SelectItem>
            <SelectItem value="closed">Closed</SelectItem>
            <SelectItem value="deferred">Deferred</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={classFilter}
          onValueChange={(v) => setClassFilter(v as IssueClassification | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Classification" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Classes</SelectItem>
            <SelectItem value="people">People</SelectItem>
            <SelectItem value="process">Process</SelectItem>
            <SelectItem value="system">System</SelectItem>
            <SelectItem value="data">Data</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={critFilter}
          onValueChange={(v) => setCritFilter(v as IssueCriticality | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Criticality" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Criticality</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="low">Low</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={data?.items || []}
        isLoading={isLoading}
        searchKey="title"
        searchPlaceholder="Search issues..."
        enableRowSelection
        onRowClick={setSelectedIssue}
      />

      {/* Detail Panel */}
      <SlideOver
        open={!!selectedIssue}
        onOpenChange={(open) => !open && setSelectedIssue(null)}
        title={selectedIssue?.display_id || ""}
        description={selectedIssue?.title || ""}
        size="lg"
      >
        {selectedIssue && (
          <div className="space-y-6">
            <SlideOverSection title="Classification">
              <SlideOverGrid>
                <SlideOverField
                  label="Classification"
                  value={
                    <ClassificationIcon
                      classification={selectedIssue.issue_classification}
                      showLabel
                    />
                  }
                />
                <SlideOverField
                  label="Criticality"
                  value={<CriticalityBadge criticality={selectedIssue.issue_criticality} />}
                />
                <SlideOverField
                  label="Complexity"
                  value={<Badge variant="outline" className="capitalize">{selectedIssue.issue_complexity}</Badge>}
                />
                <SlideOverField
                  label="Status"
                  value={<IssueStatusBadge status={selectedIssue.issue_status} />}
                />
              </SlideOverGrid>
            </SlideOverSection>

            {selectedIssue.description && (
              <SlideOverSection title="Description">
                <p className="text-sm whitespace-pre-wrap">{selectedIssue.description}</p>
              </SlideOverSection>
            )}

            <SlideOverSection title="Process">
              <SlideOverGrid cols={2}>
                <SlideOverField label="Process Ref" value={selectedIssue.process_ref} />
                <SlideOverField label="Process Name" value={selectedIssue.process_name} />
              </SlideOverGrid>
            </SlideOverSection>

            <SlideOverSection title="Timeline">
              <SlideOverGrid cols={3}>
                <SlideOverField
                  label="Date Raised"
                  value={format(new Date(selectedIssue.date_raised), "MMMM d, yyyy")}
                />
                <SlideOverField
                  label="Target Date"
                  value={selectedIssue.target_resolution_date
                    ? format(new Date(selectedIssue.target_resolution_date), "MMMM d, yyyy")
                    : "—"
                  }
                />
                <SlideOverField
                  label="Resolved Date"
                  value={selectedIssue.actual_resolution_date
                    ? format(new Date(selectedIssue.actual_resolution_date), "MMMM d, yyyy")
                    : "—"
                  }
                />
              </SlideOverGrid>
            </SlideOverSection>

            {selectedIssue.resolution_summary && (
              <SlideOverSection title="Resolution">
                <p className="text-sm">{selectedIssue.resolution_summary}</p>
              </SlideOverSection>
            )}

            {selectedIssue.opportunity_flag && (
              <SlideOverSection title="Opportunity">
                <SlideOverGrid>
                  <SlideOverField
                    label="Status"
                    value={
                      <Badge variant="outline" className="capitalize">
                        {selectedIssue.opportunity_status?.replace("_", " ") || "Identified"}
                      </Badge>
                    }
                  />
                </SlideOverGrid>
                {selectedIssue.opportunity_description && (
                  <div className="mt-4">
                    <span className="text-sm text-muted-foreground">Description</span>
                    <p className="text-sm mt-1">{selectedIssue.opportunity_description}</p>
                  </div>
                )}
                {selectedIssue.opportunity_expected_benefit && (
                  <div className="mt-4">
                    <span className="text-sm text-muted-foreground">Expected Benefit</span>
                    <p className="text-sm mt-1">{selectedIssue.opportunity_expected_benefit}</p>
                  </div>
                )}
              </SlideOverSection>
            )}
          </div>
        )}
      </SlideOver>
    </div>
  );
}

function SummaryCard({
  label,
  value,
  variant,
}: {
  label: string;
  value: number;
  variant: "blue" | "amber" | "red" | "purple" | "green";
}) {
  const colors = {
    blue: "bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800",
    amber: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800",
    red: "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800",
    purple: "bg-purple-50 dark:bg-purple-950/30 border-purple-200 dark:border-purple-800",
    green: "bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800",
  };

  return (
    <div className={`rounded-lg border p-4 ${colors[variant]}`}>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-sm text-muted-foreground">{label}</div>
    </div>
  );
}
