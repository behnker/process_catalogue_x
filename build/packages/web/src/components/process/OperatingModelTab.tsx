import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  useOperatingModel,
  useOperatingModelSummary,
  useProcessRaci,
  useProcessKpis,
  useProcessGovernance,
  useProcessPolicies,
  useProcessTiming,
  useProcessSipoc,
} from "@/hooks/useOperatingModel";
import { useProcessSystems } from "@/hooks/useProcessSystems";
import { ComponentRenderer } from "./operating-model/ComponentRenderer";
import type {
  OperatingModelComponent,
  OperatingModelComponentType,
} from "@/types/api";
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

// Types served by relational endpoints
const RELATIONAL_TYPES = new Set<string>(["raci", "kpis", "governance", "policies", "timing", "sipoc"]);

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

interface OperatingModelTabProps {
  processId: string;
}

function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-6 w-48" />
      <Skeleton className="h-2 w-full rounded-full" />
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-12 w-full" />
      ))}
    </div>
  );
}

function getItemCount(
  type: OperatingModelComponentType,
  component?: OperatingModelComponent,
  systemCount?: number,
  relationalCount?: number
): number | undefined {
  if (type === "systems") return systemCount;
  // For relational types, use the relational row count
  if (RELATIONAL_TYPES.has(type)) return relationalCount;
  if (!component) return undefined;
  const state = component.current_state;
  const firstArray = Object.values(state).find(Array.isArray);
  if (firstArray) return (firstArray as unknown[]).length;
  const keys = Object.keys(state);
  return keys.length > 0 ? keys.length : undefined;
}

export function OperatingModelTab({ processId }: OperatingModelTabProps) {
  const { data: components, isLoading: componentsLoading } =
    useOperatingModel(processId);
  const { data: summary, isLoading: summaryLoading } =
    useOperatingModelSummary(processId);
  const { data: systemsData } = useProcessSystems(processId);

  // Relational component hooks
  const { data: raciData } = useProcessRaci(processId);
  const { data: kpisData } = useProcessKpis(processId);
  const { data: governanceData } = useProcessGovernance(processId);
  const { data: policiesData } = useProcessPolicies(processId);
  const { data: timingData } = useProcessTiming(processId);
  const { data: sipocData } = useProcessSipoc(processId);

  if (componentsLoading || summaryLoading) {
    return <LoadingSkeleton />;
  }

  const componentMap = new Map<string, OperatingModelComponent>();
  if (components) {
    for (const c of components) {
      componentMap.set(c.component_type, c);
    }
  }

  const relational = {
    raci: raciData,
    kpis: kpisData,
    governance: governanceData,
    policies: policiesData,
    timing: timingData,
    sipoc: sipocData,
  };

  // Count map for relational types
  const relationalCounts: Record<string, number> = {
    raci: raciData?.length ?? 0,
    kpis: kpisData?.length ?? 0,
    governance: governanceData?.length ?? 0,
    policies: policiesData?.length ?? 0,
    timing: timingData?.length ?? 0,
    sipoc: sipocData?.length ?? 0,
  };

  const gapSet = new Set(summary?.components_with_gaps ?? []);
  const definedSet = new Set(summary?.defined_components ?? []);
  const defined = summary?.defined_components.length ?? 0;
  const total = summary?.total_components ?? 10;
  const pct = summary?.completion_percentage ?? 0;

  const systems = systemsData?.items ?? [];

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

      {gapSet.size > 0 && (
        <p className="text-xs text-amber-600 dark:text-amber-400">
          {gapSet.size} component{gapSet.size > 1 ? "s" : ""} with
          current/future state gaps
        </p>
      )}

      {/* Accordion layout */}
      <Accordion type="multiple" className="space-y-1">
        {ALL_COMPONENT_TYPES.map((type) => {
          const meta = COMPONENT_META[type] ?? { label: type, icon: FileText };
          const Icon = meta.icon;
          const component = componentMap.get(type);
          const isDefined = definedSet.has(type);
          const hasGap = gapSet.has(type);
          const count = getItemCount(
            type, component, systems.length, relationalCounts[type]
          );

          return (
            <AccordionItem key={type} value={type} className="border rounded-lg px-1">
              <AccordionTrigger className="hover:no-underline py-3 px-3">
                <div className="flex items-center gap-3 flex-1">
                  <Icon className="h-4 w-4 text-muted-foreground shrink-0" />
                  <span className="text-sm font-medium">{meta.label}</span>
                  {count !== undefined && count > 0 && (
                    <Badge variant="secondary" className="text-xs px-1.5 py-0">
                      {count}
                    </Badge>
                  )}
                  <div className="flex items-center gap-1.5 ml-auto mr-2">
                    {hasGap && <Badge variant="warning">Gap</Badge>}
                    {isDefined ? (
                      <Badge variant="success">Defined</Badge>
                    ) : (
                      <Badge variant="secondary">Not defined</Badge>
                    )}
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent className="px-3 pb-4">
                <ComponentRenderer
                  componentType={type}
                  component={component}
                  systems={systems}
                  relational={relational}
                  label={meta.label}
                />
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </div>
  );
}
