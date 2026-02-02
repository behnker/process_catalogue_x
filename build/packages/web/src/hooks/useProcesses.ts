"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  Process,
  ProcessCreate,
  ProcessUpdate,
  ProcessFilters,
  ProcessReorder,
} from "@/types/api";

const QUERY_KEY = "processes";

function buildQueryString(filters: ProcessFilters): string {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", filters.page.toString());
  if (filters.per_page) params.set("per_page", filters.per_page.toString());
  if (filters.level) params.set("level", filters.level);
  if (filters.process_type) params.set("process_type", filters.process_type);
  if (filters.status) params.set("status", filters.status);
  if (filters.parent_id) params.set("parent_id", filters.parent_id);
  if (filters.search) params.set("search", filters.search);
  return params.toString();
}

export function useProcesses(filters: ProcessFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () => {
      const queryString = buildQueryString(filters);
      const url = queryString ? `/api/v1/processes?${queryString}` : "/api/v1/processes";
      return api.get<PaginatedResponse<Process>>(url);
    },
  });
}

export function useProcess(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<Process>(`/api/v1/processes/${id}`),
    enabled: !!id,
  });
}

export function useProcessTree() {
  return useQuery({
    queryKey: [QUERY_KEY, "tree"],
    queryFn: () => api.get<Process[]>("/api/v1/processes/tree"),
  });
}

export function useProcessChildren(parentId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "children", parentId],
    queryFn: () => api.get<Process[]>(`/api/v1/processes/${parentId}/children`),
    enabled: !!parentId,
  });
}

export function useCreateProcess() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ProcessCreate) =>
      api.post<Process>("/api/v1/processes", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdateProcess() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ProcessUpdate }) =>
      api.patch<Process>(`/api/v1/processes/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeleteProcess() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/processes/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useReorderProcess() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ProcessReorder) =>
      api.post<Process>("/api/v1/processes/reorder", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}
