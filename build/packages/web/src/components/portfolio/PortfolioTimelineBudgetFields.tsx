"use client";

import { useFormContext } from "react-hook-form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

interface PortfolioTimelineBudgetFieldsProps {
  isEdit?: boolean;
}

const CURRENCIES = ["USD", "GBP", "EUR", "AUD", "NZD", "CNY"] as const;

export function PortfolioTimelineBudgetFields({ isEdit }: PortfolioTimelineBudgetFieldsProps) {
  const form = useFormContext();

  return (
    <div className="space-y-6">
      <div>
        <h4 className="text-sm font-medium mb-3">Timeline</h4>
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="planned_start"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Planned Start</FormLabel>
                <FormControl>
                  <Input type="date" {...field} value={field.value || ""} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="planned_end"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Planned End</FormLabel>
                <FormControl>
                  <Input type="date" {...field} value={field.value || ""} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {isEdit && (
            <>
              <FormField
                control={form.control}
                name="actual_start"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Actual Start</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} value={field.value || ""} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="actual_end"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Actual End</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} value={field.value || ""} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </>
          )}
        </div>
      </div>

      <div>
        <h4 className="text-sm font-medium mb-3">Budget</h4>
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="budget_currency"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Currency</FormLabel>
                <Select onValueChange={field.onChange} value={field.value || "USD"}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {CURRENCIES.map((c) => (
                      <SelectItem key={c} value={c}>{c}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="budget_approved"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Approved Budget</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    min={0}
                    placeholder="0.00"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : undefined)}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          {isEdit && (
            <>
              <FormField
                control={form.control}
                name="budget_spent"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Spent</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        placeholder="0.00"
                        {...field}
                        value={field.value ?? ""}
                        onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : undefined)}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="budget_forecast"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Forecast</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min={0}
                        placeholder="0.00"
                        {...field}
                        value={field.value ?? ""}
                        onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : undefined)}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
