"use client";

import * as React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { ProcessCreate, ProcessLevel, ProcessType, LifecycleStatus, AutomationLevel } from "@/types/api";

const processSchema = z.object({
  name: z.string().min(1, "Name is required").max(255, "Name must be 255 characters or less"),
  description: z.string().optional(),
  level: z.enum(["L0", "L1", "L2", "L3", "L4", "L5"]),
  parent_id: z.string().optional(),
  process_type: z.enum(["primary", "secondary"]).optional(),
  status: z.enum(["draft", "active", "under_review", "deprecated", "archived"]).optional(),
  current_automation: z.enum(["manual", "semi_automated", "fully_automated", "ai_assisted"]).optional(),
  target_automation: z.enum(["manual", "semi_automated", "fully_automated", "ai_assisted"]).optional(),
});

type FormData = z.infer<typeof processSchema>;

interface ProcessFormProps {
  defaultValues?: Partial<ProcessCreate>;
  onSubmit: (data: ProcessCreate) => Promise<void>;
  onCancel: () => void;
  isSubmitting?: boolean;
  /** When true, level cannot be changed (used when creating under a specific parent) */
  lockLevel?: boolean;
}

const levelLabels: Record<ProcessLevel, string> = {
  L0: "L0 - Value Stream",
  L1: "L1 - Process Group",
  L2: "L2 - Process",
  L3: "L3 - Sub-Process",
  L4: "L4 - Variation",
  L5: "L5 - Task",
};

export function ProcessForm({
  defaultValues,
  onSubmit,
  onCancel,
  isSubmitting = false,
  lockLevel = false,
}: ProcessFormProps) {
  // Auto-lock level when parent_id is set (creating a child process)
  const isLevelLocked = lockLevel || !!defaultValues?.parent_id;
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(processSchema),
    defaultValues: {
      level: "L0",
      process_type: "primary",
      status: "draft",
      current_automation: "manual",
      ...defaultValues,
    },
  });

  const level = watch("level");
  const processType = watch("process_type");
  const status = watch("status");
  const currentAutomation = watch("current_automation");
  const targetAutomation = watch("target_automation");

  const handleFormSubmit = async (data: FormData) => {
    await onSubmit(data as ProcessCreate);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="level">Level *</Label>
        <Select
          value={level}
          onValueChange={(v) => setValue("level", v as ProcessLevel)}
          disabled={isLevelLocked}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {(Object.keys(levelLabels) as ProcessLevel[]).map((l) => (
              <SelectItem key={l} value={l}>
                {levelLabels[l]}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <p className="text-xs text-muted-foreground">
          {isLevelLocked
            ? "Level is set based on parent hierarchy"
            : "Code will be auto-generated based on hierarchy position"}
        </p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="name">Name *</Label>
        <Input
          id="name"
          placeholder="Process name"
          {...register("name")}
        />
        {errors.name && (
          <p className="text-sm text-destructive">{errors.name.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <textarea
          id="description"
          className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          placeholder="Brief description of the process"
          {...register("description")}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Type</Label>
          <Select
            value={processType}
            onValueChange={(v) => setValue("process_type", v as ProcessType)}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="primary">Primary</SelectItem>
              <SelectItem value="secondary">Secondary</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>Status</Label>
          <Select
            value={status}
            onValueChange={(v) => setValue("status", v as LifecycleStatus)}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="draft">Draft</SelectItem>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="under_review">Under Review</SelectItem>
              <SelectItem value="deprecated">Deprecated</SelectItem>
              <SelectItem value="archived">Archived</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Current Automation</Label>
          <Select
            value={currentAutomation}
            onValueChange={(v) => setValue("current_automation", v as AutomationLevel)}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="manual">Manual</SelectItem>
              <SelectItem value="semi_automated">Semi-Automated</SelectItem>
              <SelectItem value="fully_automated">Fully Automated</SelectItem>
              <SelectItem value="ai_assisted">AI Assisted</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>Target Automation</Label>
          <Select
            value={targetAutomation || ""}
            onValueChange={(v) => setValue("target_automation", v as AutomationLevel || undefined)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select..." />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="manual">Manual</SelectItem>
              <SelectItem value="semi_automated">Semi-Automated</SelectItem>
              <SelectItem value="fully_automated">Fully Automated</SelectItem>
              <SelectItem value="ai_assisted">AI Assisted</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : "Save Process"}
        </Button>
      </div>
    </form>
  );
}
