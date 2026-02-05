"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useProcesses } from "@/hooks/useProcesses";
import { useCreateIssue, useUpdateIssue } from "@/hooks/useIssues";
import {
  IssueClassificationRow,
  IssueStatusField,
  IssueResolutionFields,
  IssueOpportunityFields,
} from "@/components/issues/IssueFormFields";
import type { Issue, IssueCreate, IssueUpdate } from "@/types/issue.types";

const issueFormSchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  description: z.string().optional(),
  issue_classification: z.enum(["people", "process", "system", "data"]),
  issue_criticality: z.enum(["high", "medium", "low"]),
  issue_complexity: z.enum(["high", "medium", "low"]),
  issue_status: z.enum(["open", "in_progress", "resolved", "closed", "deferred"]).optional(),
  process_id: z.string().min(1, "Process is required"),
  target_resolution_date: z.string().optional(),
  actual_resolution_date: z.string().optional(),
  resolution_summary: z.string().optional(),
  opportunity_flag: z.boolean().default(false),
  opportunity_description: z.string().optional(),
  opportunity_expected_benefit: z.string().optional(),
});

type IssueFormValues = z.infer<typeof issueFormSchema>;

interface IssueFormProps {
  issue?: Issue;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export function IssueForm({ issue, onSuccess, onCancel }: IssueFormProps) {
  const isEdit = !!issue;
  const createIssue = useCreateIssue();
  const updateIssue = useUpdateIssue();
  const { data: processesData, isLoading: processesLoading } = useProcesses({
    per_page: 500,
  });

  const form = useForm<IssueFormValues>({
    resolver: zodResolver(issueFormSchema),
    defaultValues: {
      title: issue?.title || "",
      description: issue?.description || "",
      issue_classification: issue?.issue_classification || "process",
      issue_criticality: issue?.issue_criticality || "medium",
      issue_complexity: issue?.issue_complexity || "medium",
      issue_status: issue?.issue_status || "open",
      process_id: issue?.process_id || "",
      target_resolution_date: issue?.target_resolution_date?.split("T")[0] || "",
      actual_resolution_date: issue?.actual_resolution_date?.split("T")[0] || "",
      resolution_summary: issue?.resolution_summary || "",
      opportunity_flag: issue?.opportunity_flag || false,
      opportunity_description: issue?.opportunity_description || "",
      opportunity_expected_benefit: issue?.opportunity_expected_benefit || "",
    },
  });

  const issueStatus = form.watch("issue_status");
  const showResolutionFields = isEdit && (issueStatus === "resolved" || issueStatus === "closed");

  const onSubmit = async (values: IssueFormValues) => {
    const payload: IssueCreate | IssueUpdate = {
      title: values.title,
      description: values.description || undefined,
      issue_classification: values.issue_classification,
      issue_criticality: values.issue_criticality,
      issue_complexity: values.issue_complexity,
      process_id: values.process_id,
      target_resolution_date: values.target_resolution_date || undefined,
      opportunity_flag: values.opportunity_flag,
      opportunity_description: values.opportunity_flag
        ? values.opportunity_description
        : undefined,
      opportunity_expected_benefit: values.opportunity_flag
        ? values.opportunity_expected_benefit
        : undefined,
      ...(isEdit && {
        issue_status: values.issue_status,
        actual_resolution_date: values.actual_resolution_date || undefined,
        resolution_summary: values.resolution_summary || undefined,
      }),
    };

    try {
      if (isEdit && issue) {
        await updateIssue.mutateAsync({ id: issue.id, data: payload });
      } else {
        await createIssue.mutateAsync(payload as IssueCreate);
      }
      onSuccess?.();
    } catch (error) {
      console.error("Failed to save issue:", error);
    }
  };

  const isPending = createIssue.isPending || updateIssue.isPending;

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Title */}
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title *</FormLabel>
              <FormControl>
                <Input placeholder="Brief description of the issue" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Description */}
        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Detailed description of the issue..."
                  rows={4}
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Process Selection */}
        <FormField
          control={form.control}
          name="process_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Process *</FormLabel>
              <Select
                onValueChange={field.onChange}
                defaultValue={field.value}
                disabled={processesLoading}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a process" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent className="max-h-[300px]">
                  {processesData?.items.map((process) => (
                    <SelectItem key={process.id} value={process.id}>
                      <span className="font-mono text-xs mr-2">{process.code}</span>
                      {process.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <IssueClassificationRow />

        {isEdit && <IssueStatusField />}

        {/* Target Date */}
        <FormField
          control={form.control}
          name="target_resolution_date"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Target Resolution Date</FormLabel>
              <FormControl>
                <Input type="date" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {showResolutionFields && <IssueResolutionFields />}

        <IssueOpportunityFields />

        {/* Actions */}
        <div className="flex justify-end gap-3 pt-4 border-t">
          {onCancel && (
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancel
            </Button>
          )}
          <Button type="submit" disabled={isPending}>
            {isPending ? "Saving..." : isEdit ? "Update Issue" : "Create Issue"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
