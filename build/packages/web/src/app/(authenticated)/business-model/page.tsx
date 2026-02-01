"use client";

import * as React from "react";
import { Plus, List, Grid3X3 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useBusinessModels, useBusinessModelWithEntries, useCreateBusinessModelEntry } from "@/hooks/useBusinessModel";
import type { BusinessModelEntry, BMCComponent } from "@/types/api";
import { cn } from "@/lib/utils";

const BMC_COMPONENTS: { id: BMCComponent; label: string; description: string }[] = [
  { id: "key_partners", label: "Key Partners", description: "Who are your key partners and suppliers?" },
  { id: "key_activities", label: "Key Activities", description: "What key activities do your value propositions require?" },
  { id: "key_resources", label: "Key Resources", description: "What key resources do your value propositions require?" },
  { id: "value_propositions", label: "Value Propositions", description: "What value do you deliver to the customer?" },
  { id: "customer_relationships", label: "Customer Relationships", description: "What type of relationship does each customer segment expect?" },
  { id: "channels", label: "Channels", description: "Through which channels do your customer segments want to be reached?" },
  { id: "customer_segments", label: "Customer Segments", description: "For whom are you creating value?" },
  { id: "cost_structure", label: "Cost Structure", description: "What are the most important costs inherent in your business model?" },
  { id: "revenue_streams", label: "Revenue Streams", description: "For what value are your customers willing to pay?" },
];

// BMC Grid layout positions
const gridPositions: Record<BMCComponent, string> = {
  key_partners: "col-start-1 row-start-1 row-span-2",
  key_activities: "col-start-2 row-start-1",
  key_resources: "col-start-2 row-start-2",
  value_propositions: "col-start-3 row-start-1 row-span-2",
  customer_relationships: "col-start-4 row-start-1",
  channels: "col-start-4 row-start-2",
  customer_segments: "col-start-5 row-start-1 row-span-2",
  cost_structure: "col-start-1 col-span-2 row-start-3",
  revenue_streams: "col-start-4 col-span-2 row-start-3",
};

interface BMCBoxProps {
  component: BMCComponent;
  label: string;
  description: string;
  entries: BusinessModelEntry[];
  onAddEntry: () => void;
}

function BMCBox({ component, label, description, entries, onAddEntry }: BMCBoxProps) {
  return (
    <Card className={cn("flex flex-col h-full", gridPositions[component])}>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold flex items-center justify-between">
          {label}
          <Badge variant="secondary" className="text-xs">
            {entries.length}
          </Badge>
        </CardTitle>
        <p className="text-xs text-muted-foreground">{description}</p>
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto space-y-2 pt-0">
        {entries.map((entry) => (
          <div
            key={entry.id}
            className="text-sm p-2 bg-muted rounded-md cursor-pointer hover:bg-muted/80"
          >
            <p className="font-medium">{entry.title}</p>
            {entry.agentic_readiness && (
              <Badge
                variant={
                  entry.agentic_readiness === "high"
                    ? "success"
                    : entry.agentic_readiness === "medium"
                    ? "warning"
                    : "secondary"
                }
                className="text-xs mt-1"
              >
                AI: {entry.agentic_readiness}
              </Badge>
            )}
          </div>
        ))}
        <Button
          variant="ghost"
          size="sm"
          className="w-full border-2 border-dashed text-muted-foreground"
          onClick={onAddEntry}
        >
          <Plus className="h-4 w-4 mr-1" />
          Add
        </Button>
      </CardContent>
    </Card>
  );
}

export default function BusinessModelPage() {
  const [view, setView] = React.useState<"grid" | "list">("grid");
  const { data: businessModels } = useBusinessModels();
  const activeModelId = businessModels?.items?.[0]?.id;
  const { data: activeModel } = useBusinessModelWithEntries(activeModelId);
  const createEntry = useCreateBusinessModelEntry();

  const [addDialogOpen, setAddDialogOpen] = React.useState(false);
  const [addComponent, setAddComponent] = React.useState<BMCComponent | null>(null);
  const [newEntryTitle, setNewEntryTitle] = React.useState("");

  const entriesByComponent = React.useMemo(() => {
    const map: Record<BMCComponent, BusinessModelEntry[]> = {
      key_partners: [],
      key_activities: [],
      key_resources: [],
      value_propositions: [],
      customer_relationships: [],
      channels: [],
      customer_segments: [],
      cost_structure: [],
      revenue_streams: [],
    };
    activeModel?.entries?.forEach((entry) => {
      if (map[entry.component]) {
        map[entry.component].push(entry);
      }
    });
    return map;
  }, [activeModel]);

  const handleAddEntry = (component: BMCComponent) => {
    setAddComponent(component);
    setNewEntryTitle("");
    setAddDialogOpen(true);
  };

  const handleCreateEntry = async () => {
    if (!addComponent || !newEntryTitle.trim() || !activeModelId) return;
    await createEntry.mutateAsync({
      business_model_id: activeModelId,
      component: addComponent,
      title: newEntryTitle.trim(),
    });
    setAddDialogOpen(false);
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Business Model Canvas</h1>
          <p className="text-muted-foreground mt-1">
            {activeModel?.name || "Loading..."}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Tabs value={view} onValueChange={(v) => setView(v as "grid" | "list")}>
            <TabsList>
              <TabsTrigger value="grid">
                <Grid3X3 className="h-4 w-4" />
              </TabsTrigger>
              <TabsTrigger value="list">
                <List className="h-4 w-4" />
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </div>

      {view === "grid" ? (
        /* Grid View - 9 Box Canvas */
        <div className="grid grid-cols-5 grid-rows-3 gap-4 min-h-[600px]">
          {BMC_COMPONENTS.map((comp) => (
            <BMCBox
              key={comp.id}
              component={comp.id}
              label={comp.label}
              description={comp.description}
              entries={entriesByComponent[comp.id]}
              onAddEntry={() => handleAddEntry(comp.id)}
            />
          ))}
        </div>
      ) : (
        /* List View */
        <div className="space-y-4">
          {BMC_COMPONENTS.map((comp) => (
            <Card key={comp.id}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base flex items-center justify-between">
                  {comp.label}
                  <Badge variant="secondary">{entriesByComponent[comp.id].length}</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {entriesByComponent[comp.id].length === 0 ? (
                  <p className="text-sm text-muted-foreground">No entries yet</p>
                ) : (
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                    {entriesByComponent[comp.id].map((entry) => (
                      <div
                        key={entry.id}
                        className="text-sm p-3 bg-muted rounded-md cursor-pointer hover:bg-muted/80"
                      >
                        <p className="font-medium">{entry.title}</p>
                        {entry.description && (
                          <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                            {entry.description}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
                <Button
                  variant="outline"
                  size="sm"
                  className="mt-2"
                  onClick={() => handleAddEntry(comp.id)}
                >
                  <Plus className="h-4 w-4 mr-1" />
                  Add Entry
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Add Entry Dialog */}
      <Dialog open={addDialogOpen} onOpenChange={setAddDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              Add to {BMC_COMPONENTS.find((c) => c.id === addComponent)?.label}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={newEntryTitle}
                onChange={(e) => setNewEntryTitle(e.target.value)}
                placeholder="Enter entry title"
              />
            </div>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => setAddDialogOpen(false)}>
                Cancel
              </Button>
              <Button
                onClick={handleCreateEntry}
                disabled={!newEntryTitle.trim() || createEntry.isPending}
              >
                {createEntry.isPending ? "Adding..." : "Add Entry"}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
