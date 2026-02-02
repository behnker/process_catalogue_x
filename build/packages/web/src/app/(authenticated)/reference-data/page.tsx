"use client";

import * as React from "react";
import {
  Plus,
  Edit,
  Trash2,
  Building2,
  Users,
  Layers,
  Server,
  Tag,
  Briefcase,
  Globe,
  Package,
  Handshake,
  Truck,
  Loader2,
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
import {
  useReferenceData,
  useCreateReferenceItem,
  useUpdateReferenceItem,
  useDeleteReferenceItem,
  type CatalogueType,
  type ReferenceItem,
} from "@/hooks/useReferenceData";

interface CategoryConfig {
  key: CatalogueType;
  name: string;
  singular: string;
  description: string;
  icon: React.ReactNode;
}

const categories: CategoryConfig[] = [
  {
    key: "departments",
    name: "Departments",
    singular: "Department",
    description: "Organizational departments and business units",
    icon: <Building2 className="h-5 w-5" />,
  },
  {
    key: "functions",
    name: "Functions",
    singular: "Function",
    description: "Business functions within the operating model",
    icon: <Layers className="h-5 w-5" />,
  },
  {
    key: "roles",
    name: "Roles",
    singular: "Role",
    description: "Standard roles for RACI and ownership assignment",
    icon: <Users className="h-5 w-5" />,
  },
  {
    key: "systems",
    name: "Systems",
    singular: "System",
    description: "IT systems and applications in the technology landscape",
    icon: <Server className="h-5 w-5" />,
  },
  {
    key: "clients",
    name: "Clients",
    singular: "Client",
    description: "Client organizations and accounts",
    icon: <Briefcase className="h-5 w-5" />,
  },
  {
    key: "markets",
    name: "Markets",
    singular: "Market",
    description: "Geographic markets and regions",
    icon: <Globe className="h-5 w-5" />,
  },
  {
    key: "categories",
    name: "Categories",
    singular: "Category",
    description: "Product or service categories",
    icon: <Package className="h-5 w-5" />,
  },
  {
    key: "partners",
    name: "Partners",
    singular: "Partner",
    description: "Business partners and collaborators",
    icon: <Handshake className="h-5 w-5" />,
  },
  {
    key: "suppliers",
    name: "Suppliers",
    singular: "Supplier",
    description: "Vendors and suppliers",
    icon: <Truck className="h-5 w-5" />,
  },
  {
    key: "tags",
    name: "Tags",
    singular: "Tag",
    description: "Custom tags for categorizing and filtering entities",
    icon: <Tag className="h-5 w-5" />,
  },
];

export default function ReferenceDataPage() {
  const [activeTab, setActiveTab] = React.useState<CatalogueType>("departments");
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);
  const [editItem, setEditItem] = React.useState<ReferenceItem | null>(null);
  const [deleteConfirm, setDeleteConfirm] = React.useState<ReferenceItem | null>(null);
  const [formData, setFormData] = React.useState({ code: "", name: "", description: "" });

  const { data, isLoading } = useReferenceData({ status: "active" });
  const createMutation = useCreateReferenceItem();
  const updateMutation = useUpdateReferenceItem();
  const deleteMutation = useDeleteReferenceItem();

  const activeCategory = categories.find((c) => c.key === activeTab);

  // Filter items by active tab
  const activeItems = React.useMemo(() => {
    if (!data?.items) return [];
    return data.items.filter((item) => item.catalogue_type === activeTab);
  }, [data?.items, activeTab]);

  // Count items by category
  const categoryCounts = React.useMemo(() => {
    const counts: Record<string, number> = {};
    categories.forEach((c) => {
      counts[c.key] = data?.items?.filter((item) => item.catalogue_type === c.key).length || 0;
    });
    return counts;
  }, [data?.items]);

  const handleCreate = async () => {
    try {
      await createMutation.mutateAsync({
        catalogue_type: activeTab,
        code: formData.code,
        name: formData.name,
        description: formData.description || undefined,
      });
      setIsCreateOpen(false);
      setFormData({ code: "", name: "", description: "" });
    } catch (error) {
      // Error is handled by the mutation
    }
  };

  const handleEdit = (item: ReferenceItem) => {
    setEditItem(item);
    setFormData({ code: item.code, name: item.name, description: item.description || "" });
  };

  const handleUpdate = async () => {
    if (!editItem) return;
    try {
      await updateMutation.mutateAsync({
        id: editItem.id,
        data: {
          code: formData.code,
          name: formData.name,
          description: formData.description || undefined,
        },
      });
      setEditItem(null);
      setFormData({ code: "", name: "", description: "" });
    } catch (error) {
      // Error is handled by the mutation
    }
  };

  const handleDelete = async () => {
    if (!deleteConfirm) return;
    try {
      await deleteMutation.mutateAsync(deleteConfirm.id);
      setDeleteConfirm(null);
    } catch (error) {
      // Error is handled by the mutation
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Reference Data</h1>
          <p className="text-muted-foreground mt-1">
            Manage departments, functions, roles, systems, and more
          </p>
        </div>
      </div>

      {/* Category Cards Overview */}
      <div className="grid grid-cols-5 gap-4">
        {categories.slice(0, 5).map((category) => (
          <Card
            key={category.key}
            className={`cursor-pointer transition-colors hover:border-primary ${
              activeTab === category.key ? "border-primary bg-primary/5" : ""
            }`}
            onClick={() => setActiveTab(category.key)}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2">
                {category.icon}
                <CardTitle className="text-sm">{category.name}</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{categoryCounts[category.key]}</p>
              <p className="text-xs text-muted-foreground">items</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-5 gap-4">
        {categories.slice(5).map((category) => (
          <Card
            key={category.key}
            className={`cursor-pointer transition-colors hover:border-primary ${
              activeTab === category.key ? "border-primary bg-primary/5" : ""
            }`}
            onClick={() => setActiveTab(category.key)}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center gap-2">
                {category.icon}
                <CardTitle className="text-sm">{category.name}</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{categoryCounts[category.key]}</p>
              <p className="text-xs text-muted-foreground">items</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Active Category Detail */}
      {activeCategory && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {activeCategory.icon}
                <div>
                  <CardTitle>{activeCategory.name}</CardTitle>
                  <CardDescription>{activeCategory.description}</CardDescription>
                </div>
              </div>
              <Button onClick={() => setIsCreateOpen(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add {activeCategory.singular}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
            ) : (
              <div className="space-y-2">
                {activeItems.map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-muted/50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <Badge variant="outline" className="font-mono">
                        {item.code}
                      </Badge>
                      <span className="font-medium">{item.name}</span>
                      {item.description && (
                        <span className="text-sm text-muted-foreground">— {item.description}</span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={item.status === "active" ? "success" : "secondary"}>
                        {item.status === "active" ? "Active" : "Inactive"}
                      </Badge>
                      <Button variant="ghost" size="sm" onClick={() => handleEdit(item)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setDeleteConfirm(item)}
                        className="text-destructive hover:text-destructive"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
                {activeItems.length === 0 && (
                  <div className="text-center py-8 text-muted-foreground">
                    No items yet. Click &quot;Add&quot; to create one.
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Create Dialog */}
      <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add {activeCategory?.singular}</DialogTitle>
            <DialogDescription>
              Create a new {activeCategory?.name.toLowerCase()} entry.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="code">Code</Label>
              <Input
                id="code"
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                placeholder="UNIQUE_CODE"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="Display Name"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="description">Description (Optional)</Label>
              <Input
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Brief description..."
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsCreateOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleCreate}
              disabled={!formData.code || !formData.name || createMutation.isPending}
            >
              {createMutation.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                "Create"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={!!editItem} onOpenChange={(open) => !open && setEditItem(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit {activeCategory?.singular}</DialogTitle>
            <DialogDescription>Update the {activeCategory?.name.toLowerCase()} details.</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="edit-code">Code</Label>
              <Input
                id="edit-code"
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="edit-name">Name</Label>
              <Input
                id="edit-name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="edit-description">Description (Optional)</Label>
              <Input
                id="edit-description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditItem(null)}>
              Cancel
            </Button>
            <Button
              onClick={handleUpdate}
              disabled={!formData.code || !formData.name || updateMutation.isPending}
            >
              {updateMutation.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                "Save Changes"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={!!deleteConfirm} onOpenChange={(open) => !open && setDeleteConfirm(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete {activeCategory?.singular}?</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete &quot;{deleteConfirm?.name}&quot;? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteConfirm(null)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Deleting...
                </>
              ) : (
                "Delete"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
