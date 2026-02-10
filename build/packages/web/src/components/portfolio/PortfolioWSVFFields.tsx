"use client";

import { useFormContext } from "react-hook-form";
import { Input } from "@/components/ui/input";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

function calculateWSVF(bv: number, tc: number, rr: number, js: number): number | null {
  if (!js || js === 0) return null;
  return (bv + tc + rr) / js;
}

export function PortfolioWSVFFields() {
  const form = useFormContext();
  const bv = form.watch("business_value") || 0;
  const tc = form.watch("time_criticality") || 0;
  const rr = form.watch("risk_reduction") || 0;
  const js = form.watch("job_size") || 0;

  const wsvfScore = calculateWSVF(
    Number(bv),
    Number(tc),
    Number(rr),
    Number(js)
  );

  const fields = [
    { name: "business_value" as const, label: "Business Value (1-10)" },
    { name: "time_criticality" as const, label: "Time Criticality (1-10)" },
    { name: "risk_reduction" as const, label: "Risk Reduction (1-10)" },
    { name: "job_size" as const, label: "Job Size (1-10)" },
  ];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        {fields.map((f) => (
          <FormField
            key={f.name}
            control={form.control}
            name={f.name}
            render={({ field }) => (
              <FormItem>
                <FormLabel>{f.label}</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    min={1}
                    max={10}
                    placeholder="1-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : undefined)}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        ))}
      </div>

      {wsvfScore !== null && (
        <div className="p-3 bg-muted rounded-md">
          <span className="text-sm text-muted-foreground">
            WSVF Score = ({bv} + {tc} + {rr}) / {js}
          </span>
          <p className="text-2xl font-semibold">{wsvfScore.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}
