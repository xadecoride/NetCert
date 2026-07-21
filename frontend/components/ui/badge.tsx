import * as React from "react";
import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        // Emerald-tinted — the primary brand look
        default:
          "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
        // Neutral
        secondary:
          "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400",
        outline:
          "border border-zinc-300 text-zinc-600 dark:border-zinc-700 dark:text-zinc-400",
        // Semantic
        success:
          "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
        warning:
          "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",
        danger:
          "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
        info:
          "bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300",
        // Brand
        juniper:
          "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
        cisco:
          "bg-sky-100 text-sky-700 dark:bg-sky-900/30 dark:text-sky-300",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
  pulse?: boolean;
}

function Badge({ className, variant, pulse, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props}>
      {pulse && (
        <span className="relative flex h-1.5 w-1.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-current opacity-75" />
          <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-current" />
        </span>
      )}
      {props.children}
    </div>
  );
}

export { Badge, badgeVariants };
