import { Badge } from "@/components/ui/badge";
import { Monitor, AlertCircle } from "lucide-react";
import { EmptyState } from "./EmptyState";
import type { ProcessSystemLink } from "@/types/api";

interface SystemsRendererProps {
  systems: ProcessSystemLink[];
}

const criticalityVariant = (criticality: string) => {
  switch (criticality) {
    case "critical": return "danger" as const;
    case "high": return "warning" as const;
    case "medium": return "secondary" as const;
    default: return "outline" as const;
  }
};

const roleLabel = (role: string) => {
  switch (role) {
    case "primary": return "Primary";
    case "secondary": return "Secondary";
    case "reference": return "Reference";
    case "integration_target": return "Integration Target";
    default: return role;
  }
};

export function SystemsRenderer({ systems }: SystemsRendererProps) {
  if (!systems || systems.length === 0) return <EmptyState label="Systems" />;

  return (
    <div className="space-y-3">
      {systems.map((link) => (
        <div key={link.id} className="rounded-lg border p-4 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Monitor className="h-4 w-4 text-muted-foreground" />
              <span className="font-medium text-sm">
                {link.system?.name ?? "Unknown System"}
              </span>
            </div>
            <div className="flex items-center gap-1.5">
              <Badge variant={criticalityVariant(link.criticality)}>
                {link.criticality}
              </Badge>
              <Badge variant="outline">{roleLabel(link.system_role)}</Badge>
            </div>
          </div>

          {link.purpose && (
            <p className="text-sm text-muted-foreground">{link.purpose}</p>
          )}

          <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
            {link.integration_method && (
              <span>
                Integration: <span className="text-foreground">{link.integration_method.replace(/_/g, " ")}</span>
              </span>
            )}
            {link.user_scope && (
              <span>
                Users: <span className="text-foreground">{link.user_scope}</span>
              </span>
            )}
            {link.automation_potential && link.automation_potential !== "none" && (
              <span>
                Automation: <span className="text-foreground">{link.automation_potential}</span>
              </span>
            )}
            {link.system?.system_type && (
              <span>
                Type: <span className="text-foreground">{link.system.system_type}</span>
              </span>
            )}
          </div>

          {link.pain_points && (
            <div className="flex items-start gap-1.5 text-xs text-amber-600 dark:text-amber-400">
              <AlertCircle className="h-3 w-3 mt-0.5 shrink-0" />
              <span>{link.pain_points}</span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
