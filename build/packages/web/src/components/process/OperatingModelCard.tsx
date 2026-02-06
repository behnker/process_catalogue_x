import {
  ArrowRightLeft,
  Users,
  BarChart3,
  Shield,
  Landmark,
  Monitor,
  Clock,
  Bot,
  Lock,
  Database,
  type LucideIcon,
  FileText,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type {
  OperatingModelComponent,
  OperatingModelComponentType,
} from "@/types/api";

interface ComponentMeta {
  label: string;
  icon: LucideIcon;
}

const COMPONENT_META: Record<OperatingModelComponentType, ComponentMeta> = {
  sipoc: { label: "SIPOC", icon: ArrowRightLeft },
  raci: { label: "RACI", icon: Users },
  kpis: { label: "KPIs", icon: BarChart3 },
  policies: { label: "Policies & Rules", icon: Shield },
  governance: { label: "Governance", icon: Landmark },
  systems: { label: "Systems", icon: Monitor },
  timing: { label: "Timing & SLA", icon: Clock },
  resources: { label: "Agents & Resources", icon: Bot },
  security: { label: "Security", icon: Lock },
  data: { label: "Data", icon: Database },
};

interface OperatingModelCardProps {
  componentType: OperatingModelComponentType;
  component?: OperatingModelComponent;
  hasGap: boolean;
}

function getStatePreview(state: Record<string, unknown>): string[] {
  return Object.keys(state).slice(0, 4);
}

export function OperatingModelCard({
  componentType,
  component,
  hasGap,
}: OperatingModelCardProps) {
  const meta = COMPONENT_META[componentType] ?? {
    label: componentType,
    icon: FileText,
  };
  const Icon = meta.icon;
  const isDefined = !!component;
  const preview = isDefined ? getStatePreview(component.current_state) : [];

  return (
    <div className="rounded-lg border p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm font-medium">{meta.label}</span>
        </div>
        <div className="flex items-center gap-1.5">
          {hasGap && <Badge variant="warning">Gap</Badge>}
          {isDefined ? (
            <Badge variant="success">Defined</Badge>
          ) : (
            <Badge variant="secondary">Not defined</Badge>
          )}
        </div>
      </div>

      {isDefined && preview.length > 0 ? (
        <div className="flex flex-wrap gap-1.5">
          {preview.map((key) => (
            <span
              key={key}
              className="text-xs bg-muted px-2 py-0.5 rounded"
            >
              {key}
            </span>
          ))}
          {Object.keys(component.current_state).length > 4 && (
            <span className="text-xs text-muted-foreground">
              +{Object.keys(component.current_state).length - 4} more
            </span>
          )}
        </div>
      ) : (
        !isDefined && (
          <p className="text-xs text-muted-foreground">Not yet defined</p>
        )
      )}

      {component?.transition_notes && (
        <p className="text-xs text-muted-foreground truncate">
          {component.transition_notes}
        </p>
      )}
    </div>
  );
}
