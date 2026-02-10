import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { ProcessKpi } from "@/types/api";
import { EmptyState } from "./EmptyState";
import { GenericRenderer } from "./GenericRenderer";

interface KPIEntry {
  name: string;
  current_value?: string | number;
  target_value?: string | number;
  unit?: string;
  rag?: string;
  rag_status?: string;
  trend?: string;
  frequency?: string;
}

interface KPIsRendererProps {
  items?: ProcessKpi[];
  data?: Record<string, unknown>;
}

function isKPIArray(val: unknown): val is KPIEntry[] {
  return (
    Array.isArray(val) &&
    val.length > 0 &&
    typeof val[0] === "object" &&
    val[0] !== null &&
    "name" in val[0]
  );
}

const ragVariant = (rag?: string) => {
  switch (rag) {
    case "red": return "danger" as const;
    case "amber": return "warning" as const;
    case "green": return "success" as const;
    default: return "secondary" as const;
  }
};

function TrendIcon({ trend }: { trend?: string }) {
  if (trend === "up") return <TrendingUp className="h-3 w-3 text-green-600 dark:text-green-400" />;
  if (trend === "down") return <TrendingDown className="h-3 w-3 text-red-600 dark:text-red-400" />;
  return <Minus className="h-3 w-3 text-muted-foreground" />;
}

function KPICard({ kpi }: { kpi: KPIEntry }) {
  const rag = kpi.rag_status ?? kpi.rag;
  return (
    <div className="rounded-lg border p-3 space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">{kpi.name}</span>
        <div className="flex items-center gap-1.5">
          <TrendIcon trend={kpi.trend} />
          {rag && <Badge variant={ragVariant(rag)}>{rag}</Badge>}
        </div>
      </div>

      <div className="flex items-baseline gap-3">
        {kpi.current_value !== undefined && (
          <div>
            <span className="text-lg font-semibold">{kpi.current_value}</span>
            {kpi.unit && (
              <span className="text-xs text-muted-foreground ml-0.5">{kpi.unit}</span>
            )}
          </div>
        )}
        {kpi.target_value !== undefined && (
          <span className="text-xs text-muted-foreground">
            Target: {kpi.target_value}{kpi.unit ? ` ${kpi.unit}` : ""}
          </span>
        )}
      </div>

      {kpi.frequency && (
        <span className="text-xs text-muted-foreground">
          Measured {kpi.frequency.toLowerCase()}
        </span>
      )}
    </div>
  );
}

export function KPIsRenderer({ items, data }: KPIsRendererProps) {
  // Prefer typed relational data
  if (items && items.length > 0) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {items.map((kpi) => (
          <KPICard key={kpi.id} kpi={kpi} />
        ))}
      </div>
    );
  }

  // Fallback to JSONB data
  if (data) {
    const kpis = data.kpis ?? data.metrics ?? data.indicators;
    if (isKPIArray(kpis)) {
      return (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {kpis.map((kpi) => (
            <KPICard key={kpi.name} kpi={kpi} />
          ))}
        </div>
      );
    }
    const keys = Object.keys(data);
    if (keys.length > 0) return <GenericRenderer data={data} label="KPIs" />;
  }

  return <EmptyState label="KPIs" />;
}
