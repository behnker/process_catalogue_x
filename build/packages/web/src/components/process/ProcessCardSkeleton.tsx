export function ProcessCardSkeleton({ variant = "l2" }: { variant?: "l0" | "l1" | "l2" | "l3" }) {
  if (variant === "l0") {
    return (
      <div className="p-4 bg-slate-50 border rounded-lg animate-pulse">
        <div className="h-3 w-12 bg-slate-200 rounded mb-2" />
        <div className="h-6 w-32 bg-slate-200 rounded" />
      </div>
    );
  }

  if (variant === "l1") {
    return (
      <div className="pb-2 border-b border-slate-200 animate-pulse">
        <div className="h-4 w-24 bg-slate-200 rounded" />
      </div>
    );
  }

  if (variant === "l3") {
    return (
      <div className="py-2 px-3 animate-pulse">
        <div className="h-4 w-32 bg-slate-200 rounded" />
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-lg border-l-[3px] border-l-slate-200 animate-pulse">
      <div className="p-3">
        <div className="h-5 w-3/4 bg-slate-200 rounded" />
      </div>
    </div>
  );
}
