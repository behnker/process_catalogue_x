"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { ColumnDef } from "@tanstack/react-table";
import { format } from "date-fns";
import {
  MoreHorizontal,
  Plus,
  Eye,
  Edit,
  Trash2,
  AlertTriangle,
  AlertCircle,
  CheckCircle,
  Link as LinkIcon,
  Clock,
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
import { useRiadaItems, useDeleteRiadaItem } from "@/hooks/useRiada";
import type { RiadaItem, RiadaType, RiadaCategory, RiadaSeverity, RiadaStatus } from "@/types/api";

const typeIcons: Record<RiadaType, React.ReactNode> = {
  risk: <AlertTriangle className="h-4 w-4 text-red-500" />,
  issue: <AlertCircle className="h-4 w-4 text-orange-500" />,
  action: <CheckCircle className="h-4 w-4 text-blue-500" />,
  dependency: <LinkIcon className="h-4 w-4 text-purple-500" />,
  assumption: <Clock className="h-4 w-4 text-green-500" />,
};

const severityVariants: Record<RiadaSeverity, "danger" | "warning" | "secondary"> = {
  critical: "danger",
  high: "danger",
  medium: "warning",
  low: "secondary",
};

const statusVariants: Record<RiadaStatus, "success" | "warning" | "secondary" | "danger"> = {
  open: "danger",
  in_progress: "warning",
  mitigated: "success",
  resolved: "success",
  closed: "secondary",
  accepted: "secondary",
};

export default function RiadaPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = React.useState<RiadaType | "all">("all");
  const [categoryFilter, setCategoryFilter] = React.useState<RiadaCategory | "all">("all");
  const [statusFilter, setStatusFilter] = React.useState<RiadaStatus | "all">("all");

  const filters = {
    riada_type: activeTab !== "all" ? activeTab : undefined,
    category: categoryFilter !== "all" ? categoryFilter : undefined,
    status: statusFilter !== "all" ? statusFilter : undefined,
  };

  const { data, isLoading } = useRiadaItems(filters);
  const deleteItem = useDeleteRiadaItem();

  const [selectedItem, setSelectedItem] = React.useState<RiadaItem | null>(null);

  // Base columns shared by all types
  const baseColumns: ColumnDef<RiadaItem>[] = [
    {
      accessorKey: "code",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Code" />,
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          {typeIcons[row.original.riada_type]}
          <span className="font-mono text-sm">{row.getValue("code")}</span>
        </div>
      ),
    },
    {
      accessorKey: "title",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Title" />,
      cell: ({ row }) => (
        <span className="font-medium">{row.getValue("title")}</span>
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
      accessorKey: "severity",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Severity" />,
      cell: ({ row }) => {
        const severity = row.getValue("severity") as RiadaSeverity;
        return (
          <Badge variant={severityVariants[severity]} className="capitalize">
            {severity}
          </Badge>
        );
      },
    },
    {
      accessorKey: "status",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.getValue("status") as RiadaStatus;
        return (
          <Badge variant={statusVariants[status]} className="capitalize">
            {status.replace("_", " ")}
          </Badge>
        );
      },
    },
  ];

  // Risk-specific columns
  const riskColumns: ColumnDef<RiadaItem>[] = [
    ...baseColumns,
    {
      accessorKey: "probability",
      header: "Prob.",
      cell: ({ row }) => row.getValue("probability") || "—",
    },
    {
      accessorKey: "impact",
      header: "Impact",
      cell: ({ row }) => row.getValue("impact") || "—",
    },
    {
      accessorKey: "risk_score",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Score" />,
      cell: ({ row }) => {
        const score = row.getValue("risk_score") as number | null;
        if (!score) return "—";
        return (
          <span className={score >= 16 ? "text-red-600 font-semibold" : score >= 9 ? "text-amber-600" : ""}>
            {score}
          </span>
        );
      },
    },
  ];

  // Action-specific columns
  const actionColumns: ColumnDef<RiadaItem>[] = [
    ...baseColumns,
    {
      accessorKey: "due_date",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Due Date" />,
      cell: ({ row }) => {
        const date = row.getValue("due_date") as string | null;
        if (!date) return "—";
        const isOverdue = new Date(date) < new Date();
        return (
          <span className={isOverdue ? "text-red-600" : ""}>
            {format(new Date(date), "MMM d, yyyy")}
          </span>
        );
      },
    },
  ];

  // Actions column for all types
  const actionsColumn: ColumnDef<RiadaItem> = {
    id: "actions",
    cell: ({ row }) => {
      const item = row.original;
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => setSelectedItem(item)}>
              <Eye className="mr-2 h-4 w-4" />
              View Details
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => router.push(`/riada/${item.id}/edit`)}>
              <Edit className="mr-2 h-4 w-4" />
              Edit
            </DropdownMenuItem>
            <DropdownMenuItem
              onClick={() => deleteItem.mutate(item.id)}
              className="text-destructive"
            >
              <Trash2 className="mr-2 h-4 w-4" />
              Delete
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  };

  // Select columns based on active tab
  const getColumns = () => {
    if (activeTab === "risk") return [...riskColumns, actionsColumn];
    if (activeTab === "action") return [...actionColumns, actionsColumn];
    return [...baseColumns, actionsColumn];
  };

  const typeCounts = React.useMemo(() => {
    if (!data?.items) return { risk: 0, issue: 0, action: 0, dependency: 0, assumption: 0 };
    const items = data.items;
    return {
      risk: items.filter((i) => i.riada_type === "risk").length,
      issue: items.filter((i) => i.riada_type === "issue").length,
      action: items.filter((i) => i.riada_type === "action").length,
      dependency: items.filter((i) => i.riada_type === "dependency").length,
      assumption: items.filter((i) => i.riada_type === "assumption").length,
    };
  }, [data]);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">RIADA</h1>
          <p className="text-muted-foreground mt-1">
            Risks, Issues, Actions, Dependencies, Assumptions
          </p>
        </div>
        <Button onClick={() => router.push("/riada/new")}>
          <Plus className="h-4 w-4 mr-2" />
          Create Item
        </Button>
      </div>

      {/* Type Tabs */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as RiadaType | "all")}>
        <TabsList>
          <TabsTrigger value="all">All ({data?.total || 0})</TabsTrigger>
          <TabsTrigger value="risk" className="flex items-center gap-1">
            {typeIcons.risk}
            Risks ({typeCounts.risk})
          </TabsTrigger>
          <TabsTrigger value="issue" className="flex items-center gap-1">
            {typeIcons.issue}
            Issues ({typeCounts.issue})
          </TabsTrigger>
          <TabsTrigger value="action" className="flex items-center gap-1">
            {typeIcons.action}
            Actions ({typeCounts.action})
          </TabsTrigger>
          <TabsTrigger value="dependency" className="flex items-center gap-1">
            {typeIcons.dependency}
            Dependencies ({typeCounts.dependency})
          </TabsTrigger>
          <TabsTrigger value="assumption" className="flex items-center gap-1">
            {typeIcons.assumption}
            Assumptions ({typeCounts.assumption})
          </TabsTrigger>
        </TabsList>

        <div className="mt-4 flex items-center gap-4">
          <Select
            value={categoryFilter}
            onValueChange={(v) => setCategoryFilter(v as RiadaCategory | "all")}
          >
            <SelectTrigger className="w-[140px]">
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              <SelectItem value="people">People</SelectItem>
              <SelectItem value="process">Process</SelectItem>
              <SelectItem value="system">System</SelectItem>
              <SelectItem value="data">Data</SelectItem>
            </SelectContent>
          </Select>

          <Select
            value={statusFilter}
            onValueChange={(v) => setStatusFilter(v as RiadaStatus | "all")}
          >
            <SelectTrigger className="w-[140px]">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Statuses</SelectItem>
              <SelectItem value="open">Open</SelectItem>
              <SelectItem value="in_progress">In Progress</SelectItem>
              <SelectItem value="mitigated">Mitigated</SelectItem>
              <SelectItem value="resolved">Resolved</SelectItem>
              <SelectItem value="closed">Closed</SelectItem>
              <SelectItem value="accepted">Accepted</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <TabsContent value={activeTab} className="mt-4">
          <DataTable
            columns={getColumns()}
            data={data?.items || []}
            isLoading={isLoading}
            searchKey="title"
            searchPlaceholder="Search items..."
            enableRowSelection
            enableExport
            onRowClick={setSelectedItem}
          />
        </TabsContent>
      </Tabs>

      {/* Detail Panel */}
      <SlideOver
        open={!!selectedItem}
        onOpenChange={(open) => !open && setSelectedItem(null)}
        title={selectedItem?.title || ""}
        description={selectedItem ? `${selectedItem.code} — ${selectedItem.riada_type}` : ""}
        size="lg"
      >
        {selectedItem && (
          <div className="space-y-6">
            <SlideOverSection title="Classification">
              <SlideOverGrid>
                <SlideOverField label="Type" value={
                  <div className="flex items-center gap-2 capitalize">
                    {typeIcons[selectedItem.riada_type]}
                    {selectedItem.riada_type}
                  </div>
                } />
                <SlideOverField label="Category" value={selectedItem.category} />
                <SlideOverField label="Severity" value={
                  <Badge variant={severityVariants[selectedItem.severity]} className="capitalize">
                    {selectedItem.severity}
                  </Badge>
                } />
                <SlideOverField label="Status" value={
                  <Badge variant={statusVariants[selectedItem.status]} className="capitalize">
                    {selectedItem.status.replace("_", " ")}
                  </Badge>
                } />
              </SlideOverGrid>
            </SlideOverSection>

            {selectedItem.description && (
              <SlideOverSection title="Description">
                <p className="text-sm">{selectedItem.description}</p>
              </SlideOverSection>
            )}

            {selectedItem.riada_type === "risk" && (
              <SlideOverSection title="Risk Assessment">
                <SlideOverGrid cols={3}>
                  <SlideOverField label="Probability" value={selectedItem.probability || "—"} />
                  <SlideOverField label="Impact" value={selectedItem.impact || "—"} />
                  <SlideOverField label="Risk Score" value={selectedItem.risk_score || "—"} />
                </SlideOverGrid>
                {selectedItem.mitigation_plan && (
                  <div className="mt-4">
                    <span className="text-sm text-muted-foreground">Mitigation Plan</span>
                    <p className="text-sm mt-1">{selectedItem.mitigation_plan}</p>
                  </div>
                )}
              </SlideOverSection>
            )}

            {selectedItem.due_date && (
              <SlideOverSection title="Timeline">
                <SlideOverField
                  label="Due Date"
                  value={format(new Date(selectedItem.due_date), "MMMM d, yyyy")}
                />
              </SlideOverSection>
            )}

            {selectedItem.resolution_notes && (
              <SlideOverSection title="Resolution">
                <p className="text-sm">{selectedItem.resolution_notes}</p>
                {selectedItem.resolved_at && (
                  <p className="text-sm text-muted-foreground mt-2">
                    Resolved on {format(new Date(selectedItem.resolved_at), "MMMM d, yyyy")}
                  </p>
                )}
              </SlideOverSection>
            )}
          </div>
        )}
      </SlideOver>
    </div>
  );
}
