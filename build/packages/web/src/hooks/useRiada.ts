"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  RiadaItem,
  RiadaItemCreate,
  RiadaItemUpdate,
  RiadaFilters,
} from "@/types/api";

const QUERY_KEY = "riada";

function buildQueryString(filters: RiadaFilters): string {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", filters.page.toString());
  if (filters.per_page) params.set("per_page", filters.per_page.toString());
  if (filters.riada_type) params.set("riada_type", filters.riada_type);
  if (filters.category) params.set("category", filters.category);
  if (filters.severity) params.set("severity", filters.severity);
  if (filters.status) params.set("status", filters.status);
  if (filters.process_id) params.set("process_id", filters.process_id);
  if (filters.search) params.set("search", filters.search);
  return params.toString();
}

export function useRiadaItems(filters: RiadaFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () => {
      const queryString = buildQueryString(filters);
      const url = queryString ? `/api/v1/riada?${queryString}` : "/api/v1/riada";
      return api.get<PaginatedResponse<RiadaItem>>(url);
    },
  });
}

export function useRiadaItem(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<RiadaItem>(`/api/v1/riada/${id}`),
    enabled: !!id,
  });
}

export function useRiadaByProcess(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "process", processId],
    queryFn: () => api.get<RiadaItem[]>(`/api/v1/processes/${processId}/riada`),
    enabled: !!processId,
  });
}

export function useCreateRiadaItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: RiadaItemCreate) =>
      api.post<RiadaItem>("/api/v1/riada", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdateRiadaItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: RiadaItemUpdate }) =>
      api.patch<RiadaItem>(`/api/v1/riada/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeleteRiadaItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/riada/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}
