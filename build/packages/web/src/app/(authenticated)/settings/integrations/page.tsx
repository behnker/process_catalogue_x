"use client";

import * as React from "react";
import {
  Link as LinkIcon,
  Check,
  X,
  Settings,
  RefreshCw,
  Zap,
  Database,
  Mail,
  Cloud,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface Integration {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  category: "llm" | "storage" | "communication";
  status: "connected" | "disconnected" | "error";
  lastSync?: string;
}

const integrations: Integration[] = [
  {
    id: "anthropic",
    name: "Anthropic Claude",
    description: "AI-powered analysis and recommendations",
    icon: <Zap className="h-6 w-6" />,
    category: "llm",
    status: "connected",
    lastSync: "2 minutes ago",
  },
  {
    id: "openai",
    name: "OpenAI",
    description: "Alternative LLM provider for prompts",
    icon: <Zap className="h-6 w-6" />,
    category: "llm",
    status: "disconnected",
  },
  {
    id: "supabase",
    name: "Supabase",
    description: "Database and authentication",
    icon: <Database className="h-6 w-6" />,
    category: "storage",
    status: "connected",
    lastSync: "Connected",
  },
  {
    id: "cloudflare-r2",
    name: "Cloudflare R2",
    description: "Document and file storage",
    icon: <Cloud className="h-6 w-6" />,
    category: "storage",
    status: "connected",
    lastSync: "Connected",
  },
  {
    id: "resend",
    name: "Resend",
    description: "Transactional email delivery",
    icon: <Mail className="h-6 w-6" />,
    category: "communication",
    status: "connected",
    lastSync: "5 minutes ago",
  },
  {
    id: "slack",
    name: "Slack",
    description: "Team notifications and alerts",
    icon: <Mail className="h-6 w-6" />,
    category: "communication",
    status: "disconnected",
  },
];

const categoryLabels: Record<string, string> = {
  llm: "AI & LLM",
  storage: "Storage",
  communication: "Communication",
};

const statusConfig = {
  connected: { variant: "success" as const, icon: <Check className="h-4 w-4" /> },
  disconnected: { variant: "secondary" as const, icon: <X className="h-4 w-4" /> },
  error: { variant: "danger" as const, icon: <X className="h-4 w-4" /> },
};

export default function SettingsIntegrationsPage() {
  const [configureId, setConfigureId] = React.useState<string | null>(null);
  const [apiKey, setApiKey] = React.useState("");
  const [isSaving, setIsSaving] = React.useState(false);

  const configureIntegration = integrations.find((i) => i.id === configureId);

  const handleConnect = async () => {
    setIsSaving(true);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsSaving(false);
    setConfigureId(null);
    setApiKey("");
  };

  const handleDisconnect = (id: string) => {
    console.log("Disconnecting:", id);
  };

  const handleTestConnection = (id: string) => {
    console.log("Testing connection:", id);
  };

  const groupedIntegrations = integrations.reduce((acc, integration) => {
    if (!acc[integration.category]) {
      acc[integration.category] = [];
    }
    acc[integration.category].push(integration);
    return acc;
  }, {} as Record<string, Integration[]>);

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-h1">Integrations</h1>
        <p className="text-muted-foreground mt-1">
          Connect external services and manage API configurations
        </p>
      </div>

      {Object.entries(groupedIntegrations).map(([category, categoryIntegrations]) => (
        <div key={category} className="space-y-4">
          <h2 className="text-lg font-semibold">{categoryLabels[category]}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {categoryIntegrations.map((integration) => (
              <Card key={integration.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-muted">{integration.icon}</div>
                      <div>
                        <CardTitle className="text-base">{integration.name}</CardTitle>
                        <CardDescription className="text-sm">
                          {integration.description}
                        </CardDescription>
                      </div>
                    </div>
                    <Badge variant={statusConfig[integration.status].variant}>
                      {statusConfig[integration.status].icon}
                      <span className="ml-1 capitalize">{integration.status}</span>
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  {integration.lastSync && (
                    <p className="text-xs text-muted-foreground mb-3">
                      Last sync: {integration.lastSync}
                    </p>
                  )}
                  <div className="flex gap-2">
                    {integration.status === "connected" ? (
                      <>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleTestConnection(integration.id)}
                        >
                          <RefreshCw className="h-4 w-4 mr-1" />
                          Test
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setConfigureId(integration.id)}
                        >
                          <Settings className="h-4 w-4 mr-1" />
                          Configure
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDisconnect(integration.id)}
                          className="text-destructive hover:text-destructive"
                        >
                          Disconnect
                        </Button>
                      </>
                    ) : (
                      <Button size="sm" onClick={() => setConfigureId(integration.id)}>
                        <LinkIcon className="h-4 w-4 mr-1" />
                        Connect
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      ))}

      <Dialog open={!!configureId} onOpenChange={(open) => !open && setConfigureId(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {configureIntegration?.status === "connected" ? "Configure" : "Connect"}{" "}
              {configureIntegration?.name}
            </DialogTitle>
            <DialogDescription>
              {configureIntegration?.status === "connected"
                ? "Update your API credentials and settings."
                : "Enter your API credentials to connect this integration."}
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="api-key">API Key</Label>
              <Input
                id="api-key"
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-..."
              />
              <p className="text-xs text-muted-foreground">
                Your API key is stored securely and never exposed.
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setConfigureId(null)}>
              Cancel
            </Button>
            <Button onClick={handleConnect} disabled={!apiKey || isSaving}>
              {isSaving
                ? "Saving..."
                : configureIntegration?.status === "connected"
                ? "Save Changes"
                : "Connect"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Webhooks</CardTitle>
          <CardDescription>
            Configure webhooks to receive real-time notifications about events.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" disabled>
            <Zap className="h-4 w-4 mr-2" />
            Configure Webhooks (Coming Soon)
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
