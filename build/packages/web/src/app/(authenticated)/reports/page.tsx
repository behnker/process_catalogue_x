"use client";

import * as React from "react";
import {
  FileText,
  Download,
  BarChart3,
  PieChart,
  TrendingUp,
  Calendar,
  Filter,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";

interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  category: "process" | "riada" | "portfolio" | "adoption";
  icon: React.ReactNode;
  lastGenerated?: string;
}

const reportTemplates: ReportTemplate[] = [
  {
    id: "process-catalogue",
    name: "Process Catalogue Report",
    description: "Complete overview of all processes with hierarchy, owners, and automation status",
    category: "process",
    icon: <FileText className="h-5 w-5" />,
  },
  {
    id: "riada-summary",
    name: "RIADA Summary Report",
    description: "Consolidated view of all risks, issues, actions, dependencies, and assumptions",
    category: "riada",
    icon: <BarChart3 className="h-5 w-5" />,
  },
  {
    id: "risk-register",
    name: "Risk Register",
    description: "Detailed risk register with probability, impact, and mitigation plans",
    category: "riada",
    icon: <PieChart className="h-5 w-5" />,
  },
  {
    id: "portfolio-status",
    name: "Portfolio Status Report",
    description: "Programme and project status with RAG, milestones, and budget tracking",
    category: "portfolio",
    icon: <TrendingUp className="h-5 w-5" />,
  },
  {
    id: "wsvf-prioritization",
    name: "WSVF Prioritization Report",
    description: "Weighted Shortest Job First scoring and prioritization analysis",
    category: "portfolio",
    icon: <BarChart3 className="h-5 w-5" />,
  },
  {
    id: "adoption-metrics",
    name: "Adoption Metrics Report",
    description: "Process adoption rates and change management effectiveness",
    category: "adoption",
    icon: <TrendingUp className="h-5 w-5" />,
  },
];

const categoryColors: Record<string, string> = {
  process: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
  riada: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  portfolio: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300",
  adoption: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
};

export default function ReportsPage() {
  const [categoryFilter, setCategoryFilter] = React.useState<string>("all");
  const [isGenerating, setIsGenerating] = React.useState<string | null>(null);

  const filteredReports = reportTemplates.filter(
    (report) => categoryFilter === "all" || report.category === categoryFilter
  );

  const handleGenerate = async (reportId: string) => {
    setIsGenerating(reportId);
    // Simulate report generation
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setIsGenerating(null);
    // In production, this would trigger actual report generation via API
  };

  const handleExport = (reportId: string, format: "pdf" | "excel" | "csv") => {
    // In production, this would download the report in the specified format
    console.log(`Exporting ${reportId} as ${format}`);
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Reports</h1>
          <p className="text-muted-foreground mt-1">
            Generate and export reports for processes, RIADA, and portfolio
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <Select value={categoryFilter} onValueChange={setCategoryFilter}>
          <SelectTrigger className="w-[180px]">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Filter by category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="process">Process</SelectItem>
            <SelectItem value="riada">RIADA</SelectItem>
            <SelectItem value="portfolio">Portfolio</SelectItem>
            <SelectItem value="adoption">Adoption</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Report Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredReports.map((report) => (
          <Card key={report.id} className="flex flex-col">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="p-2 rounded-lg bg-muted">{report.icon}</div>
                <Badge className={categoryColors[report.category]}>{report.category}</Badge>
              </div>
              <CardTitle className="mt-4">{report.name}</CardTitle>
              <CardDescription>{report.description}</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col justify-end">
              {report.lastGenerated && (
                <p className="text-xs text-muted-foreground mb-4 flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  Last generated: {report.lastGenerated}
                </p>
              )}
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1"
                  onClick={() => handleGenerate(report.id)}
                  disabled={isGenerating === report.id}
                >
                  {isGenerating === report.id ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Generate
                    </>
                  )}
                </Button>
                <Select onValueChange={(format) => handleExport(report.id, format as "pdf" | "excel" | "csv")}>
                  <SelectTrigger className="w-[100px]">
                    <Download className="h-4 w-4 mr-2" />
                    Export
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pdf">PDF</SelectItem>
                    <SelectItem value="excel">Excel</SelectItem>
                    <SelectItem value="csv">CSV</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredReports.length === 0 && (
        <div className="text-center py-12">
          <FileText className="h-12 w-12 mx-auto text-muted-foreground" />
          <h3 className="mt-4 text-lg font-medium">No reports found</h3>
          <p className="text-muted-foreground">
            Try adjusting your filters to see available reports.
          </p>
        </div>
      )}

      {/* Coming Soon Section */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle className="text-lg">Custom Reports (Coming Soon)</CardTitle>
          <CardDescription>
            Build custom reports with drag-and-drop fields, filters, and visualizations.
            Schedule automated report generation and delivery.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" disabled>
            <FileText className="h-4 w-4 mr-2" />
            Create Custom Report
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
