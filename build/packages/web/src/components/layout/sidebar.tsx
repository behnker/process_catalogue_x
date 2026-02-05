"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Home, LayoutGrid, List, Target, AlertTriangle, FolderKanban,
  TrendingUp, FileText, Bot, FileBarChart, BookOpen, Settings,
  HelpCircle, ChevronLeft, ChevronRight, AlertCircle, Monitor,
} from "lucide-react";

interface NavItem {
  label: string;
  href: string;
  icon: React.ElementType;
  section?: string;
}

const navigation: NavItem[] = [
  { label: "Home", href: "/dashboard", icon: Home },
  // DESIGN
  { label: "Process Canvas", href: "/processes/canvas", icon: LayoutGrid, section: "DESIGN" },
  { label: "Process List", href: "/processes", icon: List },
  { label: "Business Model", href: "/business-model", icon: Target },
  // OPERATE
  { label: "Issue Log", href: "/issues", icon: AlertCircle, section: "OPERATE" },
  { label: "Quality Logs (RIADA)", href: "/riada", icon: AlertTriangle },
  { label: "Portfolio", href: "/portfolio", icon: FolderKanban },
  { label: "Systems", href: "/systems", icon: Monitor },
  { label: "Change & Adoption", href: "/surveys", icon: TrendingUp },
  { label: "Surveys", href: "/surveys", icon: FileText },
  // INTELLIGENCE
  { label: "Prompt Library", href: "/prompts", icon: Bot, section: "INTELLIGENCE" },
  { label: "Reports", href: "/reports", icon: FileBarChart },
  // MANAGE
  { label: "Reference Data", href: "/reference-data", icon: BookOpen, section: "MANAGE" },
  { label: "Settings", href: "/settings/general", icon: Settings },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 z-30 h-screen bg-surface-sidebar border-r border-[rgb(var(--color-border))] flex flex-col transition-all duration-200 ease-in-out",
        collapsed ? "w-[64px]" : "w-[256px]"
      )}
    >
      {/* Header */}
      <div className={cn(
        "flex items-center h-14 border-b border-[rgb(var(--color-border))] px-4",
        collapsed ? "justify-center" : "justify-between"
      )}>
        {!collapsed && (
          <span className="font-bold text-h4 text-[rgb(var(--color-text))] truncate">
            Process Catalogue
          </span>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-md hover:bg-[rgb(var(--color-border))] transition-colors"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-2 px-2">
        {navigation.map((item, idx) => {
          const isActive = pathname.startsWith(item.href);
          const showSection = item.section && !collapsed;
          const prevItem = navigation[idx - 1];
          const isNewSection = item.section && (!prevItem || prevItem.section !== item.section);

          return (
            <div key={item.href + item.label}>
              {isNewSection && showSection && (
                <div className="mt-4 mb-1 px-3">
                  <span className="text-[10px] font-bold tracking-wider text-[rgb(var(--color-text-secondary))] uppercase">
                    {item.section}
                  </span>
                </div>
              )}
              {isNewSection && collapsed && <div className="my-2 mx-2 border-t border-[rgb(var(--color-border))]" />}

              <Link
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-body-sm transition-colors group relative",
                  isActive
                    ? "bg-brand-500/10 text-brand-700 dark:text-brand-400 font-medium"
                    : "text-[rgb(var(--color-text-secondary))] hover:bg-[rgb(var(--color-border))]/50 hover:text-[rgb(var(--color-text))]",
                  collapsed && "justify-center px-2"
                )}
              >
                <item.icon
                  size={20}
                  className={cn(
                    "shrink-0",
                    isActive ? "text-brand-500" : "text-[rgb(var(--color-text-secondary))]"
                  )}
                />
                {!collapsed && <span className="truncate">{item.label}</span>}

                {/* Tooltip on collapsed */}
                {collapsed && (
                  <div className="absolute left-full ml-2 px-2 py-1 rounded bg-gray-900 text-white text-caption whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50">
                    {item.label}
                  </div>
                )}
              </Link>
            </div>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-[rgb(var(--color-border))] p-2">
        <Link
          href="/help"
          className={cn(
            "flex items-center gap-3 rounded-lg px-3 py-2 text-body-sm text-[rgb(var(--color-text-secondary))] hover:bg-[rgb(var(--color-border))]/50 transition-colors",
            collapsed && "justify-center px-2"
          )}
        >
          <HelpCircle size={20} />
          {!collapsed && <span>Help</span>}
        </Link>
      </div>
    </aside>
  );
}
