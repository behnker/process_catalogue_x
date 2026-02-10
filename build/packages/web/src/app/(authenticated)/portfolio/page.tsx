"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { ColumnDef } from "@tanstack/react-table";
import { format } from "date-fns";
import {
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
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";
import { PortfolioTreeNode, levelColors, statusVariants, ragColors } from "@/components/portfolio/PortfolioTreeNode";
import { PortfolioDetailPanel } from "@/components/portfolio/PortfolioDetailPanel";
import { usePortfolioItems, usePortfolioTree, useDeletePortfolioItem } from "@/hooks/usePortfolioItems";
import type { PortfolioItem, PortfolioLevel, PortfolioStatus, RagStatus } from "@/types/api";
import { cn } from "@/lib/utils";

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
      cell: ({ row }) => <span className="font-mono text-sm">{row.getValue("code")}</span>,
    },
    {
      accessorKey: "name",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
      cell: ({ row }) => <span className="font-medium">{row.getValue("name")}</span>,
    },
    {
      accessorKey: "level",
      header: "Level",
      cell: ({ row }) => {
        const level = row.getValue("level") as PortfolioLevel;
        return (
          <div className="flex items-center gap-2">
            <div className={cn("w-2 h-2 rounded-full", levelColors[level])} />
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
        return date ? format(new Date(date), "MMM d, yyyy") : "—";
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
              <TabsTrigger value="tree"><FolderTree className="h-4 w-4" /></TabsTrigger>
              <TabsTrigger value="table"><TableIcon className="h-4 w-4" /></TabsTrigger>
              <TabsTrigger value="gantt"><GanttChart className="h-4 w-4" /></TabsTrigger>
            </TabsList>
          </Tabs>
          <Button onClick={() => router.push("/portfolio/new")}>
            <Plus className="h-4 w-4 mr-2" />
            Create Item
          </Button>
        </div>
      </div>

      {view === "tree" && (
        <div className="border rounded-lg">
          {treeLoading ? (
            <div className="p-8 text-center text-muted-foreground">Loading...</div>
          ) : treeData && treeData.length > 0 ? (
            <div className="py-2">
              {treeData.map((item) => (
                <PortfolioTreeNode
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

      <PortfolioDetailPanel item={selectedItem} onClose={() => setSelectedItem(null)} />
    </div>
  );
}
