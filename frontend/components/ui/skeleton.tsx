import { cn } from "@/lib/utils";

interface SkeletonProps {
  className?: string;
  variant?: "shimmer" | "pulse";
  style?: React.CSSProperties;
}

export function Skeleton({ className, variant = "shimmer", style }: SkeletonProps) {
  return (
    <div
      className={cn(
        "rounded-xl bg-zinc-200 dark:bg-zinc-800",
        variant === "shimmer" && "skeleton-shimmer",
        variant === "pulse" && "animate-pulse",
        className
      )}
    />
  );
}

export function SkeletonText({ lines = 3, className }: { lines?: number; className?: string }) {
  return (
    <div className={cn("space-y-2", className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton
          key={i}
          className="h-4 w-full"
          style={{ width: `${100 - (i % 3) * 15}%` }}
        />
      ))}
    </div>
  );
}
