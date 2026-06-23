"use client";

import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from "react";
import { authApi } from "@/lib/api";

interface UserPreferences {
  language?: string;
  theme?: string;
  notifications?: {
    exam_reminders?: boolean;
    weekly_report?: boolean;
    new_questions?: boolean;
    marketing?: boolean;
  };
}

interface User {
  id: string;
  email: string;
  display_name: string;
  role: string;
  total_xp: number;
  streak_days: number;
  preferences?: UserPreferences;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, displayName: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  updateProfile: (data: { display_name?: string; avatar_url?: string | null }) => Promise<void>;
  updatePreferences: (data: Record<string, any>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchProfile = useCallback(async () => {
    try {
      const profile = await authApi.getProfile();
      setUser(profile);
    } catch {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      fetchProfile();
    } else {
      setLoading(false);
    }
  }, [fetchProfile]);

  const login = async (email: string, password: string) => {
    const response = await authApi.login({ email, password });
    localStorage.setItem("access_token", response.access_token);
    localStorage.setItem("refresh_token", response.refresh_token);
    setUser(response.user);
  };

  const register = async (email: string, password: string, displayName: string) => {
    const response = await authApi.register({ email, password, display_name: displayName });
    localStorage.setItem("access_token", response.access_token);
    localStorage.setItem("refresh_token", response.refresh_token);
    setUser(response.user);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  };

  const updateProfile = async (data: { display_name?: string; avatar_url?: string | null }) => {
    const updated = await authApi.updateProfile(data);
    setUser(updated);
  };

  const updatePreferences = async (data: Record<string, any>) => {
    const updated = await authApi.updatePreferences(data);
    setUser(updated);
  };

  return (
    <AuthContext.Provider
      value={{ user, loading, login, register, logout, isAuthenticated: !!user, updateProfile, updatePreferences }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
