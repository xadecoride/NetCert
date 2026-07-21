"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { staggerContainer, fadeInUp } from "@/lib/motion";

export function PageShell({
  children,
  className,
  bare = false,
}: {
  children: React.ReactNode;
  className?: string;
  bare?: boolean;
}) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={staggerContainer}
      className={cn(
        "container-page px-4 sm:px-6 lg:px-8",
        bare ? "" : "py-8 pb-24 md:pb-8",
        className
      )}
    >
      {children}
    </motion.div>
  );
}

export function PageHeader({
  badge,
  title,
  subtitle,
  children,
  className,
}: {
  badge?: React.ReactNode;
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  children?: React.ReactNode;
  className?: string;
}) {
  return (
    <motion.div variants={fadeInUp} className={cn("mb-8 md:mb-10", className)}>
      {badge && <div className="mb-3">{badge}</div>}
      <h1 className="text-3xl md:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
        {title}
      </h1>
      {subtitle && (
        <p className="mt-2 text-base md:text-lg text-zinc-500 dark:text-zinc-400 max-w-[65ch]">
          {subtitle}
        </p>
      )}
      {children}
    </motion.div>
  );
}
