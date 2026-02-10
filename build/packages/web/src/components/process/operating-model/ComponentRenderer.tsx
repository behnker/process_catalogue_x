import type {
  OperatingModelComponent,
  OperatingModelComponentType,
  ProcessSystemLink,
  ProcessRaci,
  ProcessKpi,
  ProcessGovernance,
  ProcessPolicy,
  ProcessTiming,
  ProcessSipoc,
} from "@/types/api";
import { SystemsRenderer } from "./SystemsRenderer";
import { GovernanceRenderer } from "./GovernanceRenderer";
import { RACIRenderer } from "./RACIRenderer";
import { KPIsRenderer } from "./KPIsRenderer";
import { PoliciesRenderer } from "./PoliciesRenderer";
import { TimingRenderer } from "./TimingRenderer";
import { SIPOCRenderer } from "./SIPOCRenderer";
import { GenericRenderer } from "./GenericRenderer";
import { EmptyState } from "./EmptyState";

interface RelationalData {
  raci?: ProcessRaci[];
  kpis?: ProcessKpi[];
  governance?: ProcessGovernance[];
  policies?: ProcessPolicy[];
  timing?: ProcessTiming[];
  sipoc?: ProcessSipoc[];
}

interface ComponentRendererProps {
  componentType: OperatingModelComponentType;
  component?: OperatingModelComponent;
  systems?: ProcessSystemLink[];
  relational?: RelationalData;
  label: string;
}

export function ComponentRenderer({
  componentType,
  component,
  systems,
  relational,
  label,
}: ComponentRendererProps) {
  // Systems uses dedicated API, not JSONB
  if (componentType === "systems") {
    return <SystemsRenderer systems={systems ?? []} />;
  }

  // Relational components — typed renderers with relational data as primary source
  switch (componentType) {
    case "raci":
      return <RACIRenderer items={relational?.raci} data={component?.current_state} />;
    case "kpis":
      return <KPIsRenderer items={relational?.kpis} data={component?.current_state} />;
    case "governance":
      return <GovernanceRenderer items={relational?.governance} data={component?.current_state} />;
    case "policies":
      return <PoliciesRenderer items={relational?.policies ?? []} />;
    case "timing":
      return <TimingRenderer items={relational?.timing ?? []} />;
    case "sipoc":
      return <SIPOCRenderer items={relational?.sipoc ?? []} />;
    default:
      break;
  }

  // JSONB-only components (resources, security, data)
  const data = component?.current_state;
  if (!data || Object.keys(data).length === 0) {
    return <EmptyState label={label} />;
  }

  return <GenericRenderer data={data} label={label} />;
}
