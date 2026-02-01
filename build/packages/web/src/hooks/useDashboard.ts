"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  Process,
  RiadaItem,
  PortfolioItem,
} from "@/types/api";

export interface DashboardStats {
  activeProcesses: number;
  openRiadaItems: number;
  activeProjects: number;
  processChange: number;
  riadaChange: number;
  projectChange: number;
}

export interface RecentRiadaItem {
  id: string;
  code: string;
  title: string;
  severity: "critical" | "high" | "medium" | "low";
  riada_type: "risk" | "issue" | "action" | "dependency" | "assumption";
  created_at: string;
}

// Fetch dashboard statistics by aggregating data from various endpoints
export function useDashboardStats() {
  return useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: async (): Promise<DashboardStats> => {
      // Fetch all counts in parallel
      const [processesRes, riadaRes, portfolioRes] = await Promise.all([
        api.get<PaginatedResponse<Process>>("/api/v1/processes?status=active&per_page=1"),
        api.get<PaginatedResponse<RiadaItem>>("/api/v1/riada?status=open&per_page=1"),
        api.get<PaginatedResponse<PortfolioItem>>("/api/v1/portfolio?status=in_progress&per_page=1"),
      ]);

      return {
        activeProcesses: processesRes.total || 0,
        openRiadaItems: riadaRes.total || 0,
        activeProjects: portfolioRes.total || 0,
        // Trend changes would require a comparison endpoint or historical data
        // For now, we'll show neutral since we don't have historical comparison
        processChange: 0,
        riadaChange: 0,
        projectChange: 0,
      };
    },
    staleTime: 30000, // Cache for 30 seconds
  });
}

// Fetch recent RIADA items for the dashboard
export function useRecentRiada(limit: number = 5) {
  return useQuery({
    queryKey: ["dashboard", "recent-riada", limit],
    queryFn: async () => {
      const response = await api.get<PaginatedResponse<RiadaItem>>(
        `/api/v1/riada?per_page=${limit}&status=open`
      );
      return response.items || [];
    },
    staleTime: 30000,
  });
}

// Fetch recent portfolio activity
export function useRecentPortfolioActivity(limit: number = 5) {
  return useQuery({
    queryKey: ["dashboard", "recent-portfolio", limit],
    queryFn: async () => {
      const response = await api.get<PaginatedResponse<PortfolioItem>>(
        `/api/v1/portfolio?per_page=${limit}`
      );
      return response.items || [];
    },
    staleTime: 30000,
  });
}

// Combined hook for all dashboard data
export function useDashboard() {
  const stats = useDashboardStats();
  const recentRiada = useRecentRiada(5);

  return {
    stats: stats.data,
    recentRiada: recentRiada.data,
    isLoading: stats.isLoading || recentRiada.isLoading,
    isError: stats.isError || recentRiada.isError,
  };
}
