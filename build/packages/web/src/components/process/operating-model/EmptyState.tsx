import { FileText } from "lucide-react";

interface EmptyStateProps {
  label: string;
}

export function EmptyState({ label }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
      <FileText className="h-8 w-8 mb-2 opacity-50" />
      <p className="text-sm">{label} not yet defined</p>
    </div>
  );
}
