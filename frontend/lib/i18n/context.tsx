"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";
import { en } from "./locales/en";
import { ru } from "./locales/ru";
import { authApi } from "@/lib/api";

export type Locale = "en" | "ru";
type NestedKeyOf<T> = T extends Record<string, any>
  ? {
      [K in keyof T]: K extends string
        ? T[K] extends Record<string, any>
          ? `${K}.${NestedKeyOf<T[K]>}`
          : K
        : never;
    }[keyof T]
  : never;

export type TranslationKey = NestedKeyOf<typeof en>;

const locales: Record<Locale, Record<string, any>> = { en, ru };

interface I18nContextType {
  locale: Locale;
  setLocale: (locale: Locale) => Promise<void>;
  t: (path: TranslationKey, params?: Record<string, string | number>) => string;
  isLoading: boolean;
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

function resolveNested(obj: Record<string, any>, path: string): string {
  const keys = path.split(".");
  let current = obj;
  for (const key of keys) {
    if (current && typeof current === "object" && key in current) {
      current = current[key];
    } else {
      return path;
    }
  }
  return typeof current === "string" ? current : path;
}

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("en");
  const [isLoading, setIsLoading] = useState(true);

  // Load saved locale on mount
  useEffect(() => {
    const saved = localStorage.getItem("locale") as Locale | null;
    if (saved === "en" || saved === "ru") {
      setLocaleState(saved);
    }
    setIsLoading(false);
  }, []);

  // Update html lang attribute
  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);

  const setLocale = useCallback(async (newLocale: Locale) => {
    setLocaleState(newLocale);
    localStorage.setItem("locale", newLocale);
    document.documentElement.lang = newLocale;

    // Try to persist to backend if user is logged in
    try {
      const token = localStorage.getItem("access_token");
      if (token) {
        await authApi.updatePreferences({ language: newLocale });
      }
    } catch {
      // Offline — locale is saved locally
    }
  }, []);

  const t = useCallback(
    (path: TranslationKey, params?: Record<string, string | number>): string => {
      const dict = locales[locale] || en;
      let value = resolveNested(dict, path as string);

      if (params) {
        for (const [key, val] of Object.entries(params)) {
          value = value.replace(`{${key}}`, String(val));
        }
      }

      return value;
    },
    [locale]
  );

  return (
    <I18nContext.Provider value={{ locale, setLocale, t, isLoading }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useTranslation() {
  const context = useContext(I18nContext);
  if (context === undefined) {
    throw new Error("useTranslation must be used within an I18nProvider");
  }
  return context;
}

export { I18nContext };
