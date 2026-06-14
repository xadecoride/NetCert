"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { useState } from "react";
import { useTheme } from "next-themes";
import { MobileNav } from "./mobile-nav";
import {
  Layout,
  BookOpen,
  Gear,
  SignOut,
  List,
  X,
  ComputerTower,
  Book,
  Sun,
  Moon,
  Translate,
} from "@phosphor-icons/react";

export function Header() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const { t, locale, setLocale } = useTranslation();
  const { theme, setTheme } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: "/dashboard", label: t("nav.dashboard"), icon: Layout },
    { href: "/exams", label: t("nav.exams"), icon: BookOpen },
    { href: "/labs", label: t("nav.labs"), icon: ComputerTower },
    { href: "/study", label: t("nav.study"), icon: Book },
    { href: "/settings", label: t("nav.settings"), icon: Gear },
  ];

  if (pathname === "/" || pathname?.startsWith("/exam/")) return <MobileNav />;

  const toggleTheme = () => setTheme(theme === "dark" ? "light" : "dark");
  const toggleLocale = () => setLocale(locale === "en" ? "ru" : "en");

  return (
    <>
      <header className="sticky top-0 z-40 w-full border-b border-zinc-200/80 bg-white/70 backdrop-blur-xl dark:border-zinc-800/80 dark:bg-zinc-950/70">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center transition-transform duration-300 group-hover:scale-105 group-hover:rotate-3">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" />
                  <path d="M2 17l10 5 10-5" />
                  <path d="M2 12l10 5 10-5" />
                </svg>
              </div>
              <span className="font-semibold text-lg tracking-tight text-zinc-900 dark:text-zinc-100">
                NetCert
              </span>
            </Link>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center gap-1">
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = pathname?.startsWith(link.href);
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={cn(
                      "flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-all duration-200",
                      isActive
                        ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                        : "text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:text-zinc-100 dark:hover:bg-zinc-800/50"
                    )}
                  >
                    <Icon className="h-4 w-4" weight={isActive ? "fill" : "regular"} />
                    {link.label}
                  </Link>
                );
              })}
            </nav>

            {/* Right side */}
            <div className="flex items-center gap-2">
              <button
                onClick={toggleTheme}
                className="hidden md:flex h-10 w-10 items-center justify-center rounded-xl text-zinc-500 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-colors"
                aria-label="Toggle theme"
              >
                {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </button>
              <button
                onClick={toggleLocale}
                className="hidden md:flex h-10 px-2.5 items-center gap-1.5 rounded-xl text-xs font-medium text-zinc-500 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-colors"
                aria-label="Toggle language"
              >
                <Translate className="h-4 w-4" />
                {locale.toUpperCase()}
              </button>

              {user ? (
                <div className="hidden md:flex items-center gap-3 ml-2">
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-zinc-100 dark:bg-zinc-800">
                    <div className="w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center">
                      <span className="text-[10px] font-bold text-white">
                        {user.display_name?.charAt(0) || "U"}
                      </span>
                    </div>
                    <span className="text-sm text-zinc-600 dark:text-zinc-300">
                      {user.display_name?.split(" ")[0]}
                    </span>
                  </div>
                  <Button variant="ghost" size="icon" onClick={logout}>
                    <SignOut className="h-4 w-4" weight="regular" />
                  </Button>
                </div>
              ) : (
                <div className="hidden md:flex items-center gap-2 ml-2">
                  <Link href="/auth/login">
                    <Button variant="ghost" size="sm">{t("nav.signIn")}</Button>
                  </Link>
                  <Link href="/auth/register">
                    <Button variant="primary" size="sm">{t("nav.getStarted")}</Button>
                  </Link>
                </div>
              )}

              {/* Mobile menu button */}
              <button
                className="md:hidden p-2 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label="Toggle menu"
              >
                {mobileMenuOpen ? (
                  <X className="h-5 w-5 text-zinc-600 dark:text-zinc-400" weight="regular" />
                ) : (
                  <List className="h-5 w-5 text-zinc-600 dark:text-zinc-400" weight="regular" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          {mobileMenuOpen && (
            <div className="md:hidden pb-4 border-t border-zinc-200 dark:border-zinc-800 pt-4 animate-in slide-in-from-top-2 duration-200">
              <nav className="flex flex-col gap-1">
                {navLinks.map((link) => {
                  const Icon = link.icon;
                  const isActive = pathname?.startsWith(link.href);
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={cn(
                        "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors",
                        isActive
                          ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                          : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
                      )}
                    >
                      <Icon className="h-4 w-4" weight={isActive ? "fill" : "regular"} />
                      {link.label}
                    </Link>
                  );
                })}
                <div className="flex items-center gap-2 mt-2 px-3">
                  <button
                    onClick={toggleTheme}
                    className="flex flex-1 items-center justify-center gap-2 py-2 rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 text-sm"
                  >
                    {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                    {theme === "dark" ? "Light" : "Dark"}
                  </button>
                  <button
                    onClick={toggleLocale}
                    className="flex flex-1 items-center justify-center gap-2 py-2 rounded-xl bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 text-sm"
                  >
                    <Translate className="h-4 w-4" />
                    {locale === "en" ? "RU" : "EN"}
                  </button>
                </div>
                {user ? (
                  <button
                    onClick={() => { logout(); setMobileMenuOpen(false); }}
                    className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20 transition-colors"
                  >
                    <SignOut className="h-4 w-4" weight="regular" />
                    {t("nav.signOut")}
                  </button>
                ) : (
                  <>
                    <div className="border-t border-zinc-200 dark:border-zinc-800 my-2" />
                    <Link
                      href="/auth/login"
                      onClick={() => setMobileMenuOpen(false)}
                      className="px-3 py-2.5 text-sm font-medium text-zinc-600 dark:text-zinc-400"
                    >
                      {t("nav.signIn")}
                    </Link>
                    <Link href="/auth/register" onClick={() => setMobileMenuOpen(false)} className="px-3">
                      <Button variant="primary" size="sm" className="w-full">
                        {t("nav.getStarted")}
                      </Button>
                    </Link>
                  </>
                )}
              </nav>
            </div>
          )}
        </div>
      </header>
      <MobileNav />
    </>
  );
}
