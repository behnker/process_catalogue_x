import { Badge } from "@/components/ui/badge";
import { Clock, Zap } from "lucide-react";
import type { ProcessTiming } from "@/types/api";
import { EmptyState } from "./EmptyState";

interface TimingRendererProps {
  items: ProcessTiming[];
}

export function TimingRenderer({ items }: TimingRendererProps) {
  if (items.length === 0) return <EmptyState label="Timing & SLA" />;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {items.map((t) => (
        <div key={t.id} className="rounded-lg border p-3 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">{t.name}</span>
            </div>
            {t.frequency && (
              <Badge variant="secondary">{t.frequency.replace(/_/g, " ")}</Badge>
            )}
          </div>

          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs">
            {t.volume_per_period && (
              <div>
                <span className="text-muted-foreground">Volume: </span>
                <span className="font-medium">{t.volume_per_period}</span>
              </div>
            )}
            {t.cycle_time_target && (
              <div>
                <span className="text-muted-foreground">Target: </span>
                <span className="font-medium">{t.cycle_time_target}</span>
              </div>
            )}
            {t.cycle_time_actual && (
              <div>
                <span className="text-muted-foreground">Actual: </span>
                <span className="font-medium">{t.cycle_time_actual}</span>
              </div>
            )}
            {t.peak_season && (
              <div>
                <span className="text-muted-foreground">Peak: </span>
                <span className="font-medium">{t.peak_season}</span>
              </div>
            )}
          </div>

          {t.sla_commitment && (
            <div className="flex items-start gap-1.5 text-xs">
              <Zap className="h-3 w-3 text-amber-500 mt-0.5 shrink-0" />
              <span className="text-muted-foreground">{t.sla_commitment}</span>
            </div>
          )}

          {t.trigger_event && (
            <p className="text-xs text-muted-foreground">
              <span className="font-medium">Trigger:</span> {t.trigger_event}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
