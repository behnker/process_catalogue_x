"use client";

import * as React from "react";
import { Plus, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DataTable } from "@/components/shared/DataTable";
import { SlideOver } from "@/components/shared/SlideOver";
import { IssueSummaryCard } from "@/components/issues/IssueSummaryCard";
import { IssueDetailPanel } from "@/components/issues/IssueDetailPanel";
import { IssueForm } from "@/components/issues/IssueForm";
import { getIssueColumns } from "@/components/issues/issueColumns";
import { useIssues, useDeleteIssue, useIssueSummary, useExportIssues } from "@/hooks/useIssues";
import type { Issue, IssueStatus, IssueClassification, IssueCriticality } from "@/types/issue.types";

export default function IssuesPage() {
  const [statusFilter, setStatusFilter] = React.useState<IssueStatus | "all">("all");
  const [classFilter, setClassFilter] = React.useState<IssueClassification | "all">("all");
  const [critFilter, setCritFilter] = React.useState<IssueCriticality | "all">("all");
  const [selectedIssue, setSelectedIssue] = React.useState<Issue | null>(null);
  const [isNewIssueOpen, setIsNewIssueOpen] = React.useState(false);
  const [editingIssue, setEditingIssue] = React.useState<Issue | null>(null);

  const filters = {
    status_filter: statusFilter !== "all" ? statusFilter : undefined,
    classification: classFilter !== "all" ? classFilter : undefined,
    criticality: critFilter !== "all" ? critFilter : undefined,
  };

  const { data, isLoading } = useIssues(filters);
  const { data: summary } = useIssueSummary();
  const deleteIssue = useDeleteIssue();
  const exportIssues = useExportIssues();

  const columns = React.useMemo(
    () =>
      getIssueColumns({
        onView: setSelectedIssue,
        onEdit: setEditingIssue,
        onDelete: (id) => deleteIssue.mutate(id),
      }),
    [deleteIssue]
  );

  const handleEditFromDetail = (issue: Issue) => {
    setSelectedIssue(null);
    setEditingIssue(issue);
  };

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
          <Button onClick={() => setIsNewIssueOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Issue
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <IssueSummaryCard label="Open" value={summary.total_open} variant="blue" />
          <IssueSummaryCard label="In Progress" value={summary.total_in_progress} variant="amber" />
          <IssueSummaryCard label="Overdue" value={summary.overdue_count} variant="red" />
          <IssueSummaryCard label="Due This Week" value={summary.due_this_week} variant="purple" />
          <IssueSummaryCard label="Opportunities" value={summary.opportunities_identified} variant="green" />
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

      {/* New Issue Drawer */}
      <SlideOver
        open={isNewIssueOpen}
        onOpenChange={setIsNewIssueOpen}
        title="New Issue"
        description="Log a new operational issue"
        size="lg"
      >
        <IssueForm
          onSuccess={() => setIsNewIssueOpen(false)}
          onCancel={() => setIsNewIssueOpen(false)}
        />
      </SlideOver>

      {/* Edit Issue Drawer */}
      <SlideOver
        open={!!editingIssue}
        onOpenChange={(open) => !open && setEditingIssue(null)}
        title={`Edit ${editingIssue?.display_id || ""}`}
        description="Update issue details and status"
        size="lg"
      >
        {editingIssue && (
          <IssueForm
            issue={editingIssue}
            onSuccess={() => setEditingIssue(null)}
            onCancel={() => setEditingIssue(null)}
          />
        )}
      </SlideOver>

      {/* Detail Panel */}
      <SlideOver
        open={!!selectedIssue}
        onOpenChange={(open) => !open && setSelectedIssue(null)}
        title={selectedIssue?.display_id || ""}
        description={selectedIssue?.title || ""}
        size="lg"
      >
        {selectedIssue && (
          <IssueDetailPanel issue={selectedIssue} onEdit={handleEditFromDetail} />
        )}
      </SlideOver>
    </div>
  );
}
