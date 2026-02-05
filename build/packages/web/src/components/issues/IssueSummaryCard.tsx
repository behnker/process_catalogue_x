interface IssueSummaryCardProps {
  label: string;
  value: number;
  variant: "blue" | "amber" | "red" | "purple" | "green";
}

const colors = {
  blue: "bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800",
  amber: "bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800",
  red: "bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800",
  purple: "bg-purple-50 dark:bg-purple-950/30 border-purple-200 dark:border-purple-800",
  green: "bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800",
};

export function IssueSummaryCard({ label, value, variant }: IssueSummaryCardProps) {
  return (
    <div className={`rounded-lg border p-4 ${colors[variant]}`}>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-sm text-muted-foreground">{label}</div>
    </div>
  );
}
