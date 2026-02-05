"use client";

import { useFormContext } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
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

interface IssueFormFieldsProps {
  isEdit: boolean;
}

export function IssueClassificationRow() {
  const form = useFormContext();

  return (
    <div className="grid grid-cols-3 gap-4">
      <FormField
        control={form.control}
        name="issue_classification"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Classification *</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="people">People</SelectItem>
                <SelectItem value="process">Process</SelectItem>
                <SelectItem value="system">System</SelectItem>
                <SelectItem value="data">Data</SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="issue_criticality"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Criticality</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )}
      />

      <FormField
        control={form.control}
        name="issue_complexity"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Complexity</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
}

export function IssueStatusField() {
  const form = useFormContext();

  return (
    <FormField
      control={form.control}
      name="issue_status"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Status</FormLabel>
          <Select onValueChange={field.onChange} defaultValue={field.value}>
            <FormControl>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
            </FormControl>
            <SelectContent>
              <SelectItem value="open">Open</SelectItem>
              <SelectItem value="in_progress">In Progress</SelectItem>
              <SelectItem value="resolved">Resolved</SelectItem>
              <SelectItem value="closed">Closed</SelectItem>
              <SelectItem value="deferred">Deferred</SelectItem>
            </SelectContent>
          </Select>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

export function IssueResolutionFields() {
  const form = useFormContext();

  return (
    <div className="space-y-4 rounded-lg border border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-950/20 p-4">
      <p className="text-sm font-medium text-green-800 dark:text-green-200">Resolution Details</p>
      <FormField
        control={form.control}
        name="actual_resolution_date"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Resolution Date</FormLabel>
            <FormControl>
              <Input type="date" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
      <FormField
        control={form.control}
        name="resolution_summary"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Resolution Summary</FormLabel>
            <FormControl>
              <Textarea
                placeholder="How was this issue resolved?"
                rows={3}
                {...field}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
}

export function IssueOpportunityFields() {
  const form = useFormContext();
  const opportunityFlag = form.watch("opportunity_flag");

  return (
    <>
      <FormField
        control={form.control}
        name="opportunity_flag"
        render={({ field }) => (
          <FormItem className="flex items-center gap-2 space-y-0">
            <FormControl>
              <Checkbox
                checked={field.value}
                onCheckedChange={field.onChange}
              />
            </FormControl>
            <FormLabel className="font-normal">
              This issue represents an improvement opportunity
            </FormLabel>
          </FormItem>
        )}
      />

      {opportunityFlag && (
        <div className="space-y-4 pl-6 border-l-2 border-green-200 dark:border-green-800">
          <FormField
            control={form.control}
            name="opportunity_description"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Opportunity Description</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Describe the improvement opportunity..."
                    rows={3}
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="opportunity_expected_benefit"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Expected Benefit</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="What benefits would this improvement deliver?"
                    rows={2}
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
      )}
    </>
  );
}
