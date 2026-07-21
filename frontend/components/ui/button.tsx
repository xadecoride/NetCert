"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "relative inline-flex items-center justify-center rounded-xl text-sm font-medium transition-all duration-300 " +
    "focus-visible:outline-none focus-visible:outline-2 focus-visible:outline-emerald-500 focus-visible:outline-offset-2 " +
    "disabled:opacity-50 disabled:pointer-events-none active:scale-[0.97] select-none",
  {
    variants: {
      variant: {
        primary:
          "bg-emerald-500 text-white hover:bg-emerald-600 shadow-[var(--shadow-glow-emerald-soft)] hover:shadow-[var(--shadow-glow-emerald)]",
        accent:
          "bg-cyan-500 text-white hover:bg-cyan-600 shadow-[var(--shadow-glow-cyan-soft)] hover:shadow-[var(--shadow-glow-cyan)]",
        secondary:
          "bg-zinc-100 text-zinc-900 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-100 dark:hover:bg-zinc-700",
        outline:
          "border border-zinc-300 bg-white/50 text-zinc-700 hover:bg-zinc-100 hover:border-zinc-400 dark:bg-zinc-900/50 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800",
        ghost:
          "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800",
        glass:
          "bg-white/70 backdrop-blur-xl border border-white/30 text-zinc-900 hover:bg-white/80 dark:bg-zinc-900/70 dark:border-zinc-700/50 dark:text-zinc-100 dark:hover:bg-zinc-800/80",
        danger:
          "bg-red-500 text-white hover:bg-red-600 shadow-[0_1px_3px_rgba(239,68,68,0.2)] hover:shadow-[0_8px_24px_rgba(239,68,68,0.35)]",
        link:
          "text-emerald-600 underline-offset-4 hover:underline dark:text-emerald-400",
      },
      size: {
        sm: "h-9 px-3 text-xs",
        md: "h-10 px-4",
        lg: "h-12 px-6 text-base",
        xl: "h-14 px-8 text-lg",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, children, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }), loading && "overflow-hidden")}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <span className="absolute inset-0 skeleton-shimmer opacity-30" />
        )}
        <span className={cn("relative flex items-center gap-2", loading && "opacity-80")}>
          {children}
        </span>
      </button>
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
