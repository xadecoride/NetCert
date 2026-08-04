"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useTranslation } from "@/lib/i18n/context";
import {
  Layout,
  BookOpen,
  ComputerTower,
  Book,
  Gear,
} from "@phosphor-icons/react";

export function MobileNav() {
  const pathname = usePathname();
  const { t } = useTranslation();

  const links = [
    { href: "/dashboard", label: t("nav.dashboard"), icon: Layout },
    { href: "/exams", label: t("nav.exams"), icon: BookOpen },
    { href: "/labs", label: t("nav.labs"), icon: ComputerTower },
    { href: "/study", label: t("nav.study"), icon: Book },
    { href: "/settings", label: t("nav.settings"), icon: Gear },
  ];

  if (pathname === "/" || pathname?.startsWith("/exams/")) return null;

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-[var(--z-overlay)] border-t border-zinc-200 bg-white/90 backdrop-blur-xl backdrop-saturate-150 dark:border-zinc-800 dark:bg-zinc-950/90 md:hidden">
      <div className="flex items-center justify-around px-2 pb-safe">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname?.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "relative flex flex-col items-center gap-0.5 py-2.5 px-3 text-[10px] font-medium transition-colors",
                isActive
                  ? "text-emerald-600 dark:text-emerald-400"
                  : "text-zinc-500 dark:text-zinc-400"
              )}
            >
              <Icon
                className={cn("h-5 w-5", isActive && "text-emerald-600 dark:text-emerald-400")}
                weight={isActive ? "fill" : "regular"}
              />
              <span className="truncate max-w-[3.5rem]">{link.label}</span>
              {isActive && (
                <span className="absolute top-0 h-0.5 w-6 rounded-full bg-cyan-500 dark:bg-cyan-400" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
