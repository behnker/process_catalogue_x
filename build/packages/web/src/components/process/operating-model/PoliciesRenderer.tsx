import { Badge } from "@/components/ui/badge";
import type { ProcessPolicy } from "@/types/api";
import { EmptyState } from "./EmptyState";

interface PoliciesRendererProps {
  items: ProcessPolicy[];
}

const typeBadgeVariant = (type: string) => {
  switch (type) {
    case "regulatory": return "danger" as const;
    case "policy": return "default" as const;
    case "business_rule": return "warning" as const;
    default: return "secondary" as const;
  }
};

export function PoliciesRenderer({ items }: PoliciesRendererProps) {
  if (items.length === 0) return <EmptyState label="Policies & Rules" />;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b">
            <th className="text-left px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase">
              Policy
            </th>
            <th className="text-left px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-28">
              Type
            </th>
            <th className="text-left px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase">
              Compliance
            </th>
            <th className="text-left px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-28">
              Last Reviewed
            </th>
            <th className="text-center px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-20">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {items.map((p) => (
            <tr key={p.id} className="border-b last:border-0">
              <td className="px-2 py-1.5">
                <div className="font-medium text-sm">{p.name}</div>
                {p.description && (
                  <div className="text-xs text-muted-foreground mt-0.5 line-clamp-1">
                    {p.description}
                  </div>
                )}
              </td>
              <td className="px-2 py-1.5">
                <Badge variant={typeBadgeVariant(p.policy_type)}>
                  {p.policy_type.replace(/_/g, " ")}
                </Badge>
              </td>
              <td className="px-2 py-1.5 text-xs text-muted-foreground">
                {p.compliance_requirement || "—"}
              </td>
              <td className="px-2 py-1.5 text-xs text-muted-foreground">
                {p.last_reviewed || "—"}
              </td>
              <td className="px-2 py-1.5 text-center">
                <Badge variant={p.is_active ? "success" : "secondary"}>
                  {p.is_active ? "Active" : "Inactive"}
                </Badge>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
