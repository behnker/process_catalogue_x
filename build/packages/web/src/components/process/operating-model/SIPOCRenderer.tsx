import type { ProcessSipoc } from "@/types/api";
import { EmptyState } from "./EmptyState";

interface SIPOCRendererProps {
  items: ProcessSipoc[];
}

const ELEMENT_ORDER = ["supplier", "input", "output", "customer"] as const;

const ELEMENT_LABELS: Record<string, string> = {
  supplier: "Suppliers",
  input: "Inputs",
  output: "Outputs",
  customer: "Customers",
};

const ELEMENT_COLORS: Record<string, string> = {
  supplier: "border-l-blue-400",
  input: "border-l-green-400",
  output: "border-l-amber-400",
  customer: "border-l-purple-400",
};

export function SIPOCRenderer({ items }: SIPOCRendererProps) {
  if (items.length === 0) return <EmptyState label="SIPOC" />;

  const grouped = new Map<string, ProcessSipoc[]>();
  for (const type of ELEMENT_ORDER) {
    grouped.set(type, []);
  }
  for (const item of items) {
    const list = grouped.get(item.element_type);
    if (list) list.push(item);
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {ELEMENT_ORDER.map((type) => {
        const entries = grouped.get(type) ?? [];
        return (
          <div key={type} className="space-y-2">
            <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              {ELEMENT_LABELS[type]}
            </h4>
            {entries.length === 0 ? (
              <p className="text-xs text-muted-foreground italic">None defined</p>
            ) : (
              <ul className="space-y-1">
                {entries.map((e) => (
                  <li
                    key={e.id}
                    className={`border-l-2 ${ELEMENT_COLORS[type]} pl-2 py-1`}
                  >
                    <span className="text-sm font-medium">{e.name}</span>
                    {e.description && (
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {e.description}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        );
      })}
    </div>
  );
}
