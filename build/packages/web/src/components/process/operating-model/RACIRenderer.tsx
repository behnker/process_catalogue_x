import { cn } from "@/lib/utils";
import { EmptyState } from "./EmptyState";
import { GenericRenderer } from "./GenericRenderer";

interface RACIRendererProps {
  data: Record<string, unknown>;
}

interface RACIEntry {
  activity: string;
  responsible?: string;
  accountable?: string;
  consulted?: string;
  informed?: string;
}

function isRACIArray(val: unknown): val is RACIEntry[] {
  return (
    Array.isArray(val) &&
    val.length > 0 &&
    typeof val[0] === "object" &&
    val[0] !== null &&
    "activity" in val[0]
  );
}

const cellStyle = (letter: string) =>
  cn(
    "text-center text-xs font-medium rounded px-1 py-0.5",
    letter === "R" && "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
    letter === "A" && "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400",
    letter === "C" && "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400",
    letter === "I" && "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400"
  );

function RACICell({ value, letter }: { value?: string; letter: string }) {
  if (!value) return <td className="px-2 py-1.5 text-center text-xs text-muted-foreground">—</td>;
  return (
    <td className="px-2 py-1.5">
      <div className="flex flex-col items-center gap-0.5">
        <span className={cellStyle(letter)}>{letter}</span>
        <span className="text-xs text-muted-foreground text-center">{value}</span>
      </div>
    </td>
  );
}

export function RACIRenderer({ data }: RACIRendererProps) {
  const entries = data.matrix ?? data.entries ?? data.raci;

  if (!isRACIArray(entries)) {
    // Fall back to generic key-value if shape doesn't match
    const keys = Object.keys(data);
    if (keys.length === 0) return <EmptyState label="RACI" />;
    return <GenericRenderer data={data} label="RACI" />;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b">
            <th className="text-left px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase">
              Activity
            </th>
            <th className="text-center px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-24">
              Responsible
            </th>
            <th className="text-center px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-24">
              Accountable
            </th>
            <th className="text-center px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-24">
              Consulted
            </th>
            <th className="text-center px-2 py-1.5 text-xs font-medium text-muted-foreground uppercase w-24">
              Informed
            </th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, i) => (
            <tr key={i} className="border-b last:border-0">
              <td className="px-2 py-1.5 text-sm font-medium">
                {entry.activity}
              </td>
              <RACICell value={entry.responsible} letter="R" />
              <RACICell value={entry.accountable} letter="A" />
              <RACICell value={entry.consulted} letter="C" />
              <RACICell value={entry.informed} letter="I" />
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
