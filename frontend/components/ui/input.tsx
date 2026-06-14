"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helper?: string;
  rightElement?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, helper, rightElement, ...props }, ref) => {
    return (
      <div className={cn("space-y-1.5", className)}>
        {label && (
          <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <input
            ref={ref}
            className={cn(
              "flex w-full rounded-xl border bg-white/70 px-4 py-2.5 text-sm text-zinc-900 placeholder:text-zinc-400 transition-all duration-200",
              "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/50 focus-visible:border-emerald-500",
              "dark:bg-zinc-900/70 dark:text-zinc-100 dark:border-zinc-700",
              error
                ? "border-red-300 focus-visible:border-red-500 focus-visible:ring-red-500/30 dark:border-red-800"
                : "border-zinc-300 hover:border-zinc-400 dark:hover:border-zinc-600",
              rightElement && "pr-10"
            )}
            {...props}
          />
          {rightElement && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 dark:text-zinc-500">
              {rightElement}
            </div>
          )}
        </div>
        {error ? (
          <p className="text-xs text-red-500">{error}</p>
        ) : helper ? (
          <p className="text-xs text-zinc-500 dark:text-zinc-400">{helper}</p>
        ) : null}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
