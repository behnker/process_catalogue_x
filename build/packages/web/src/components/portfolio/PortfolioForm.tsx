"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { ArrowLeft, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { PortfolioBasicFields } from "@/components/portfolio/PortfolioBasicFields";
import { PortfolioWSVFFields } from "@/components/portfolio/PortfolioWSVFFields";
import { PortfolioTimelineBudgetFields } from "@/components/portfolio/PortfolioTimelineBudgetFields";
import { useCreatePortfolioItem, useUpdatePortfolioItem, usePortfolioItems } from "@/hooks/usePortfolioItems";
import type { PortfolioItem, PortfolioItemCreate, PortfolioItemUpdate } from "@/types/api";

const portfolioFormSchema = z.object({
  code: z.string().min(1, "Code is required").max(50),
  name: z.string().min(1, "Name is required").max(255),
  description: z.string().optional(),
  level: z.enum(["strategy", "portfolio", "programme", "project", "workstream", "epic", "task"]),
  parent_id: z.string().optional(),
  status: z.enum(["proposed", "approved", "in_progress", "on_hold", "completed", "cancelled"]),
  business_value: z.number().min(1).max(10).optional().nullable(),
  time_criticality: z.number().min(1).max(10).optional().nullable(),
  risk_reduction: z.number().min(1).max(10).optional().nullable(),
  job_size: z.number().min(1).max(10).optional().nullable(),
  planned_start: z.string().optional(),
  planned_end: z.string().optional(),
  actual_start: z.string().optional(),
  actual_end: z.string().optional(),
  budget_currency: z.string().optional(),
  budget_approved: z.number().min(0).optional().nullable(),
  budget_spent: z.number().min(0).optional().nullable(),
  budget_forecast: z.number().min(0).optional().nullable(),
  rag_status: z.enum(["red", "amber", "green"]).optional().nullable(),
  rag_notes: z.string().optional(),
});

type PortfolioFormValues = z.infer<typeof portfolioFormSchema>;

interface PortfolioFormProps {
  initialData?: PortfolioItem;
  children?: React.ReactNode;
}

function toFormValues(item: PortfolioItem): PortfolioFormValues {
  return {
    code: item.code,
    name: item.name,
    description: item.description || "",
    level: item.level,
    parent_id: item.parent_id || "",
    status: item.status,
    business_value: item.business_value ?? null,
    time_criticality: item.time_criticality ?? null,
    risk_reduction: item.risk_reduction ?? null,
    job_size: item.job_size ?? null,
    planned_start: item.planned_start || "",
    planned_end: item.planned_end || "",
    actual_start: item.actual_start || "",
    actual_end: item.actual_end || "",
    budget_currency: item.budget_currency || "USD",
    budget_approved: item.budget_approved ?? null,
    budget_spent: item.budget_spent ?? null,
    budget_forecast: item.budget_forecast ?? null,
    rag_status: item.rag_status ?? null,
    rag_notes: item.rag_notes || "",
  };
}

function stripEmpty<T extends Record<string, unknown>>(obj: T): Partial<T> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== "" && value !== null && value !== undefined) {
      result[key] = value;
    }
  }
  return result as Partial<T>;
}

export function PortfolioForm({ initialData, children }: PortfolioFormProps) {
  const router = useRouter();
  const isEdit = !!initialData;
  const createItem = useCreatePortfolioItem();
  const updateItem = useUpdatePortfolioItem();
  const { data: allItems } = usePortfolioItems({ per_page: 200 });

  const parentOptions = allItems?.items?.filter((p) => p.id !== initialData?.id) || [];

  const form = useForm<PortfolioFormValues>({
    resolver: zodResolver(portfolioFormSchema),
    defaultValues: initialData
      ? toFormValues(initialData)
      : {
          code: "",
          name: "",
          description: "",
          level: "project",
          parent_id: "",
          status: "proposed",
          budget_currency: "USD",
        },
  });

  const isPending = createItem.isPending || updateItem.isPending;

  async function onSubmit(values: PortfolioFormValues) {
    const cleaned = stripEmpty(values);

    if (isEdit) {
      await updateItem.mutateAsync({
        id: initialData!.id,
        data: cleaned as PortfolioItemUpdate,
      });
    } else {
      await createItem.mutateAsync(cleaned as PortfolioItemCreate);
    }
    router.push("/portfolio");
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => router.push("/portfolio")}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>
        <div>
          <h1 className="text-h1">{isEdit ? "Edit" : "Create"} Portfolio Item</h1>
          {isEdit && (
            <p className="text-sm text-muted-foreground mt-1">
              {initialData!.code} — {initialData!.name}
            </p>
          )}
        </div>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <Accordion type="multiple" defaultValue={["basic", "wsvf", "timeline"]}>
            <AccordionItem value="basic">
              <AccordionTrigger>Basic Information</AccordionTrigger>
              <AccordionContent className="pt-4">
                <PortfolioBasicFields parentOptions={parentOptions} />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="wsvf">
              <AccordionTrigger>WSVF Prioritisation</AccordionTrigger>
              <AccordionContent className="pt-4">
                <PortfolioWSVFFields />
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="timeline">
              <AccordionTrigger>Timeline & Budget</AccordionTrigger>
              <AccordionContent className="pt-4">
                <PortfolioTimelineBudgetFields isEdit={isEdit} />
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          {children}

          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button type="button" variant="outline" onClick={() => router.push("/portfolio")}>
              Cancel
            </Button>
            <Button type="submit" disabled={isPending}>
              {isPending && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
              {isEdit ? "Save Changes" : "Create Item"}
            </Button>
          </div>
        </form>
      </Form>
    </div>
  );
}
