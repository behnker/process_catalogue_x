"use client";

import * as React from "react";
import { X, FileText, Users, TrendingUp, Shield, Plus, ChevronRight, Trash2, Edit } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { Process } from "@/types/api";

interface ProcessDetailModalProps {
  process: Process | null;
  open: boolean;
  onClose: () => void;
  onEdit?: (process: Process) => void;
  onDelete?: (process: Process) => void;
  onAddChild?: (level: string, parentId: string) => void;
  onSelectProcess?: (process: Process) => void;
}

type TabId = "overview" | "raci" | "kpis" | "policies";

const tabs: { id: TabId; label: string; icon: React.ReactNode }[] = [
  { id: "overview", label: "Overview", icon: <FileText className="h-4 w-4" /> },
  { id: "raci", label: "RACI", icon: <Users className="h-4 w-4" /> },
  { id: "kpis", label: "KPIs", icon: <TrendingUp className="h-4 w-4" /> },
  { id: "policies", label: "Policies & Standards", icon: <Shield className="h-4 w-4" /> },
];

function getNextLevel(currentLevel: string): string | null {
  const levelNum = parseInt(currentLevel.replace("L", ""), 10);
  if (levelNum >= 5) return null;
  return `L${levelNum + 1}`;
}

function getLevelNumber(level: string): string {
  return level.replace("L", "");
}

export function ProcessDetailModal({
  process,
  open,
  onClose,
  onEdit,
  onDelete,
  onAddChild,
  onSelectProcess,
}: ProcessDetailModalProps) {
  const [activeTab, setActiveTab] = React.useState<TabId>("overview");

  // Reset tab when process changes
  React.useEffect(() => {
    setActiveTab("overview");
  }, [process?.id]);

  if (!open || !process) return null;

  const nextLevel = getNextLevel(process.level);
  const children = process.children || [];
  const hasChildren = children.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[85vh] overflow-hidden flex flex-col mx-4">
        {/* Header */}
        <div className="p-6 pb-0">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Badge className="bg-blue-500 text-white text-xs">
                  {process.status === "active" ? "Active" : process.status === "draft" ? "Draft" : "N/A"}
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  LEVEL {getLevelNumber(process.level)}
                </Badge>
              </div>
              <h2 className="text-xl font-bold text-slate-900">{process.name}</h2>
              {process.code && (
                <p className="text-sm text-slate-500 mt-1">Code: {process.code}</p>
              )}
            </div>
            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Tabs */}
          <div className="flex gap-6 mt-6 border-b border-slate-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  "flex items-center gap-2 pb-3 text-sm font-medium transition-colors",
                  activeTab === tab.id
                    ? "text-blue-600 border-b-2 border-blue-600"
                    : "text-slate-500 hover:text-slate-700"
                )}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {activeTab === "overview" && (
            <div className="space-y-6">
              {/* Description */}
              <div>
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  <FileText className="h-4 w-4" />
                  Description
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <p className="text-slate-700">
                    {process.description || "No description provided."}
                  </p>
                </div>
              </div>

              {/* Process Owner */}
              <div>
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  <Users className="h-4 w-4" />
                  Process Owner
                </div>
                <div className="bg-slate-50 rounded-lg p-4 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-semibold">
                    {process.owner_id ? "O" : "?"}
                  </div>
                  <span className="text-slate-700">
                    {process.owner_id || "Not assigned"}
                  </span>
                </div>
              </div>

              {/* Automation */}
              <div>
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-500 uppercase tracking-wide mb-3">
                  <TrendingUp className="h-4 w-4" />
                  Automation
                </div>
                <div className="bg-slate-50 rounded-lg p-4 grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Current</p>
                    <p className="text-slate-700 capitalize">{process.current_automation?.replace("_", " ") || "Manual"}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Target</p>
                    <p className="text-slate-700 capitalize">{process.target_automation?.replace("_", " ") || "Not set"}</p>
                  </div>
                </div>
              </div>

              {/* Sub-processes (Children) */}
              {(hasChildren || nextLevel) && (
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2 text-sm font-semibold text-slate-500 uppercase tracking-wide">
                      <ChevronRight className="h-4 w-4" />
                      Sub-processes
                    </div>
                    {nextLevel && onAddChild && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onAddChild(nextLevel, process.id)}
                      >
                        <Plus className="h-4 w-4 mr-1" />
                        Add {nextLevel}
                      </Button>
                    )}
                  </div>

                  {hasChildren ? (
                    <div className="space-y-2">
                      {children.map((child) => (
                        <div
                          key={child.id}
                          className="bg-slate-50 rounded-lg p-3 flex items-center justify-between hover:bg-slate-100 cursor-pointer transition-colors"
                          onClick={() => onSelectProcess?.(child)}
                        >
                          <div>
                            <div className="flex items-center gap-2">
                              <Badge variant="secondary" className="text-xs">
                                L{getLevelNumber(child.level)}
                              </Badge>
                              <span className="font-medium text-slate-800">{child.name}</span>
                            </div>
                            {child.description && (
                              <p className="text-sm text-slate-500 mt-1 line-clamp-1">{child.description}</p>
                            )}
                          </div>
                          <ChevronRight className="h-4 w-4 text-slate-400" />
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="bg-slate-50 rounded-lg p-4 text-center text-slate-500">
                      No sub-processes yet
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === "raci" && (
            <div className="text-center text-slate-500 py-12">
              <Users className="h-12 w-12 mx-auto mb-4 text-slate-300" />
              <p>RACI matrix will be displayed here.</p>
              <p className="text-sm mt-2">Define Responsible, Accountable, Consulted, and Informed roles.</p>
            </div>
          )}

          {activeTab === "kpis" && (
            <div className="text-center text-slate-500 py-12">
              <TrendingUp className="h-12 w-12 mx-auto mb-4 text-slate-300" />
              <p>KPIs and metrics will be displayed here.</p>
              <p className="text-sm mt-2">Track process performance indicators.</p>
            </div>
          )}

          {activeTab === "policies" && (
            <div className="text-center text-slate-500 py-12">
              <Shield className="h-12 w-12 mx-auto mb-4 text-slate-300" />
              <p>Policies & Standards will be displayed here.</p>
              <p className="text-sm mt-2">Link governance documents and compliance requirements.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="text-xs text-slate-400">
            {process.created_at && `Created: ${new Date(process.created_at).toLocaleDateString()}`}
          </div>
          <div className="flex items-center gap-2">
            {onDelete && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDelete(process)}
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                <Trash2 className="h-4 w-4 mr-1" />
                Delete
              </Button>
            )}
            {onEdit && (
              <Button size="sm" onClick={() => onEdit(process)}>
                <Edit className="h-4 w-4 mr-1" />
                Edit
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
