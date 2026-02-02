"use client";

import * as React from "react";
import { ColumnDef } from "@tanstack/react-table";
import { format } from "date-fns";
import {
  MoreHorizontal,
  UserPlus,
  Mail,
  Shield,
  Trash2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DataTable, DataTableColumnHeader } from "@/components/shared/DataTable";

interface User {
  id: string;
  email: string;
  display_name: string | null;
  role: "admin" | "editor" | "viewer";
  status: "active" | "pending" | "disabled";
  last_login?: string;
  created_at: string;
}

const mockUsers: User[] = [
  {
    id: "1",
    email: "admin@surity.com",
    display_name: "Admin User",
    role: "admin",
    status: "active",
    last_login: "2026-02-01T10:30:00Z",
    created_at: "2026-01-01T00:00:00Z",
  },
  {
    id: "2",
    email: "john@surity.com",
    display_name: "John Smith",
    role: "editor",
    status: "active",
    last_login: "2026-01-31T14:20:00Z",
    created_at: "2026-01-15T00:00:00Z",
  },
  {
    id: "3",
    email: "jane@surity.com",
    display_name: "Jane Doe",
    role: "viewer",
    status: "active",
    last_login: "2026-01-30T09:15:00Z",
    created_at: "2026-01-20T00:00:00Z",
  },
  {
    id: "4",
    email: "pending@surity.com",
    display_name: null,
    role: "viewer",
    status: "pending",
    created_at: "2026-02-01T00:00:00Z",
  },
];

const roleVariants: Record<string, "success" | "warning" | "secondary"> = {
  admin: "success",
  editor: "warning",
  viewer: "secondary",
};

const statusVariants: Record<string, "success" | "warning" | "secondary"> = {
  active: "success",
  pending: "warning",
  disabled: "secondary",
};

export default function SettingsUsersPage() {
  const [users] = React.useState<User[]>(mockUsers);
  const [isInviteOpen, setIsInviteOpen] = React.useState(false);
  const [inviteForm, setInviteForm] = React.useState({ email: "", role: "viewer" });
  const [isInviting, setIsInviting] = React.useState(false);

  const handleInvite = async () => {
    setIsInviting(true);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsInviting(false);
    setIsInviteOpen(false);
    setInviteForm({ email: "", role: "viewer" });
  };

  const handleResendInvite = (userId: string) => {
    console.log("Resending invite to:", userId);
  };

  const handleRemoveUser = (userId: string) => {
    console.log("Removing user:", userId);
  };

  const columns: ColumnDef<User>[] = [
    {
      accessorKey: "email",
      header: ({ column }) => <DataTableColumnHeader column={column} title="User" />,
      cell: ({ row }) => (
        <div>
          <p className="font-medium">{row.original.display_name || "Pending"}</p>
          <p className="text-sm text-muted-foreground">{row.getValue("email")}</p>
        </div>
      ),
    },
    {
      accessorKey: "role",
      header: "Role",
      cell: ({ row }) => {
        const role = row.getValue("role") as string;
        return (
          <Badge variant={roleVariants[role]} className="capitalize">
            {role}
          </Badge>
        );
      },
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => {
        const status = row.getValue("status") as string;
        return (
          <Badge variant={statusVariants[status]} className="capitalize">
            {status}
          </Badge>
        );
      },
    },
    {
      accessorKey: "last_login",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Last Login" />,
      cell: ({ row }) => {
        const date = row.getValue("last_login") as string | undefined;
        return date ? format(new Date(date), "MMM d, yyyy HH:mm") : "Never";
      },
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const user = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {user.status === "pending" && (
                <DropdownMenuItem onClick={() => handleResendInvite(user.id)}>
                  <Mail className="mr-2 h-4 w-4" />
                  Resend Invite
                </DropdownMenuItem>
              )}
              <DropdownMenuItem>
                <Shield className="mr-2 h-4 w-4" />
                Change Role
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => handleRemoveUser(user.id)}
                className="text-destructive"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Remove User
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1">Users</h1>
          <p className="text-muted-foreground mt-1">
            Manage team members and their permissions
          </p>
        </div>
        <Button onClick={() => setIsInviteOpen(true)}>
          <UserPlus className="h-4 w-4 mr-2" />
          Invite User
        </Button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 rounded-lg border">
          <p className="text-sm text-muted-foreground">Total Users</p>
          <p className="text-2xl font-bold">{users.length}</p>
        </div>
        <div className="p-4 rounded-lg border">
          <p className="text-sm text-muted-foreground">Admins</p>
          <p className="text-2xl font-bold">{users.filter((u) => u.role === "admin").length}</p>
        </div>
        <div className="p-4 rounded-lg border">
          <p className="text-sm text-muted-foreground">Editors</p>
          <p className="text-2xl font-bold">{users.filter((u) => u.role === "editor").length}</p>
        </div>
        <div className="p-4 rounded-lg border">
          <p className="text-sm text-muted-foreground">Pending Invites</p>
          <p className="text-2xl font-bold">{users.filter((u) => u.status === "pending").length}</p>
        </div>
      </div>

      <DataTable
        columns={columns}
        data={users}
        searchKey="email"
        searchPlaceholder="Search users..."
      />

      <Dialog open={isInviteOpen} onOpenChange={setIsInviteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invite User</DialogTitle>
            <DialogDescription>
              Send an invitation email to add a new team member.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                value={inviteForm.email}
                onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })}
                placeholder="colleague@company.com"
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="role">Role</Label>
              <Select
                value={inviteForm.role}
                onValueChange={(v) => setInviteForm({ ...inviteForm, role: v })}
              >
                <SelectTrigger id="role">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">Admin — Full access</SelectItem>
                  <SelectItem value="editor">Editor — Can edit content</SelectItem>
                  <SelectItem value="viewer">Viewer — Read-only access</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsInviteOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleInvite} disabled={!inviteForm.email || isInviting}>
              {isInviting ? "Sending..." : "Send Invite"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
