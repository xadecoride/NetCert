"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { LabWorkspace } from "@/components/lab/LabWorkspace";
import { useAuth } from "@/lib/auth-context";
import { labsApi } from "@/lib/api";
import { Spinner } from "@phosphor-icons/react";

interface LabInfo {
  id: string;
  slug: string;
  title: string;
  description: string;
  level: string;
  technology: string;
  duration_minutes: number;
  max_score: number;
  passing_score: number;
}

export default function LabPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const labId = params.id as string;

  const [lab, setLab] = useState<LabInfo | null>(null);
  const [submissionId, setSubmissionId] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pageReady, setPageReady] = useState(false);

  // Auth check
  useEffect(() => {
    if (authLoading) return;
    if (!isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    setPageReady(true);
  }, [isAuthenticated, authLoading, router]);

  // Load lab info
  useEffect(() => {
    if (!labId || !pageReady) return;

    // Try to find an existing active submission first
    labsApi.getActive()
      .then((activeSubs) => {
        const matchingSub = activeSubs?.find((s: any) => s.lab_id === labId);
        if (matchingSub) {
          setSubmissionId(matchingSub.id);
        }
      })
      .catch(() => {
        // No active submission — that's fine, will start a new one
      });

    // Load lab details
    labsApi.get(labId)
      .then((data) => {
        setLab(data);
      })
      .catch((err) => {
        setError(err.message || "Lab not found");
      });
  }, [labId, pageReady]);

  const startLab = async () => {
    setStarting(true);
    setError(null);

    try {
      const sub = await labsApi.start({ lab_id: labId, mode: "practice" });
      setSubmissionId(sub.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start lab");
    } finally {
      setStarting(false);
    }
  };

  // Loading
  if (!pageReady || (!lab && !error)) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-950">
        <div className="flex flex-col items-center gap-4">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
          <p className="text-zinc-400 text-sm">Loading lab...</p>
        </div>
      </div>
    );
  }

  // Error
  if (error && !submissionId) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-950">
        <div className="text-center max-w-md">
          <p className="text-red-400 text-lg font-medium mb-2">Failed to load lab</p>
          <p className="text-zinc-500 text-sm mb-6">{error}</p>
          <button
            onClick={() => startLab()}
            className="px-4 py-2 rounded-lg bg-emerald-600 text-white text-sm hover:bg-emerald-500 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Lab Workspace (active session)
  if (submissionId) {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || "/api/v1";
    const wsProtocol = typeof window !== "undefined" && window.location.protocol === "https:" ? "wss" : "ws";
    const wsHost = typeof window !== "undefined" ? window.location.host : "localhost:8080";
    const wsBase = `${wsProtocol}://${wsHost}`;

    return <LabWorkspace submissionId={submissionId} wsBaseUrl={wsBase} />;
  }

  // Start screen
  return (
    <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-950 text-white px-4">
      <div className="max-w-lg text-center">
        <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
          <svg
            viewBox="0 0 24 24"
            className="w-8 h-8 text-emerald-400"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="12" cy="12" r="6" />
            <path d="M12 6v12M6 12h12" />
          </svg>
        </div>

        <h1 className="text-3xl font-bold tracking-tight mb-3 text-white">
          {lab?.title || "Network Lab"}
        </h1>

        <p className="text-zinc-400 text-sm mb-6 max-w-md mx-auto leading-relaxed">
          {lab?.description || "Interactive lab environment with virtual Juniper devices. Practice CLI commands, configure protocols, and verify network operations in real-time."}
        </p>

        <div className="flex justify-center gap-4 mb-8 text-sm">
          <span className="px-3 py-1 rounded-full bg-zinc-800 text-zinc-300">
            {lab?.level || "JNCIA"}
          </span>
          <span className="px-3 py-1 rounded-full bg-zinc-800 text-zinc-300">
            {lab?.technology || "junos-cli"}
          </span>
          <span className="px-3 py-1 rounded-full bg-zinc-800 text-zinc-300">
            {lab?.duration_minutes || 15} min
          </span>
        </div>

        {error && (
          <div className="mb-6 p-3 rounded-lg bg-red-900/20 border border-red-800 text-sm text-red-400">
            {error}
          </div>
        )}

        <div className="flex justify-center gap-4">
          <button
            onClick={() => router.push("/labs")}
            className="px-4 py-2.5 rounded-lg border border-zinc-700 text-zinc-300 text-sm hover:bg-zinc-800 transition-colors"
          >
            Back to Labs
          </button>
          <button
            onClick={startLab}
            disabled={starting}
            className="px-6 py-2.5 rounded-lg bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-500 disabled:opacity-50 transition-colors flex items-center gap-2"
          >
            {starting ? (
              <>
                <Spinner className="h-4 w-4 animate-spin" weight="bold" />
                Deploying...
              </>
            ) : (
              <>
                <svg
                  viewBox="0 0 24 24"
                  className="w-4 h-4"
                  fill="currentColor"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
                Start Lab
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
