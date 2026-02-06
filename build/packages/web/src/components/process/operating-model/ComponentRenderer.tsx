import type {
  OperatingModelComponent,
  OperatingModelComponentType,
  ProcessSystemLink,
} from "@/types/api";
import { SystemsRenderer } from "./SystemsRenderer";
import { GovernanceRenderer } from "./GovernanceRenderer";
import { RACIRenderer } from "./RACIRenderer";
import { KPIsRenderer } from "./KPIsRenderer";
import { GenericRenderer } from "./GenericRenderer";
import { EmptyState } from "./EmptyState";

interface ComponentRendererProps {
  componentType: OperatingModelComponentType;
  component?: OperatingModelComponent;
  systems?: ProcessSystemLink[];
  label: string;
}

export function ComponentRenderer({
  componentType,
  component,
  systems,
  label,
}: ComponentRendererProps) {
  // Systems uses dedicated API, not JSONB
  if (componentType === "systems") {
    return <SystemsRenderer systems={systems ?? []} />;
  }

  const data = component?.current_state;
  if (!data || Object.keys(data).length === 0) {
    return <EmptyState label={label} />;
  }

  switch (componentType) {
    case "governance":
      return <GovernanceRenderer data={data} />;
    case "raci":
      return <RACIRenderer data={data} />;
    case "kpis":
      return <KPIsRenderer data={data} />;
    default:
      return <GenericRenderer data={data} label={label} />;
  }
}
