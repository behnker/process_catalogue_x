"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type { Issue, IssueCreate, IssueUpdate, IssueExportRequest } from "@/types/issue.types";

const QUERY_KEY = "issues";

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

      const disposition = response.headers.get("Content-Disposition");
      const filename = disposition?.match(/filename=(.+)/)?.[1] || `issues.${request.format}`;

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
