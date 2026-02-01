"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  PortfolioItem,
  PortfolioMilestone,
  PortfolioItemCreate,
  PortfolioItemUpdate,
  PortfolioFilters,
} from "@/types/api";

const QUERY_KEY = "portfolio";

function buildQueryString(filters: PortfolioFilters): string {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", filters.page.toString());
  if (filters.per_page) params.set("per_page", filters.per_page.toString());
  if (filters.level) params.set("level", filters.level);
  if (filters.status) params.set("status", filters.status);
  if (filters.parent_id) params.set("parent_id", filters.parent_id);
  if (filters.search) params.set("search", filters.search);
  return params.toString();
}

export function usePortfolioItems(filters: PortfolioFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () => {
      const queryString = buildQueryString(filters);
      const url = queryString ? `/api/v1/portfolio?${queryString}` : "/api/v1/portfolio";
      return api.get<PaginatedResponse<PortfolioItem>>(url);
    },
  });
}

export function usePortfolioItem(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<PortfolioItem>(`/api/v1/portfolio/${id}`),
    enabled: !!id,
  });
}

export function usePortfolioTree() {
  return useQuery({
    queryKey: [QUERY_KEY, "tree"],
    queryFn: () => api.get<PortfolioItem[]>("/api/v1/portfolio/tree"),
  });
}

export function usePortfolioChildren(parentId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "children", parentId],
    queryFn: () => api.get<PortfolioItem[]>(`/api/v1/portfolio/${parentId}/children`),
    enabled: !!parentId,
  });
}

export function useCreatePortfolioItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PortfolioItemCreate) =>
      api.post<PortfolioItem>("/api/v1/portfolio", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdatePortfolioItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: PortfolioItemUpdate }) =>
      api.patch<PortfolioItem>(`/api/v1/portfolio/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeletePortfolioItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/portfolio/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

// Milestones
export function useCreateMilestone() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { portfolio_item_id: string; name: string; due_date?: string }) =>
      api.post<PortfolioMilestone>(
        `/api/v1/portfolio/${data.portfolio_item_id}/milestones`,
        data
      ),
    onSuccess: (_, { portfolio_item_id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, portfolio_item_id] });
    },
  });
}

export function useUpdateMilestone() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: Partial<{ name: string; due_date: string; status: string; completed_date: string }>;
    }) => api.patch<PortfolioMilestone>(`/api/v1/portfolio/milestones/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useDeleteMilestone() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/portfolio/milestones/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}
