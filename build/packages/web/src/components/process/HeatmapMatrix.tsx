"use client";

import { RAGDot } from "@/components/shared/RAGBadge";
import { cn } from "@/lib/utils";
import type { HeatmapCell } from "@/types/issue.types";

interface HeatmapMatrixProps {
  cells: HeatmapCell[];
  onProcessClick?: (processId: string) => void;
}

const dimensions = [
  { key: "people_colour" as const, label: "People" },
  { key: "process_colour" as const, label: "Process" },
  { key: "system_colour" as const, label: "System" },
  { key: "data_colour" as const, label: "Data" },
  { key: "overall_colour" as const, label: "Overall" },
];

/**
 * Summary heatmap table: L0 rows × 5 dimension columns.
 * Each cell is a clickable RAGDot showing the RAG status.
 */
export function HeatmapMatrix({ cells, onProcessClick }: HeatmapMatrixProps) {
  const l0Cells = cells.filter((c) => c.level === "L0");

  if (l0Cells.length === 0) return null;

  return (
    <div className="border rounded-lg bg-white overflow-hidden">
      <div className="px-4 py-2 border-b bg-slate-50">
        <h3 className="text-sm font-semibold text-slate-700">RAG Heatmap Summary</h3>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-slate-50/50">
            <th className="text-left px-4 py-2 font-medium text-slate-600">Value Stream</th>
            {dimensions.map((dim) => (
              <th
                key={dim.key}
                className="text-center px-3 py-2 font-medium text-slate-600 w-20"
              >
                {dim.label}
              </th>
            ))}
            <th className="text-center px-3 py-2 font-medium text-slate-600 w-16">Issues</th>
          </tr>
        </thead>
        <tbody>
          {l0Cells.map((cell) => (
            <tr
              key={cell.process_id}
              className={cn(
                "border-b last:border-b-0 hover:bg-slate-50 transition-colors",
                onProcessClick && "cursor-pointer"
              )}
              onClick={() => onProcessClick?.(cell.process_id)}
            >
              <td className="px-4 py-2 font-medium text-slate-800 truncate max-w-[200px]" title={cell.process_name}>
                <span className="text-xs text-muted-foreground mr-1.5">{cell.process_ref}</span>
                {cell.process_name}
              </td>
              {dimensions.map((dim) => (
                <td key={dim.key} className="text-center px-3 py-2">
                  <div className="flex justify-center">
                    <RAGDot status={cell[dim.key]} size="md" />
                  </div>
                </td>
              ))}
              <td className="text-center px-3 py-2 text-slate-600 tabular-nums">
                {cell.total_issues}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
