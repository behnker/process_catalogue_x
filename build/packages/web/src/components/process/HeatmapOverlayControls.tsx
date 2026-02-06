"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export type OverlayMode = "off" | "overall" | "dimensions";

interface HeatmapOverlayControlsProps {
  overlayMode: OverlayMode;
  onOverlayModeChange: (mode: OverlayMode) => void;
  rollup: boolean;
  onRollupChange: (rollup: boolean) => void;
}

const modes: { value: OverlayMode; label: string }[] = [
  { value: "off", label: "Off" },
  { value: "overall", label: "Overall" },
  { value: "dimensions", label: "Dimensions" },
];

export function HeatmapOverlayControls({
  overlayMode,
  onOverlayModeChange,
  rollup,
  onRollupChange,
}: HeatmapOverlayControlsProps) {
  return (
    <div className="flex items-center gap-2">
      {/* RAG Heatmap label */}
      <span className="text-xs text-muted-foreground font-medium whitespace-nowrap">
        RAG Overlay
      </span>

      {/* Segmented toggle */}
      <div className="flex items-center border rounded-md">
        {modes.map((mode) => (
          <Button
            key={mode.value}
            variant="ghost"
            size="sm"
            className={cn(
              "h-8 px-3 rounded-none text-xs",
              mode.value === "off" && "rounded-l-md",
              mode.value === "dimensions" && "rounded-r-md",
              overlayMode === mode.value &&
                "bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground"
            )}
            onClick={() => onOverlayModeChange(mode.value)}
          >
            {mode.label}
          </Button>
        ))}
      </div>

      {/* Rollup toggle — only shown when overlay is active */}
      {overlayMode !== "off" && (
        <label className="flex items-center gap-1.5 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={rollup}
            onChange={(e) => onRollupChange(e.target.checked)}
            className="h-3.5 w-3.5 rounded border-gray-300 text-primary accent-primary"
          />
          <span className="text-xs text-muted-foreground whitespace-nowrap">
            Include children
          </span>
        </label>
      )}
    </div>
  );
}
