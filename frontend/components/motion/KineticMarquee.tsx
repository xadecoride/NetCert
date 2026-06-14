"use client";

import { cn } from "@/lib/utils";

export function KineticMarquee({
  items,
  className,
  speed = 30,
}: {
  items: string[];
  className?: string;
  speed?: number;
}) {
  const content = items.join("  •  ");
  return (
    <div
      className={cn(
        "group relative flex overflow-hidden whitespace-nowrap border-y border-zinc-200 bg-zinc-50 py-4 dark:border-zinc-800 dark:bg-zinc-950",
        className
      )}
    >
      <div
        className="animate-marquee flex shrink-0 items-center gap-8 pr-8 text-sm font-medium text-zinc-500 dark:text-zinc-400"
        style={{ animationDuration: `${speed}s` }}
      >
        <span>{content}</span>
        <span>{content}</span>
      </div>
      <div
        className="animate-marquee flex shrink-0 items-center gap-8 pr-8 text-sm font-medium text-zinc-500 dark:text-zinc-400"
        style={{ animationDuration: `${speed}s` }}
      >
        <span>{content}</span>
        <span>{content}</span>
      </div>
    </div>
  );
}
