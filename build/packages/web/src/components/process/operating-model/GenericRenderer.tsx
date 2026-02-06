import { EmptyState } from "./EmptyState";

interface GenericRendererProps {
  data: Record<string, unknown>;
  label: string;
}

function renderValue(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (Array.isArray(value)) return value.map(renderValue).join(", ");
  if (typeof value === "object") return JSON.stringify(value, null, 2);
  return String(value);
}

function isSimpleValue(value: unknown): boolean {
  return (
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean" ||
    value === null ||
    value === undefined
  );
}

export function GenericRenderer({ data, label }: GenericRendererProps) {
  const entries = Object.entries(data);
  if (entries.length === 0) return <EmptyState label={label} />;

  return (
    <div className="space-y-3">
      {entries.map(([key, value]) => (
        <div key={key} className="rounded-lg border p-3">
          <dt className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-1">
            {key.replace(/_/g, " ")}
          </dt>
          {isSimpleValue(value) ? (
            <dd className="text-sm">{renderValue(value)}</dd>
          ) : Array.isArray(value) ? (
            <dd className="text-sm">
              {value.length === 0 ? (
                <span className="text-muted-foreground">—</span>
              ) : (
                <ul className="list-disc list-inside space-y-0.5">
                  {value.map((item, i) => (
                    <li key={i}>{renderValue(item)}</li>
                  ))}
                </ul>
              )}
            </dd>
          ) : (
            <dd className="text-sm whitespace-pre-wrap font-mono text-xs bg-muted rounded p-2">
              {renderValue(value)}
            </dd>
          )}
        </div>
      ))}
    </div>
  );
}
