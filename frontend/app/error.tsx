"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ErrorPage({ error, reset }: { error: Error; reset: () => void }) {
  const router = useRouter();

  useEffect(() => {
    // Silent console log for debugging — not visible to user
    console.error("Global error boundary caught:", error.message);
  }, [error]);

  return (
    <div className="min-h-[calc(100dvh-4rem)] flex items-center justify-center bg-zinc-50 dark:bg-zinc-950 px-6">
      <div className="max-w-md text-center rounded-[2rem] border border-zinc-200 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/50 backdrop-blur-xl p-8 shadow-[var(--shadow-diffuse-lg)]">
        <h2 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 mb-3">Something went wrong</h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6 leading-relaxed">
          We could not load this page. This is usually a temporary issue with the network or server.
        </p>
        <div className="flex items-center justify-center gap-3">
          <button
            onClick={() => reset()}
            className="inline-flex items-center gap-2 rounded-xl bg-emerald-500 text-white px-5 py-2.5 text-sm font-medium hover:bg-emerald-600 transition-colors shadow-[var(--shadow-glow-emerald-soft)]"
          >
            Try again
          </button>
          <button
            onClick={() => router.push("/")}
            className="inline-flex items-center gap-2 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white/50 dark:bg-zinc-800/50 px-5 py-2.5 text-sm font-medium text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
          >
            Go home
          </button>
        </div>
      </div>
    </div>
  );
}
