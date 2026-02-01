"use client";

import { useState } from "react";
import { useAuthStore } from "@/stores/auth-store";
import { Search, Plus, Bell, ChevronDown, LogOut, User as UserIcon } from "lucide-react";

export function Header() {
  const { user, logout } = useAuthStore();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNewMenu, setShowNewMenu] = useState(false);

  return (
    <header className="fixed top-0 right-0 left-[256px] z-20 h-14 bg-white dark:bg-[rgb(var(--color-surface))] border-b border-[rgb(var(--color-border))] flex items-center px-4 gap-4">
      {/* Breadcrumbs / Page title (slot — filled by each page) */}
      <div className="flex-1" id="page-header-slot" />

      {/* Global Search (Cmd+K) */}
      <button
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-[rgb(var(--color-border))] text-body-sm text-[rgb(var(--color-text-secondary))] hover:border-brand-300 transition-colors w-64"
        onClick={() => {
          // TODO: Open command palette
        }}
      >
        <Search size={16} />
        <span className="flex-1 text-left">Search...</span>
        <kbd className="text-[10px] bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded font-mono">
          ⌘K
        </kbd>
      </button>

      {/* Quick Action (+ New) */}
      <div className="relative">
        <button
          onClick={() => setShowNewMenu(!showNewMenu)}
          className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-brand-500 hover:bg-brand-600 text-white text-body-sm font-medium transition-colors"
        >
          <Plus size={16} />
          New
        </button>

        {showNewMenu && (
          <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-[rgb(var(--color-surface))] rounded-lg shadow-lg border border-[rgb(var(--color-border))] py-1 z-50">
            {[
              { label: "📊 New Process", href: "/processes/new" },
              { label: "⚠️ New RIADA Item", href: "/riada/new" },
              { label: "📁 New Project", href: "/portfolio/new" },
              { label: "📝 New Survey", href: "/surveys/new" },
              { label: "🤖 Run Prompt", href: "/prompts" },
            ].map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="block px-3 py-2 text-body-sm hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                onClick={() => setShowNewMenu(false)}
              >
                {item.label}
              </a>
            ))}
          </div>
        )}
      </div>

      {/* Notifications */}
      <button className="relative p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
        <Bell size={20} className="text-[rgb(var(--color-text-secondary))]" />
        <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
      </button>

      {/* Version */}
      <span className="text-[10px] text-[rgb(var(--color-text-secondary))] font-mono">
        v{process.env.NEXT_PUBLIC_APP_VERSION || "0.1.0"}
      </span>

      {/* User Menu */}
      <div className="relative">
        <button
          onClick={() => setShowUserMenu(!showUserMenu)}
          className="flex items-center gap-2 p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <div className="w-8 h-8 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center text-body-sm font-bold">
            {user?.display_name?.[0] || user?.email?.[0]?.toUpperCase() || "?"}
          </div>
          <ChevronDown size={14} className="text-[rgb(var(--color-text-secondary))]" />
        </button>

        {showUserMenu && (
          <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-[rgb(var(--color-surface))] rounded-lg shadow-lg border border-[rgb(var(--color-border))] py-1 z-50">
            <div className="px-3 py-2 border-b border-[rgb(var(--color-border))]">
              <p className="text-body-sm font-medium truncate">{user?.display_name}</p>
              <p className="text-caption text-[rgb(var(--color-text-secondary))] truncate">
                {user?.email}
              </p>
              <p className="text-[10px] text-brand-600 font-medium mt-0.5">
                {user?.organization_name}
              </p>
            </div>
            <a
              href="/settings/general"
              className="flex items-center gap-2 px-3 py-2 text-body-sm hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              <UserIcon size={16} /> Profile & Settings
            </a>
            <button
              onClick={() => {
                logout();
                window.location.href = "/auth/login";
              }}
              className="flex items-center gap-2 px-3 py-2 text-body-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 w-full text-left transition-colors"
            >
              <LogOut size={16} /> Sign out
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
