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
  Play,
  Sparkles,
  FileText,
  BarChart3,
  Settings,
  History,
  Copy,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";
import { SlideOver, SlideOverSection, SlideOverField, SlideOverGrid } from "@/components/shared/SlideOver";
import {
  usePromptTemplates,
  useCreatePromptTemplate,
  useDeletePromptTemplate,
  usePromptExecutions,
  useExecutePrompt,
} from "@/hooks/usePrompts";
import type {
  PromptTemplate,
  PromptTemplateCreate,
  PromptExecution,
  PromptCategory,
  ContextType,
} from "@/types/api";

const categoryIcons: Record<PromptCategory, React.ReactNode> = {
  analysis: <BarChart3 className="h-4 w-4 text-blue-500" />,
  documentation: <FileText className="h-4 w-4 text-green-500" />,
  optimization: <Zap className="h-4 w-4 text-yellow-500" />,
  reporting: <BarChart3 className="h-4 w-4 text-purple-500" />,
  custom: <Sparkles className="h-4 w-4 text-gray-500" />,
};

const contextTypeLabels: Record<ContextType, string> = {
  process: "Process",
  portfolio: "Portfolio Item",
  riada: "RIADA Item",
  business_model: "Business Model",
};

const defaultTemplate: PromptTemplateCreate = {
  name: "",
  description: "",
  category: "analysis",
  user_prompt_template: "",
  context_type: "process",
  include_riada: false,
  include_kpis: false,
  include_raci: false,
};

export default function PromptsPage() {
  const [activeTab, setActiveTab] = React.useState<"templates" | "history">("templates");
  const [categoryFilter, setCategoryFilter] = React.useState<PromptCategory | "all">("all");
  const [selectedTemplate, setSelectedTemplate] = React.useState<PromptTemplate | null>(null);
  const [selectedExecution, setSelectedExecution] = React.useState<PromptExecution | null>(null);
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);
  const [isExecuteOpen, setIsExecuteOpen] = React.useState(false);
  const [formData, setFormData] = React.useState<PromptTemplateCreate>(defaultTemplate);
  const [executeTargetId, setExecuteTargetId] = React.useState("");

  const filters = {
    category: categoryFilter !== "all" ? categoryFilter : undefined,
  };

  const { data: templatesData, isLoading: templatesLoading } = usePromptTemplates(filters);
  const { data: executionsData, isLoading: executionsLoading } = usePromptExecutions(50);
  const createTemplate = useCreatePromptTemplate();
  const deleteTemplate = useDeletePromptTemplate();
  const executePrompt = useExecutePrompt();

  const handleCreate = async () => {
    await createTemplate.mutateAsync(formData);
    setIsCreateOpen(false);
    setFormData(defaultTemplate);
  };

  const handleExecute = async () => {
    if (!selectedTemplate || !executeTargetId) return;
    await executePrompt.mutateAsync({
      template_id: selectedTemplate.id,
      target_entity_type: selectedTemplate.context_type,
      target_entity_id: executeTargetId,
    });
    setIsExecuteOpen(false);
    setExecuteTargetId("");
    setActiveTab("history");
  };

  const templateColumns: ColumnDef<PromptTemplate>[] = [
    {
      accessorKey: "name",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          {categoryIcons[row.original.category]}
          <span className="font-medium">{row.getValue("name")}</span>
        </div>
      ),
    },
    {
      accessorKey: "category",
      header: "Category",
      cell: ({ row }) => (
        <Badge variant="outline" className="capitalize">
          {row.getValue("category")}
        </Badge>
      ),
    },
    {
      accessorKey: "context_type",
      header: "Context",
      cell: ({ row }) => (
        <span className="text-sm">
          {contextTypeLabels[row.getValue("context_type") as ContextType]}
        </span>
      ),
    },
    {
      accessorKey: "usage_count",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Uses" />,
      cell: ({ row }) => row.getValue("usage_count") || 0,
    },
    {
      accessorKey: "is_active",
      header: "Status",
      cell: ({ row }) => (
        <Badge variant={row.getValue("is_active") ? "success" : "secondary"}>
          {row.getValue("is_active") ? "Active" : "Inactive"}
        </Badge>
      ),
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const template = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setSelectedTemplate(template)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  setSelectedTemplate(template);
                  setIsExecuteOpen(true);
                }}
              >
                <Play className="mr-2 h-4 w-4" />
                Execute
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Copy className="mr-2 h-4 w-4" />
                Duplicate
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => deleteTemplate.mutate(template.id)}
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

  const executionColumns: ColumnDef<PromptExecution>[] = [
    {
      accessorKey: "created_at",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Date" />,
      cell: ({ row }) => format(new Date(row.getValue("created_at")), "MMM d, yyyy HH:mm"),
    },
    {
      accessorKey: "target_entity_type",
      header: "Target",
      cell: ({ row }) => (
        <span className="capitalize">{row.getValue("target_entity_type")}</span>
      ),
    },
    {
      accessorKey: "model_used",
      header: "Model",
      cell: ({ row }) => (
        <Badge variant="outline">{row.getValue("model_used")}</Badge>
      ),
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => {
        const status = row.getValue("status") as string;
        return (
          <Badge
            variant={
              status === "completed" ? "success" : status === "failed" ? "danger" : "warning"
            }
          >
            {status}
          </Badge>
        );
      },
    },
    {
      accessorKey: "prompt_tokens",
      header: "Tokens",
      cell: ({ row }) => {
        const promptTokens = row.original.prompt_tokens || 0;
        const completionTokens = row.original.completion_tokens || 0;
        return `${promptTokens + completionTokens}`;
      },
    },
    {
      accessorKey: "execution_time_ms",
      header: "Time",
      cell: ({ row }) => {
        const ms = row.getValue("execution_time_ms") as number | null;
        return ms ? `${(ms / 1000).toFixed(2)}s` : "—";
      },
    },
    {
      id: "actions",
      cell: ({ row }) => (
        <Button variant="ghost" size="sm" onClick={() => setSelectedExecution(row.original)}>
          <Eye className="h-4 w-4" />
        </Button>
      ),
    },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Prompt Library</h1>
          <p className="text-muted-foreground mt-1">
            AI-powered analysis templates for processes and portfolio items
          </p>
        </div>
        <Button onClick={() => setIsCreateOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Create Template
        </Button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Templates</CardDescription>
            <CardTitle className="text-2xl">{templatesData?.total || 0}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Total Executions</CardDescription>
            <CardTitle className="text-2xl">{executionsData?.total || 0}</CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>This Month</CardDescription>
            <CardTitle className="text-2xl">
              {(executionsData?.items ?? []).filter(
                (e) => new Date(e.created_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
              ).length}
            </CardTitle>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardDescription>Success Rate</CardDescription>
            <CardTitle className="text-2xl">
              {(executionsData?.items?.length ?? 0) > 0
                ? `${Math.round(
                    ((executionsData?.items ?? []).filter((e) => e.status === "completed").length /
                      (executionsData?.items?.length ?? 1)) *
                      100
                  )}%`
                : "—"}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as "templates" | "history")}>
        <div className="flex items-center justify-between">
          <TabsList>
            <TabsTrigger value="templates" className="flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              Templates
            </TabsTrigger>
            <TabsTrigger value="history" className="flex items-center gap-2">
              <History className="h-4 w-4" />
              Execution History
            </TabsTrigger>
          </TabsList>

          {activeTab === "templates" && (
            <Select
              value={categoryFilter}
              onValueChange={(v) => setCategoryFilter(v as PromptCategory | "all")}
            >
              <SelectTrigger className="w-[160px]">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="analysis">Analysis</SelectItem>
                <SelectItem value="documentation">Documentation</SelectItem>
                <SelectItem value="optimization">Optimization</SelectItem>
                <SelectItem value="reporting">Reporting</SelectItem>
                <SelectItem value="custom">Custom</SelectItem>
              </SelectContent>
            </Select>
          )}
        </div>

        <TabsContent value="templates" className="mt-4">
          <DataTable
            columns={templateColumns}
            data={templatesData?.items || []}
            isLoading={templatesLoading}
            searchKey="name"
            searchPlaceholder="Search templates..."
            onRowClick={setSelectedTemplate}
          />
        </TabsContent>

        <TabsContent value="history" className="mt-4">
          <DataTable
            columns={executionColumns}
            data={executionsData?.items || []}
            isLoading={executionsLoading}
            searchKey="target_entity_type"
            searchPlaceholder="Search executions..."
          />
        </TabsContent>
      </Tabs>

      {/* Create Template Dialog */}
      <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Create Prompt Template</DialogTitle>
            <DialogDescription>
              Create a reusable prompt template for AI-powered analysis.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Process Gap Analysis"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Input
                id="description"
                value={formData.description || ""}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Analyze gaps between current and target state..."
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label>Category</Label>
                <Select
                  value={formData.category}
                  onValueChange={(v) => setFormData({ ...formData, category: v as PromptCategory })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="analysis">Analysis</SelectItem>
                    <SelectItem value="documentation">Documentation</SelectItem>
                    <SelectItem value="optimization">Optimization</SelectItem>
                    <SelectItem value="reporting">Reporting</SelectItem>
                    <SelectItem value="custom">Custom</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-2">
                <Label>Context Type</Label>
                <Select
                  value={formData.context_type}
                  onValueChange={(v) => setFormData({ ...formData, context_type: v as ContextType })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="process">Process</SelectItem>
                    <SelectItem value="portfolio">Portfolio Item</SelectItem>
                    <SelectItem value="riada">RIADA Item</SelectItem>
                    <SelectItem value="business_model">Business Model</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="prompt">Prompt Template</Label>
              <textarea
                id="prompt"
                className="min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={formData.user_prompt_template}
                onChange={(e) =>
                  setFormData({ ...formData, user_prompt_template: e.target.value })
                }
                placeholder="Analyze the following process and identify improvement opportunities..."
              />
              <p className="text-xs text-muted-foreground">
                Use {"{{context}}"} to include entity data in the prompt.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsCreateOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleCreate}
              disabled={!formData.name || !formData.user_prompt_template || createTemplate.isPending}
            >
              {createTemplate.isPending ? "Creating..." : "Create Template"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Execute Dialog */}
      <Dialog open={isExecuteOpen} onOpenChange={setIsExecuteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Execute Prompt</DialogTitle>
            <DialogDescription>
              Run "{selectedTemplate?.name}" on a {selectedTemplate?.context_type}.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="target_id">
                {contextTypeLabels[selectedTemplate?.context_type || "process"]} ID
              </Label>
              <Input
                id="target_id"
                value={executeTargetId}
                onChange={(e) => setExecuteTargetId(e.target.value)}
                placeholder="Enter the entity ID..."
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsExecuteOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleExecute}
              disabled={!executeTargetId || executePrompt.isPending}
            >
              {executePrompt.isPending ? "Executing..." : "Execute"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Template Detail Panel */}
      <SlideOver
        open={!!selectedTemplate && !isExecuteOpen}
        onOpenChange={(open) => !open && setSelectedTemplate(null)}
        title={selectedTemplate?.name || ""}
        description={selectedTemplate?.category || ""}
        size="lg"
      >
        {selectedTemplate && (
          <div className="space-y-6">
            <SlideOverSection title="Overview">
              <SlideOverGrid>
                <SlideOverField
                  label="Category"
                  value={
                    <div className="flex items-center gap-2 capitalize">
                      {categoryIcons[selectedTemplate.category]}
                      {selectedTemplate.category}
                    </div>
                  }
                />
                <SlideOverField
                  label="Context"
                  value={contextTypeLabels[selectedTemplate.context_type]}
                />
                <SlideOverField
                  label="Status"
                  value={
                    <Badge variant={selectedTemplate.is_active ? "success" : "secondary"}>
                      {selectedTemplate.is_active ? "Active" : "Inactive"}
                    </Badge>
                  }
                />
                <SlideOverField label="Usage Count" value={selectedTemplate.usage_count} />
              </SlideOverGrid>
            </SlideOverSection>

            {selectedTemplate.description && (
              <SlideOverSection title="Description">
                <p className="text-sm">{selectedTemplate.description}</p>
              </SlideOverSection>
            )}

            <SlideOverSection title="Prompt Template">
              <pre className="text-sm bg-muted p-4 rounded-md whitespace-pre-wrap">
                {selectedTemplate.user_prompt_template}
              </pre>
            </SlideOverSection>

            {selectedTemplate.system_prompt && (
              <SlideOverSection title="System Prompt">
                <pre className="text-sm bg-muted p-4 rounded-md whitespace-pre-wrap">
                  {selectedTemplate.system_prompt}
                </pre>
              </SlideOverSection>
            )}

            <SlideOverSection title="Context Options">
              <SlideOverGrid cols={3}>
                <SlideOverField
                  label="Include RIADA"
                  value={selectedTemplate.include_riada ? "Yes" : "No"}
                />
                <SlideOverField
                  label="Include KPIs"
                  value={selectedTemplate.include_kpis ? "Yes" : "No"}
                />
                <SlideOverField
                  label="Include RACI"
                  value={selectedTemplate.include_raci ? "Yes" : "No"}
                />
              </SlideOverGrid>
            </SlideOverSection>

            <div className="pt-4">
              <Button
                className="w-full"
                onClick={() => setIsExecuteOpen(true)}
              >
                <Play className="h-4 w-4 mr-2" />
                Execute This Template
              </Button>
            </div>
          </div>
        )}
      </SlideOver>

      {/* Execution Detail Panel */}
      <SlideOver
        open={!!selectedExecution}
        onOpenChange={(open) => !open && setSelectedExecution(null)}
        title="Execution Details"
        description={
          selectedExecution
            ? format(new Date(selectedExecution.created_at), "MMMM d, yyyy HH:mm")
            : ""
        }
        size="lg"
      >
        {selectedExecution && (
          <div className="space-y-6">
            <SlideOverSection title="Execution Info">
              <SlideOverGrid>
                <SlideOverField
                  label="Status"
                  value={
                    <Badge
                      variant={
                        selectedExecution.status === "completed"
                          ? "success"
                          : selectedExecution.status === "failed"
                          ? "danger"
                          : "warning"
                      }
                    >
                      {selectedExecution.status}
                    </Badge>
                  }
                />
                <SlideOverField label="Model" value={selectedExecution.model_used} />
                <SlideOverField
                  label="Target"
                  value={`${selectedExecution.target_entity_type} (${selectedExecution.target_entity_id.slice(0, 8)}...)`}
                />
              </SlideOverGrid>
            </SlideOverSection>

            <SlideOverSection title="Token Usage">
              <SlideOverGrid cols={3}>
                <SlideOverField
                  label="Prompt Tokens"
                  value={selectedExecution.prompt_tokens || "—"}
                />
                <SlideOverField
                  label="Completion Tokens"
                  value={selectedExecution.completion_tokens || "—"}
                />
                <SlideOverField
                  label="Execution Time"
                  value={
                    selectedExecution.execution_time_ms
                      ? `${(selectedExecution.execution_time_ms / 1000).toFixed(2)}s`
                      : "—"
                  }
                />
              </SlideOverGrid>
            </SlideOverSection>

            <SlideOverSection title="Prompt Sent">
              <pre className="text-sm bg-muted p-4 rounded-md whitespace-pre-wrap max-h-[200px] overflow-y-auto">
                {selectedExecution.prompt_sent}
              </pre>
            </SlideOverSection>

            {selectedExecution.response_received && (
              <SlideOverSection title="Response">
                <pre className="text-sm bg-muted p-4 rounded-md whitespace-pre-wrap max-h-[300px] overflow-y-auto">
                  {selectedExecution.response_received}
                </pre>
              </SlideOverSection>
            )}

            {selectedExecution.error_message && (
              <SlideOverSection title="Error">
                <p className="text-sm text-destructive">{selectedExecution.error_message}</p>
              </SlideOverSection>
            )}
          </div>
        )}
      </SlideOver>
    </div>
  );
}
