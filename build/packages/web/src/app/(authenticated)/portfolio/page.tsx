"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { ColumnDef } from "@tanstack/react-table";
import { format } from "date-fns";
import {
  ChevronRight,
  ChevronDown,
  Plus,
  FolderTree,
  Table as TableIcon,
  GanttChart,
  MoreHorizontal,
  Eye,
  Edit,
  Trash2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";
import { SlideOver, SlideOverSection, SlideOverField, SlideOverGrid } from "@/components/shared/SlideOver";
import { usePortfolioItems, usePortfolioTree, useDeletePortfolioItem } from "@/hooks/usePortfolio";
import type { PortfolioItem, PortfolioLevel, PortfolioStatus, RagStatus } from "@/types/api";
import { cn } from "@/lib/utils";

const levelIcons: Record<PortfolioLevel, string> = {
  strategy: "bg-purple-500",
  portfolio: "bg-blue-500",
  programme: "bg-green-500",
  project: "bg-orange-500",
  workstream: "bg-yellow-500",
  epic: "bg-pink-500",
  task: "bg-gray-500",
};

const statusVariants: Record<PortfolioStatus, "success" | "warning" | "secondary" | "danger"> = {
  proposed: "secondary",
  approved: "success",
  in_progress: "warning",
  on_hold: "secondary",
  completed: "success",
  cancelled: "danger",
};

const ragColors: Record<RagStatus, string> = {
  red: "bg-rag-red",
  amber: "bg-rag-amber",
  green: "bg-rag-green",
};

// Tree Node Component
interface TreeNodeProps {
  item: PortfolioItem;
  depth: number;
  onSelect: (item: PortfolioItem) => void;
  selectedId?: string;
}

function TreeNode({ item, depth, onSelect, selectedId }: TreeNodeProps) {
  const [expanded, setExpanded] = React.useState(depth < 2);
  const hasChildren = item.children && item.children.length > 0;

  return (
    <div>
      <div
        className={cn(
          "flex items-center gap-2 py-2 px-3 cursor-pointer hover:bg-muted rounded-md transition-colors",
          selectedId === item.id && "bg-muted"
        )}
        style={{ paddingLeft: `${depth * 24 + 12}px` }}
        onClick={() => onSelect(item)}
      >
        {hasChildren ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setExpanded(!expanded);
            }}
            className="p-0.5 hover:bg-accent rounded"
          >
            {expanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        ) : (
          <span className="w-5" />
        )}

        <div className={cn("w-2 h-2 rounded-full", levelIcons[item.level])} />

        <span className="font-mono text-xs text-muted-foreground">{item.code}</span>

        <span className="font-medium flex-1">{item.name}</span>

        {item.rag_status && (
          <div className={cn("w-3 h-3 rounded-full", ragColors[item.rag_status])} />
        )}

        <Badge variant={statusVariants[item.status]} className="text-xs capitalize">
          {item.status.replace("_", " ")}
        </Badge>
      </div>

      {expanded && hasChildren && (
        <div>
          {item.children!.map((child) => (
            <TreeNode
              key={child.id}
              item={child}
              depth={depth + 1}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function PortfolioPage() {
  const router = useRouter();
  const [view, setView] = React.useState<"tree" | "table" | "gantt">("tree");
  const { data: treeData, isLoading: treeLoading } = usePortfolioTree();
  const { data: tableData, isLoading: tableLoading } = usePortfolioItems();
  const deleteItem = useDeletePortfolioItem();

  const [selectedItem, setSelectedItem] = React.useState<PortfolioItem | null>(null);

  const columns: ColumnDef<PortfolioItem>[] = [
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
      header: "Level",
      cell: ({ row }) => {
        const level = row.getValue("level") as PortfolioLevel;
        return (
          <div className="flex items-center gap-2">
            <div className={cn("w-2 h-2 rounded-full", levelIcons[level])} />
            <span className="capitalize">{level}</span>
          </div>
        );
      },
    },
    {
      accessorKey: "status",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.getValue("status") as PortfolioStatus;
        return (
          <Badge variant={statusVariants[status]} className="capitalize">
            {status.replace("_", " ")}
          </Badge>
        );
      },
    },
    {
      accessorKey: "rag_status",
      header: "RAG",
      cell: ({ row }) => {
        const rag = row.getValue("rag_status") as RagStatus | null;
        if (!rag) return "—";
        return <div className={cn("w-4 h-4 rounded-full", ragColors[rag])} />;
      },
    },
    {
      accessorKey: "planned_end",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Due" />,
      cell: ({ row }) => {
        const date = row.getValue("planned_end") as string | null;
        if (!date) return "—";
        return format(new Date(date), "MMM d, yyyy");
      },
    },
    {
      accessorKey: "wsvf_score",
      header: ({ column }) => <DataTableColumnHeader column={column} title="WSVF" />,
      cell: ({ row }) => {
        const score = row.getValue("wsvf_score") as number | null;
        return score ? score.toFixed(1) : "—";
      },
    },
    {
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
              <DropdownMenuItem onClick={() => router.push(`/portfolio/${item.id}/edit`)}>
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
    },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Portfolio</h1>
          <p className="text-muted-foreground mt-1">
            Manage programmes, projects, and initiatives
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Tabs value={view} onValueChange={(v) => setView(v as "tree" | "table" | "gantt")}>
            <TabsList>
              <TabsTrigger value="tree">
                <FolderTree className="h-4 w-4" />
              </TabsTrigger>
              <TabsTrigger value="table">
                <TableIcon className="h-4 w-4" />
              </TabsTrigger>
              <TabsTrigger value="gantt">
                <GanttChart className="h-4 w-4" />
              </TabsTrigger>
            </TabsList>
          </Tabs>
          <Button onClick={() => router.push("/portfolio/new")}>
            <Plus className="h-4 w-4 mr-2" />
            Create Item
          </Button>
        </div>
      </div>

      {/* Views */}
      {view === "tree" && (
        <div className="border rounded-lg">
          {treeLoading ? (
            <div className="p-8 text-center text-muted-foreground">Loading...</div>
          ) : treeData && treeData.length > 0 ? (
            <div className="py-2">
              {treeData.map((item) => (
                <TreeNode
                  key={item.id}
                  item={item}
                  depth={0}
                  onSelect={setSelectedItem}
                  selectedId={selectedItem?.id}
                />
              ))}
            </div>
          ) : (
            <div className="p-8 text-center">
              <p className="text-muted-foreground mb-4">No portfolio items yet</p>
              <Button onClick={() => router.push("/portfolio/new")}>
                <Plus className="h-4 w-4 mr-2" />
                Create First Item
              </Button>
            </div>
          )}
        </div>
      )}

      {view === "table" && (
        <DataTable
          columns={columns}
          data={tableData?.items || []}
          isLoading={tableLoading}
          searchKey="name"
          searchPlaceholder="Search portfolio..."
          enableRowSelection
          enableExport
          onRowClick={setSelectedItem}
        />
      )}

      {view === "gantt" && (
        <div className="border rounded-lg p-8 text-center">
          <GanttChart className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">
            Gantt view coming soon. Use Tree or Table view for now.
          </p>
        </div>
      )}

      {/* Detail Panel */}
      <SlideOver
        open={!!selectedItem}
        onOpenChange={(open) => !open && setSelectedItem(null)}
        title={selectedItem?.name || ""}
        description={selectedItem ? `${selectedItem.code} — ${selectedItem.level}` : ""}
        size="lg"
      >
        {selectedItem && (
          <div className="space-y-6">
            <SlideOverSection title="Status">
              <SlideOverGrid>
                <SlideOverField
                  label="Status"
                  value={
                    <Badge variant={statusVariants[selectedItem.status]} className="capitalize">
                      {selectedItem.status.replace("_", " ")}
                    </Badge>
                  }
                />
                <SlideOverField
                  label="RAG"
                  value={
                    selectedItem.rag_status ? (
                      <div className="flex items-center gap-2">
                        <div className={cn("w-4 h-4 rounded-full", ragColors[selectedItem.rag_status])} />
                        <span className="capitalize">{selectedItem.rag_status}</span>
                      </div>
                    ) : (
                      "—"
                    )
                  }
                />
              </SlideOverGrid>
            </SlideOverSection>

            {selectedItem.description && (
              <SlideOverSection title="Description">
                <p className="text-sm">{selectedItem.description}</p>
              </SlideOverSection>
            )}

            <SlideOverSection title="Timeline">
              <SlideOverGrid>
                <SlideOverField
                  label="Planned Start"
                  value={selectedItem.planned_start ? format(new Date(selectedItem.planned_start), "MMM d, yyyy") : "—"}
                />
                <SlideOverField
                  label="Planned End"
                  value={selectedItem.planned_end ? format(new Date(selectedItem.planned_end), "MMM d, yyyy") : "—"}
                />
                <SlideOverField
                  label="Actual Start"
                  value={selectedItem.actual_start ? format(new Date(selectedItem.actual_start), "MMM d, yyyy") : "—"}
                />
                <SlideOverField
                  label="Actual End"
                  value={selectedItem.actual_end ? format(new Date(selectedItem.actual_end), "MMM d, yyyy") : "—"}
                />
              </SlideOverGrid>
            </SlideOverSection>

            {(selectedItem.budget_approved || selectedItem.budget_spent) && (
              <SlideOverSection title="Budget">
                <SlideOverGrid cols={3}>
                  <SlideOverField
                    label="Approved"
                    value={selectedItem.budget_approved ? `${selectedItem.budget_currency} ${selectedItem.budget_approved.toLocaleString()}` : "—"}
                  />
                  <SlideOverField
                    label="Spent"
                    value={selectedItem.budget_spent ? `${selectedItem.budget_currency} ${selectedItem.budget_spent.toLocaleString()}` : "—"}
                  />
                  <SlideOverField
                    label="Forecast"
                    value={selectedItem.budget_forecast ? `${selectedItem.budget_currency} ${selectedItem.budget_forecast.toLocaleString()}` : "—"}
                  />
                </SlideOverGrid>
              </SlideOverSection>
            )}

            {selectedItem.wsvf_score && (
              <SlideOverSection title="WSVF Prioritization">
                <SlideOverGrid>
                  <SlideOverField label="Business Value" value={selectedItem.business_value || "—"} />
                  <SlideOverField label="Time Criticality" value={selectedItem.time_criticality || "—"} />
                  <SlideOverField label="Risk Reduction" value={selectedItem.risk_reduction || "—"} />
                  <SlideOverField label="Job Size" value={selectedItem.job_size || "—"} />
                </SlideOverGrid>
                <div className="mt-4 p-3 bg-muted rounded-md">
                  <span className="text-sm text-muted-foreground">WSVF Score</span>
                  <p className="text-2xl font-semibold">{selectedItem.wsvf_score.toFixed(2)}</p>
                </div>
              </SlideOverSection>
            )}
          </div>
        )}
      </SlideOver>
    </div>
  );
}
