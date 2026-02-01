"use client";

import { Search, Filter, ZoomIn, ZoomOut, Maximize2, Grid3X3 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { ProcessType, LifecycleStatus } from "@/types/api";

interface ProcessCanvasToolbarProps {
  search: string;
  onSearchChange: (value: string) => void;
  processType: ProcessType | "all";
  onProcessTypeChange: (value: ProcessType | "all") => void;
  statusFilter: LifecycleStatus[];
  onStatusFilterChange: (value: LifecycleStatus[]) => void;
  cardSize: "sm" | "md" | "lg";
  onCardSizeChange: (value: "sm" | "md" | "lg") => void;
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetZoom: () => void;
}

const statuses: LifecycleStatus[] = ["draft", "active", "under_review", "deprecated", "archived"];

export function ProcessCanvasToolbar({
  search,
  onSearchChange,
  processType,
  onProcessTypeChange,
  statusFilter,
  onStatusFilterChange,
  cardSize,
  onCardSizeChange,
  zoom,
  onZoomIn,
  onZoomOut,
  onResetZoom,
}: ProcessCanvasToolbarProps) {
  const toggleStatus = (status: LifecycleStatus) => {
    if (statusFilter.includes(status)) {
      onStatusFilterChange(statusFilter.filter((s) => s !== status));
    } else {
      onStatusFilterChange([...statusFilter, status]);
    }
  };

  return (
    <div className="flex items-center justify-between gap-4 p-4 border-b bg-background">
      <div className="flex items-center gap-2 flex-1">
        {/* Search */}
        <div className="relative max-w-xs">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search processes..."
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-9 w-[200px]"
          />
        </div>

        {/* Type Filter */}
        <Select value={processType} onValueChange={(v) => onProcessTypeChange(v as ProcessType | "all")}>
          <SelectTrigger className="w-[140px]">
            <SelectValue placeholder="Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="primary">Primary</SelectItem>
            <SelectItem value="secondary">Secondary</SelectItem>
          </SelectContent>
        </Select>

        {/* Status Filter */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Status
              {statusFilter.length > 0 && statusFilter.length < statuses.length && (
                <span className="ml-1 text-xs bg-primary text-primary-foreground rounded-full px-1.5">
                  {statusFilter.length}
                </span>
              )}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="w-[180px]">
            <DropdownMenuLabel>Filter by Status</DropdownMenuLabel>
            <DropdownMenuSeparator />
            {statuses.map((status) => (
              <DropdownMenuCheckboxItem
                key={status}
                checked={statusFilter.length === 0 || statusFilter.includes(status)}
                onCheckedChange={() => toggleStatus(status)}
                className="capitalize"
              >
                {status.replace("_", " ")}
              </DropdownMenuCheckboxItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="flex items-center gap-2">
        {/* Card Size */}
        <Select value={cardSize} onValueChange={(v) => onCardSizeChange(v as "sm" | "md" | "lg")}>
          <SelectTrigger className="w-[100px]">
            <Grid3X3 className="h-4 w-4 mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="sm">Small</SelectItem>
            <SelectItem value="md">Medium</SelectItem>
            <SelectItem value="lg">Large</SelectItem>
          </SelectContent>
        </Select>

        {/* Zoom Controls */}
        <div className="flex items-center gap-1 border rounded-md">
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onZoomOut}>
            <ZoomOut className="h-4 w-4" />
          </Button>
          <span className="text-sm w-12 text-center">{Math.round(zoom * 100)}%</span>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onZoomIn}>
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onResetZoom}>
            <Maximize2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
