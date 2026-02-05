"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type { PaginatedResponse } from "@/types/api";
import type {
  Issue,
  IssueCreate,
  IssueUpdate,
  IssueFilters,
  IssueSummary,
  IssueHistory,
  HeatmapResponse,
  IssueExportRequest,
} from "@/types/issue.types";

const QUERY_KEY = "issues";

function buildQueryString(filters: IssueFilters): string {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", filters.page.toString());
  if (filters.per_page) params.set("per_page", filters.per_page.toString());
  if (filters.status_filter) params.set("status_filter", filters.status_filter);
  if (filters.classification) params.set("classification", filters.classification);
  if (filters.criticality) params.set("criticality", filters.criticality);
  if (filters.process_id) params.set("process_id", filters.process_id);
  if (filters.assigned_to) params.set("assigned_to", filters.assigned_to);
  return params.toString();
}

// List issues with pagination and filters
export function useIssues(filters: IssueFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () => {
      const queryString = buildQueryString(filters);
      const url = queryString ? `/api/v1/issues?${queryString}` : "/api/v1/issues";
      return api.get<PaginatedResponse<Issue>>(url);
    },
  });
}

// Get single issue by ID
export function useIssue(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<Issue>(`/api/v1/issues/${id}`),
    enabled: !!id,
  });
}

// Get issues for a specific process
export function useProcessIssues(
  processId: string | undefined,
  options: {
    includeDescendants?: boolean;
    statusFilter?: string;
    page?: number;
    perPage?: number;
  } = {}
) {
  const { includeDescendants = false, statusFilter, page = 1, perPage = 50 } = options;

  return useQuery({
    queryKey: [QUERY_KEY, "process", processId, options],
    queryFn: () => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("per_page", perPage.toString());
      if (includeDescendants) params.set("include_descendants", "true");
      if (statusFilter) params.set("status_filter", statusFilter);
      return api.get<PaginatedResponse<Issue>>(
        `/api/v1/processes/${processId}/issues?${params.toString()}`
      );
    },
    enabled: !!processId,
  });
}

// Create new issue
export function useCreateIssue() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: IssueCreate) =>
      api.post<Issue>("/api/v1/issues", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: ["processes"] });
    },
  });
}

// Update issue
export function useUpdateIssue() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: IssueUpdate }) =>
      api.patch<Issue>(`/api/v1/issues/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
      queryClient.invalidateQueries({ queryKey: ["processes"] });
    },
  });
}

// Delete issue
export function useDeleteIssue() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/issues/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: ["processes"] });
    },
  });
}

// Get issue history
export function useIssueHistory(issueId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "history", issueId],
    queryFn: () => api.get<IssueHistory>(`/api/v1/issues/${issueId}/history`),
    enabled: !!issueId,
  });
}

// Get issue summary/stats
export function useIssueSummary() {
  return useQuery({
    queryKey: [QUERY_KEY, "summary"],
    queryFn: () => api.get<IssueSummary>("/api/v1/issues/summary"),
  });
}

// Get heatmap data
export function useIssueHeatmap(rollup: boolean = false) {
  return useQuery({
    queryKey: [QUERY_KEY, "heatmap", { rollup }],
    queryFn: () => api.get<HeatmapResponse>(`/api/v1/issues/heatmap?rollup=${rollup}`),
  });
}

// Export issues
export function useExportIssues() {
  return useMutation({
    mutationFn: async (request: IssueExportRequest) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/issues/export`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("pc-auth") ? JSON.parse(localStorage.getItem("pc-auth")!).state?.accessToken : ""}`,
          },
          body: JSON.stringify(request),
        }
      );

      if (!response.ok) {
        throw new Error("Export failed");
      }

      // Get filename from Content-Disposition header
      const disposition = response.headers.get("Content-Disposition");
      const filename = disposition?.match(/filename=(.+)/)?.[1] || `issues.${request.format}`;

      // Create download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    },
  });
}
