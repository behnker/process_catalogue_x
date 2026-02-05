import { ColumnDef } from "@tanstack/react-table";
import { format } from "date-fns";
import { MoreHorizontal, Eye, Edit, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { DataTableColumnHeader } from "@/components/shared/DataTable";
import { IssueStatusBadge } from "@/components/issues/IssueStatusBadge";
import { CriticalityBadge } from "@/components/issues/CriticalityBadge";
import { ClassificationIcon } from "@/components/issues/ClassificationIcon";
import type { Issue } from "@/types/issue.types";

interface ColumnActions {
  onView: (issue: Issue) => void;
  onEdit: (issue: Issue) => void;
  onDelete: (id: string) => void;
}

export function getIssueColumns({ onView, onEdit, onDelete }: ColumnActions): ColumnDef<Issue>[] {
  return [
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
              <DropdownMenuItem onClick={() => onView(issue)}>
                <Eye className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onEdit(issue)}>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => onDelete(issue.id)}
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
}
