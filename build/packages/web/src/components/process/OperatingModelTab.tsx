import { Skeleton } from "@/components/ui/skeleton";
import {
  useOperatingModel,
  useOperatingModelSummary,
} from "@/hooks/useOperatingModel";
import { OperatingModelCard } from "./OperatingModelCard";
import type {
  OperatingModelComponent,
  OperatingModelComponentType,
} from "@/types/api";

const ALL_COMPONENT_TYPES: OperatingModelComponentType[] = [
  "sipoc",
  "raci",
  "kpis",
  "policies",
  "governance",
  "systems",
  "timing",
  "resources",
  "security",
  "data",
];

interface OperatingModelTabProps {
  processId: string;
}

function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-6 w-48" />
      <Skeleton className="h-2 w-full rounded-full" />
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {Array.from({ length: 10 }).map((_, i) => (
          <Skeleton key={i} className="h-24 w-full" />
        ))}
      </div>
    </div>
  );
}

export function OperatingModelTab({ processId }: OperatingModelTabProps) {
  const { data: components, isLoading: componentsLoading } =
    useOperatingModel(processId);
  const { data: summary, isLoading: summaryLoading } =
    useOperatingModelSummary(processId);

  if (componentsLoading || summaryLoading) {
    return <LoadingSkeleton />;
  }

  const componentMap = new Map<string, OperatingModelComponent>();
  if (components) {
    for (const c of components) {
      componentMap.set(c.component_type, c);
    }
  }

  const gapSet = new Set(summary?.components_with_gaps ?? []);
  const defined = summary?.defined_components.length ?? 0;
  const total = summary?.total_components ?? 10;
  const pct = summary?.completion_percentage ?? 0;

  return (
    <div className="space-y-4">
      {/* Completion summary */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">
            {defined}/{total} components defined
          </span>
          <span className="font-medium">{pct}%</span>
        </div>
        <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {/* Components with gaps callout */}
      {gapSet.size > 0 && (
        <p className="text-xs text-amber-600 dark:text-amber-400">
          {gapSet.size} component{gapSet.size > 1 ? "s" : ""} with
          current/future state gaps
        </p>
      )}

      {/* Component grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {ALL_COMPONENT_TYPES.map((type) => (
          <OperatingModelCard
            key={type}
            componentType={type}
            component={componentMap.get(type)}
            hasGap={gapSet.has(type)}
          />
        ))}
      </div>
    </div>
  );
}
