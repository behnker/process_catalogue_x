import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UserBrief {
  id: string;
  email: string;
  display_name: string | null;
  avatar_url: string | null;
  role: string;
  organization_id: string;
  organization_name: string;
}

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: UserBrief | null;
  isAuthenticated: boolean;
  setAuth: (accessToken: string, refreshToken: string, user: UserBrief) => void;
  logout: () => void;
  switchOrganization: (orgId: string, orgName: string, role: string) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,

      setAuth: (accessToken, refreshToken, user) =>
        set({ accessToken, refreshToken, user, isAuthenticated: true }),

      logout: () =>
        set({
          accessToken: null,
          refreshToken: null,
          user: null,
          isAuthenticated: false,
        }),

      switchOrganization: (orgId, orgName, role) =>
        set((state) => ({
          user: state.user
            ? { ...state.user, organization_id: orgId, organization_name: orgName, role }
            : null,
        })),
    }),
    {
      name: "pc-auth",
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
