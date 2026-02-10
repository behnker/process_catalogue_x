import { Badge } from "@/components/ui/badge";
import { Users, Gavel } from "lucide-react";
import type { ProcessGovernance } from "@/types/api";
import { EmptyState } from "./EmptyState";

interface GovernanceForum {
  name?: string;
  forum_name?: string;
  cadence?: string;
  attendees?: string[];
  decision_authority?: string;
  chair?: string;
}

interface GovernanceRendererProps {
  items?: ProcessGovernance[];
  data?: Record<string, unknown>;
}

function isForumArray(val: unknown): val is GovernanceForum[] {
  return Array.isArray(val) && val.length > 0 && typeof val[0] === "object" && val[0] !== null && ("name" in val[0] || "forum_name" in val[0]);
}

const cadenceBadgeVariant = (cadence: string) => {
  const lower = cadence.toLowerCase().replace(/_/g, " ");
  if (lower === "weekly") return "danger" as const;
  if (lower === "fortnightly" || lower === "biweekly") return "warning" as const;
  return "secondary" as const;
};

function ForumCard({ forum }: { forum: GovernanceForum }) {
  const name = forum.forum_name ?? forum.name;
  const cadenceLabel = forum.cadence?.replace(/_/g, " ");
  return (
    <div className="rounded-lg border p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Gavel className="h-4 w-4 text-muted-foreground" />
          <span className="font-medium text-sm">{name}</span>
        </div>
        {cadenceLabel && (
          <Badge variant={cadenceBadgeVariant(cadenceLabel)}>
            {cadenceLabel}
          </Badge>
        )}
      </div>

      {forum.decision_authority && (
        <p className="text-sm text-muted-foreground">
          {forum.decision_authority}
        </p>
      )}

      <div className="flex flex-wrap gap-4 text-xs">
        {forum.chair && (
          <div>
            <span className="text-muted-foreground">Chair: </span>
            <span className="font-medium">{forum.chair}</span>
          </div>
        )}
        {forum.attendees && forum.attendees.length > 0 && (
          <div className="flex items-center gap-1">
            <Users className="h-3 w-3 text-muted-foreground" />
            <span className="text-muted-foreground">
              {forum.attendees.join(", ")}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

export function GovernanceRenderer({ items, data }: GovernanceRendererProps) {
  // Prefer typed relational data
  if (items && items.length > 0) {
    return (
      <div className="space-y-3">
        {items.map((item) => (
          <ForumCard key={item.id} forum={item} />
        ))}
      </div>
    );
  }

  // Fallback to JSONB data
  if (data) {
    const forums = data.forums;
    if (isForumArray(forums)) {
      return (
        <div className="space-y-3">
          {forums.map((forum) => (
            <ForumCard key={forum.forum_name ?? forum.name} forum={forum} />
          ))}
        </div>
      );
    }
  }

  return <EmptyState label="Governance" />;
}
