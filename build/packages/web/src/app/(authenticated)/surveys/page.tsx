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
  ClipboardList,
  BarChart3,
  Users,
  Calendar,
  Play,
  Pause,
  Archive,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";
import { SlideOver, SlideOverSection, SlideOverField, SlideOverGrid } from "@/components/shared/SlideOver";
import { useSurveys, useCreateSurvey, useUpdateSurvey, useDeleteSurvey, useSurveyResponses } from "@/hooks/useSurveys";
import type { Survey, SurveyMode, SurveyStatus, SurveyCreate } from "@/types/api";

const modeIcons: Record<SurveyMode, React.ReactNode> = {
  adoption: <Users className="h-4 w-4 text-blue-500" />,
  sentiment: <BarChart3 className="h-4 w-4 text-green-500" />,
  readiness: <ClipboardList className="h-4 w-4 text-purple-500" />,
  feedback: <ClipboardList className="h-4 w-4 text-orange-500" />,
  custom: <ClipboardList className="h-4 w-4 text-gray-500" />,
};

const statusVariants: Record<SurveyStatus, "success" | "warning" | "secondary" | "danger"> = {
  draft: "secondary",
  active: "success",
  paused: "warning",
  closed: "secondary",
  archived: "secondary",
};

const defaultSurvey: SurveyCreate = {
  title: "",
  description: "",
  mode: "feedback",
  is_anonymous: true,
};

export default function SurveysPage() {
  const [modeFilter, setModeFilter] = React.useState<SurveyMode | "all">("all");
  const [statusFilter, setStatusFilter] = React.useState<SurveyStatus | "all">("all");
  const [selectedSurvey, setSelectedSurvey] = React.useState<Survey | null>(null);
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);
  const [formData, setFormData] = React.useState<SurveyCreate>(defaultSurvey);

  const filters = {
    mode: modeFilter !== "all" ? modeFilter : undefined,
    status: statusFilter !== "all" ? statusFilter : undefined,
  };

  const { data, isLoading } = useSurveys(filters);
  const createSurvey = useCreateSurvey();
  const updateSurvey = useUpdateSurvey();
  const deleteSurvey = useDeleteSurvey();
  const { data: responsesData } = useSurveyResponses(selectedSurvey?.id);

  const handleCreate = async () => {
    await createSurvey.mutateAsync(formData);
    setIsCreateOpen(false);
    setFormData(defaultSurvey);
  };

  const handleStatusChange = (id: string, status: SurveyStatus) => {
    updateSurvey.mutate({ id, data: { } });
  };

  const columns: ColumnDef<Survey>[] = [
    {
      accessorKey: "title",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Title" />,
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          {modeIcons[row.original.mode]}
          <span className="font-medium">{row.getValue("title")}</span>
        </div>
      ),
    },
    {
      accessorKey: "mode",
      header: "Mode",
      cell: ({ row }) => (
        <Badge variant="outline" className="capitalize">
          {row.getValue("mode")}
        </Badge>
      ),
    },
    {
      accessorKey: "status",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.getValue("status") as SurveyStatus;
        return (
          <Badge variant={statusVariants[status]} className="capitalize">
            {status}
          </Badge>
        );
      },
    },
    {
      accessorKey: "question_count",
      header: "Questions",
      cell: ({ row }) => row.getValue("question_count") || 0,
    },
    {
      accessorKey: "response_count",
      header: "Responses",
      cell: ({ row }) => row.getValue("response_count") || 0,
    },
    {
      accessorKey: "start_date",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Start Date" />,
      cell: ({ row }) => {
        const date = row.getValue("start_date") as string | null;
        return date ? format(new Date(date), "MMM d, yyyy") : "—";
      },
    },
    {
      accessorKey: "end_date",
      header: "End Date",
      cell: ({ row }) => {
        const date = row.getValue("end_date") as string | null;
        return date ? format(new Date(date), "MMM d, yyyy") : "—";
      },
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const survey = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setSelectedSurvey(survey)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Edit className="mr-2 h-4 w-4" />
                Edit Survey
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              {survey.status === "draft" && (
                <DropdownMenuItem onClick={() => handleStatusChange(survey.id, "active")}>
                  <Play className="mr-2 h-4 w-4" />
                  Activate
                </DropdownMenuItem>
              )}
              {survey.status === "active" && (
                <DropdownMenuItem onClick={() => handleStatusChange(survey.id, "paused")}>
                  <Pause className="mr-2 h-4 w-4" />
                  Pause
                </DropdownMenuItem>
              )}
              {survey.status === "paused" && (
                <DropdownMenuItem onClick={() => handleStatusChange(survey.id, "active")}>
                  <Play className="mr-2 h-4 w-4" />
                  Resume
                </DropdownMenuItem>
              )}
              {(survey.status === "active" || survey.status === "paused") && (
                <DropdownMenuItem onClick={() => handleStatusChange(survey.id, "closed")}>
                  <Archive className="mr-2 h-4 w-4" />
                  Close
                </DropdownMenuItem>
              )}
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => deleteSurvey.mutate(survey.id)}
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

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Surveys</h1>
          <p className="text-muted-foreground mt-1">
            Create and manage adoption, sentiment, and feedback surveys
          </p>
        </div>
        <Button onClick={() => setIsCreateOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Create Survey
        </Button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <Select
          value={modeFilter}
          onValueChange={(v) => setModeFilter(v as SurveyMode | "all")}
        >
          <SelectTrigger className="w-[160px]">
            <SelectValue placeholder="Mode" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Modes</SelectItem>
            <SelectItem value="adoption">Adoption</SelectItem>
            <SelectItem value="sentiment">Sentiment</SelectItem>
            <SelectItem value="readiness">Readiness</SelectItem>
            <SelectItem value="feedback">Feedback</SelectItem>
            <SelectItem value="custom">Custom</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={statusFilter}
          onValueChange={(v) => setStatusFilter(v as SurveyStatus | "all")}
        >
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value="draft">Draft</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="paused">Paused</SelectItem>
            <SelectItem value="closed">Closed</SelectItem>
            <SelectItem value="archived">Archived</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Data Table */}
      <DataTable
        columns={columns}
        data={data?.items || []}
        isLoading={isLoading}
        searchKey="title"
        searchPlaceholder="Search surveys..."
        onRowClick={setSelectedSurvey}
      />

      {/* Create Dialog */}
      <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Create Survey</DialogTitle>
            <DialogDescription>
              Create a new survey to collect feedback from your team.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                placeholder="Q1 Adoption Survey"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Input
                id="description"
                value={formData.description || ""}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Survey to measure process adoption rates..."
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="mode">Survey Mode</Label>
              <Select
                value={formData.mode}
                onValueChange={(v) => setFormData({ ...formData, mode: v as SurveyMode })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="adoption">Adoption</SelectItem>
                  <SelectItem value="sentiment">Sentiment</SelectItem>
                  <SelectItem value="readiness">Readiness</SelectItem>
                  <SelectItem value="feedback">Feedback</SelectItem>
                  <SelectItem value="custom">Custom</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="start_date">Start Date</Label>
                <Input
                  id="start_date"
                  type="date"
                  value={formData.start_date || ""}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="end_date">End Date</Label>
                <Input
                  id="end_date"
                  type="date"
                  value={formData.end_date || ""}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                />
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="anonymous"
                checked={formData.is_anonymous}
                onCheckedChange={(checked) =>
                  setFormData({ ...formData, is_anonymous: checked as boolean })
                }
              />
              <Label htmlFor="anonymous">Anonymous responses</Label>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsCreateOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreate} disabled={!formData.title || createSurvey.isPending}>
              {createSurvey.isPending ? "Creating..." : "Create Survey"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Detail Panel */}
      <SlideOver
        open={!!selectedSurvey}
        onOpenChange={(open) => !open && setSelectedSurvey(null)}
        title={selectedSurvey?.title || ""}
        description={selectedSurvey ? `${selectedSurvey.mode} survey` : ""}
        size="lg"
      >
        {selectedSurvey && (
          <div className="space-y-6">
            <SlideOverSection title="Overview">
              <SlideOverGrid>
                <SlideOverField
                  label="Mode"
                  value={
                    <div className="flex items-center gap-2 capitalize">
                      {modeIcons[selectedSurvey.mode]}
                      {selectedSurvey.mode}
                    </div>
                  }
                />
                <SlideOverField
                  label="Status"
                  value={
                    <Badge variant={statusVariants[selectedSurvey.status]} className="capitalize">
                      {selectedSurvey.status}
                    </Badge>
                  }
                />
                <SlideOverField
                  label="Anonymous"
                  value={selectedSurvey.is_anonymous ? "Yes" : "No"}
                />
              </SlideOverGrid>
            </SlideOverSection>

            {selectedSurvey.description && (
              <SlideOverSection title="Description">
                <p className="text-sm">{selectedSurvey.description}</p>
              </SlideOverSection>
            )}

            <SlideOverSection title="Statistics">
              <SlideOverGrid cols={3}>
                <SlideOverField label="Questions" value={selectedSurvey.question_count} />
                <SlideOverField label="Responses" value={selectedSurvey.response_count} />
                <SlideOverField
                  label="Response Rate"
                  value={
                    selectedSurvey.question_count > 0
                      ? `${Math.round((selectedSurvey.response_count / selectedSurvey.question_count) * 100)}%`
                      : "—"
                  }
                />
              </SlideOverGrid>
            </SlideOverSection>

            <SlideOverSection title="Timeline">
              <SlideOverGrid>
                <SlideOverField
                  label="Start Date"
                  value={
                    selectedSurvey.start_date
                      ? format(new Date(selectedSurvey.start_date), "MMMM d, yyyy")
                      : "Not set"
                  }
                />
                <SlideOverField
                  label="End Date"
                  value={
                    selectedSurvey.end_date
                      ? format(new Date(selectedSurvey.end_date), "MMMM d, yyyy")
                      : "Not set"
                  }
                />
              </SlideOverGrid>
            </SlideOverSection>

            {responsesData && responsesData.items.length > 0 && (
              <SlideOverSection title="Recent Responses">
                <div className="space-y-2">
                  {responsesData.items.slice(0, 5).map((response) => (
                    <div
                      key={response.id}
                      className="text-sm p-2 bg-muted rounded-md flex justify-between"
                    >
                      <span>Response #{response.id.slice(0, 8)}</span>
                      <span className="text-muted-foreground">
                        {format(new Date(response.submitted_at), "MMM d, yyyy")}
                      </span>
                    </div>
                  ))}
                </div>
              </SlideOverSection>
            )}
          </div>
        )}
      </SlideOver>
    </div>
  );
}
