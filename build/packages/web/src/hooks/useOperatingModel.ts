"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  OperatingModelComponent,
  OperatingModelSummary,
  ProcessRaci,
  ProcessKpi,
  ProcessGovernance,
  ProcessPolicy,
  ProcessTiming,
  ProcessSipoc,
} from "@/types/api";

const QUERY_KEY = "operating-model";

export function useOperatingModel(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, processId],
    queryFn: () =>
      api.get<OperatingModelComponent[]>(
        `/api/v1/processes/${processId}/operating-model`
      ),
    enabled: !!processId,
  });
}

export function useOperatingModelSummary(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "summary", processId],
    queryFn: () =>
      api.get<OperatingModelSummary>(
        `/api/v1/processes/${processId}/operating-model/summary`
      ),
    enabled: !!processId,
  });
}

export function useProcessRaci(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "raci", processId],
    queryFn: () =>
      api.get<ProcessRaci[]>(
        `/api/v1/processes/${processId}/operating-model/raci`
      ),
    enabled: !!processId,
  });
}

export function useProcessKpis(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "kpis", processId],
    queryFn: () =>
      api.get<ProcessKpi[]>(
        `/api/v1/processes/${processId}/operating-model/kpis`
      ),
    enabled: !!processId,
  });
}

export function useProcessGovernance(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "governance", processId],
    queryFn: () =>
      api.get<ProcessGovernance[]>(
        `/api/v1/processes/${processId}/operating-model/governance`
      ),
    enabled: !!processId,
  });
}

export function useProcessPolicies(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "policies", processId],
    queryFn: () =>
      api.get<ProcessPolicy[]>(
        `/api/v1/processes/${processId}/operating-model/policies`
      ),
    enabled: !!processId,
  });
}

export function useProcessTiming(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "timing", processId],
    queryFn: () =>
      api.get<ProcessTiming[]>(
        `/api/v1/processes/${processId}/operating-model/timing`
      ),
    enabled: !!processId,
  });
}

export function useProcessSipoc(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "sipoc", processId],
    queryFn: () =>
      api.get<ProcessSipoc[]>(
        `/api/v1/processes/${processId}/operating-model/sipoc`
      ),
    enabled: !!processId,
  });
}
