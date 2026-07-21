"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

const fieldBase =
  "flex w-full rounded-xl border bg-white/70 px-4 py-2.5 text-sm text-zinc-900 placeholder:text-zinc-400 transition-all duration-200 " +
  "focus-visible:outline-none focus-visible:outline-2 focus-visible:outline-emerald-500 focus-visible:outline-offset-2 " +
  "dark:bg-zinc-900/70 dark:text-zinc-100 dark:placeholder:text-zinc-500";

const fieldBorderNormal =
  "border-zinc-300 hover:border-zinc-400 dark:border-zinc-700 dark:hover:border-zinc-600";
const fieldBorderError =
  "border-red-300 focus-visible:outline-red-500 dark:border-red-800";

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
            className={cn(fieldBase, error ? fieldBorderError : fieldBorderNormal, rightElement && "pr-10")}
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

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helper?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, helper, ...props }, ref) => {
    return (
      <div className={cn("space-y-1.5", className)}>
        {label && (
          <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <textarea
          ref={ref}
          className={cn(
            fieldBase,
            "min-h-[96px] resize-y",
            error ? fieldBorderError : fieldBorderNormal,
            className
          )}
          {...props}
        />
        {error ? (
          <p className="text-xs text-red-500">{error}</p>
        ) : helper ? (
          <p className="text-xs text-zinc-500 dark:text-zinc-400">{helper}</p>
        ) : null}
      </div>
    );
  }
);
Textarea.displayName = "Textarea";

export interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  helper?: string;
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, helper, children, ...props }, ref) => {
    return (
      <div className={cn("space-y-1.5", className)}>
        {label && (
          <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <select
          ref={ref}
          className={cn(fieldBase, "appearance-none pr-10", error ? fieldBorderError : fieldBorderNormal)}
          {...props}
        >
          {children}
        </select>
        {error ? (
          <p className="text-xs text-red-500">{error}</p>
        ) : helper ? (
          <p className="text-xs text-zinc-500 dark:text-zinc-400">{helper}</p>
        ) : null}
      </div>
    );
  }
);
Select.displayName = "Select";

export { Input, Textarea, Select };
