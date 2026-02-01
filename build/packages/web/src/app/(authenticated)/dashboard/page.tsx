"use client";

import { useAuthStore } from "@/stores/auth-store";
import { useDashboard } from "@/hooks/useDashboard";
import { formatDistanceToNow } from "date-fns";
import Link from "next/link";
import {
  AlertTriangle, TrendingUp, FolderKanban, LayoutGrid,
  ArrowUpRight, ArrowDownRight, Minus, AlertCircle, CheckCircle,
  Link as LinkIcon, Clock,
} from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import type { RiadaType, RiadaSeverity } from "@/types/api";

const typeIcons: Record<RiadaType, React.ReactNode> = {
  risk: <AlertTriangle className="h-4 w-4 text-red-500" />,
  issue: <AlertCircle className="h-4 w-4 text-orange-500" />,
  action: <CheckCircle className="h-4 w-4 text-blue-500" />,
  dependency: <LinkIcon className="h-4 w-4 text-purple-500" />,
  assumption: <Clock className="h-4 w-4 text-green-500" />,
};

function StatCard({
  label,
  value,
  change,
  icon: Icon,
  color,
  isLoading,
}: {
  label: string;
  value: number | string;
  change: number;
  icon: React.ElementType;
  color: string;
  isLoading: boolean;
}) {
  const trend = change > 0 ? "up" : change < 0 ? "down" : "flat";

  if (isLoading) {
    return (
      <div className="bg-white dark:bg-[rgb(var(--color-surface))] rounded-xl border border-[rgb(var(--color-border))] p-5">
        <div className="flex items-center justify-between mb-3">
          <Skeleton className="h-9 w-9 rounded-lg" />
          <Skeleton className="h-4 w-12" />
        </div>
        <Skeleton className="h-8 w-16 mb-1" />
        <Skeleton className="h-4 w-24" />
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-[rgb(var(--color-surface))] rounded-xl border border-[rgb(var(--color-border))] p-5 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon size={20} />
        </div>
        <div className="flex items-center gap-1 text-caption">
          {trend === "up" && (
            <ArrowUpRight size={14} className="text-green-500" />
          )}
          {trend === "down" && (
            <ArrowDownRight size={14} className="text-red-500" />
          )}
          {trend === "flat" && (
            <Minus size={14} className="text-gray-400" />
          )}
          <span
            className={
              trend === "up"
                ? "text-green-600"
                : trend === "down"
                ? "text-red-600"
                : "text-gray-500"
            }
          >
            {change > 0 ? `+${change}` : change === 0 ? "—" : change}
          </span>
        </div>
      </div>
      <p className="text-2xl font-bold text-[rgb(var(--color-text))]">
        {value}
      </p>
      <p className="text-caption text-[rgb(var(--color-text-secondary))] mt-1">
        {label}
      </p>
    </div>
  );
}

function RecentRiadaItem({
  code,
  title,
  severity,
  riada_type,
  created_at,
}: {
  code: string;
  title: string;
  severity: RiadaSeverity;
  riada_type: RiadaType;
  created_at: string;
}) {
  const severityBadge = {
    critical: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
    high: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400",
    medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
    low: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
  };

  return (
    <Link
      href={`/riada?search=${code}`}
      className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
    >
      <div className="flex-shrink-0">
        {typeIcons[riada_type]}
      </div>
      <span className={`px-2 py-0.5 rounded text-xs font-medium capitalize ${severityBadge[severity]}`}>
        {severity}
      </span>
      <div className="flex-1 min-w-0">
        <p className="text-body-sm font-medium truncate">
          <span className="text-[rgb(var(--color-text-secondary))]">{code}:</span>{" "}
          {title}
        </p>
      </div>
      <span className="text-caption text-[rgb(var(--color-text-secondary))] shrink-0">
        {formatDistanceToNow(new Date(created_at), { addSuffix: true })}
      </span>
    </Link>
  );
}

function RecentRiadaSkeleton() {
  return (
    <div className="flex items-center gap-3 p-3">
      <Skeleton className="h-4 w-4" />
      <Skeleton className="h-5 w-16" />
      <Skeleton className="h-4 flex-1" />
      <Skeleton className="h-4 w-16" />
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { stats, recentRiada, isLoading } = useDashboard();

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      {/* Greeting */}
      <div className="mb-8">
        <h1 className="text-h1">
          Good {new Date().getHours() < 12 ? "morning" : "afternoon"},{" "}
          {user?.display_name?.split(" ")[0] || "there"}
        </h1>
        <p className="text-body text-[rgb(var(--color-text-secondary))] mt-1">
          Here&apos;s what&apos;s happening across {user?.organization_name}
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Active Processes"
          value={stats?.activeProcesses ?? 0}
          change={stats?.processChange ?? 0}
          icon={LayoutGrid}
          color="text-blue-600 bg-blue-50"
          isLoading={isLoading}
        />
        <StatCard
          label="Open RIADA Items"
          value={stats?.openRiadaItems ?? 0}
          change={stats?.riadaChange ?? 0}
          icon={AlertTriangle}
          color="text-amber-600 bg-amber-50"
          isLoading={isLoading}
        />
        <StatCard
          label="Active Projects"
          value={stats?.activeProjects ?? 0}
          change={stats?.projectChange ?? 0}
          icon={FolderKanban}
          color="text-purple-600 bg-purple-50"
          isLoading={isLoading}
        />
        <StatCard
          label="Adoption Score"
          value="—"
          change={0}
          icon={TrendingUp}
          color="text-green-600 bg-green-50"
          isLoading={isLoading}
        />
      </div>

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent RIADA */}
        <div className="lg:col-span-2 bg-white dark:bg-[rgb(var(--color-surface))] rounded-xl border border-[rgb(var(--color-border))] p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-h3">Recent Quality Items</h2>
            <Link
              href="/riada"
              className="text-body-sm text-brand-600 hover:text-brand-700 font-medium"
            >
              View all →
            </Link>
          </div>

          <div className="space-y-1">
            {isLoading ? (
              <>
                <RecentRiadaSkeleton />
                <RecentRiadaSkeleton />
                <RecentRiadaSkeleton />
                <RecentRiadaSkeleton />
              </>
            ) : recentRiada && recentRiada.length > 0 ? (
              recentRiada.map((item) => (
                <RecentRiadaItem
                  key={item.id}
                  code={item.code}
                  title={item.title}
                  severity={item.severity}
                  riada_type={item.riada_type}
                  created_at={item.created_at}
                />
              ))
            ) : (
              <div className="py-8 text-center text-muted-foreground">
                <AlertTriangle className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>No open quality items</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white dark:bg-[rgb(var(--color-surface))] rounded-xl border border-[rgb(var(--color-border))] p-5">
          <h2 className="text-h3 mb-4">Quick Actions</h2>
          <div className="space-y-2">
            {[
              { label: "Log an Issue", href: "/riada/new", emoji: "⚠️" },
              { label: "View Process Canvas", href: "/processes/canvas", emoji: "📊" },
              { label: "View Portfolio", href: "/portfolio", emoji: "📁" },
              { label: "Business Model Canvas", href: "/business-model", emoji: "🎯" },
              { label: "View Reports", href: "/reports", emoji: "📄" },
            ].map((action) => (
              <Link
                key={action.href}
                href={action.href}
                className="flex items-center gap-3 p-3 rounded-lg border border-[rgb(var(--color-border))] hover:border-brand-300 hover:bg-brand-50/50 dark:hover:bg-brand-900/10 transition-colors"
              >
                <span className="text-lg">{action.emoji}</span>
                <span className="text-body-sm font-medium">{action.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
