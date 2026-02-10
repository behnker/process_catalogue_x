"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import { PORTFOLIO_QUERY_KEY } from "@/hooks/usePortfolioItems";
import type { PortfolioMilestone } from "@/types/api";

export function useCreateMilestone() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { portfolio_item_id: string; name: string; description?: string; due_date?: string }) =>
      api.post<PortfolioMilestone>(
        `/api/v1/portfolio/${data.portfolio_item_id}/milestones`,
        data
      ),
    onSuccess: (_, { portfolio_item_id }) => {
      queryClient.invalidateQueries({ queryKey: [PORTFOLIO_QUERY_KEY, portfolio_item_id] });
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
      data: Partial<{ name: string; description: string; due_date: string; status: string; completed_date: string }>;
    }) => api.patch<PortfolioMilestone>(`/api/v1/portfolio/milestones/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [PORTFOLIO_QUERY_KEY] });
    },
  });
}

export function useDeleteMilestone() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/portfolio/milestones/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [PORTFOLIO_QUERY_KEY] });
    },
  });
}
