import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { EmptyState } from "./EmptyState";
import { GenericRenderer } from "./GenericRenderer";

interface KPIEntry {
  name: string;
  current_value?: string | number;
  target_value?: string | number;
  unit?: string;
  rag?: string;
  trend?: "up" | "down" | "flat";
  frequency?: string;
}

interface KPIsRendererProps {
  data: Record<string, unknown>;
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

export function KPIsRenderer({ data }: KPIsRendererProps) {
  const kpis = data.kpis ?? data.metrics ?? data.indicators;

  if (!isKPIArray(kpis)) {
    const keys = Object.keys(data);
    if (keys.length === 0) return <EmptyState label="KPIs" />;
    return <GenericRenderer data={data} label="KPIs" />;
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {kpis.map((kpi) => (
        <div key={kpi.name} className="rounded-lg border p-3 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">{kpi.name}</span>
            <div className="flex items-center gap-1.5">
              <TrendIcon trend={kpi.trend} />
              {kpi.rag && (
                <Badge variant={ragVariant(kpi.rag)}>{kpi.rag}</Badge>
              )}
            </div>
          </div>

          <div className="flex items-baseline gap-3">
            {kpi.current_value !== undefined && (
              <div>
                <span className="text-lg font-semibold">
                  {kpi.current_value}
                </span>
                {kpi.unit && (
                  <span className="text-xs text-muted-foreground ml-0.5">
                    {kpi.unit}
                  </span>
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
      ))}
    </div>
  );
}
