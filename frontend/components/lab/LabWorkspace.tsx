"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Terminal,
  Network,
  ListChecks,
  CornersOut,
  CornersIn,
  X,
  Spinner,
  CheckCircle,
  Circle,
  Trophy,
  WarningCircle,
} from "@phosphor-icons/react";

import { LabTerminal } from "./LabTerminal";
import { labsApi } from "@/lib/api";
import { springTransition } from "@/lib/motion";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BentoCard } from "@/components/ui/card";

interface LabDevice {
  name: string;
  kind: string;
  mgmt_ip: string;
  status: string;
}

interface LabSubmission {
  id: string;
  lab_id: string;
  status: string;
  pod_id: string;
  devices: LabDevice[];
  started_at: string;
  time_remaining_seconds: number;
  current_score: number;
  max_score: number;
  terminal_ws_url: string;
}

interface LabWorkspaceProps {
  submissionId: string;
}

const defaultTasks = [
  "Deploy the lab topology",
  "Configure the required protocols",
  "Verify connectivity and behavior",
  "Submit your work for grading",
];

function DeviceIcon({ kind }: { kind: string }) {
  if (kind === "juniper_crpd" || kind === "router") {
    return (
      <svg viewBox="0 0 24 24" className="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="6" />
        <path d="M12 6v12M6 12h12" />
      </svg>
    );
  }
  if (kind === "firewall" || kind === "juniper_vsrx") {
    return (
      <svg viewBox="0 0 24 24" className="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 2l8 4v6c0 5-8 8-8 8s-8-3-8-8V6l8-4z" />
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 24 24" className="w-5 h-5 text-zinc-400" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="2" y="2" width="20" height="8" rx="2" />
      <rect x="2" y="14" width="20" height="8" rx="2" />
    </svg>
  );
}

function TopologyPlaceholder() {
  return (
    <div className="w-full aspect-[4/3] rounded-xl bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center relative overflow-hidden">
      <Network className="h-8 w-8 text-zinc-400 absolute" weight="regular" />
      <svg viewBox="0 0 200 140" className="w-full h-full opacity-30" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="40" cy="70" r="18" className="text-zinc-500" />
        <circle cx="100" cy="35" r="16" className="text-emerald-500" />
        <circle cx="160" cy="70" r="18" className="text-zinc-500" />
        <circle cx="100" cy="110" r="16" className="text-zinc-500" />
        <line x1="58" y1="70" x2="84" y2="45" className="text-zinc-400" />
        <line x1="116" y1="45" x2="142" y2="70" className="text-zinc-400" />
        <line x1="40" y1="88" x2="84" y2="100" className="text-zinc-400" />
        <line x1="116" y1="100" x2="142" y2="88" className="text-zinc-400" />
      </svg>
    </div>
  );
}

export function LabWorkspace({ submissionId }: LabWorkspaceProps) {
  const [submission, setSubmission] = useState<LabSubmission | null>(null);
  const [activeDevice, setActiveDevice] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [fullscreen, setFullscreen] = useState(false);
  const [mobilePanel, setMobilePanel] = useState<"devices" | "tasks" | null>(null);
  const [checkedTasks, setCheckedTasks] = useState<Set<number>>(new Set());
  const [grading, setGrading] = useState(false);
  const [gradeResult, setGradeResult] = useState<{ score: number; max_score: number } | null>(null);

  useEffect(() => {
    const fetchSubmission = async () => {
      try {
        const data = await labsApi.getSubmission(submissionId);
        setSubmission(data);
        setTimeRemaining(data.time_remaining_seconds || 0);
        if (data.devices && data.devices.length > 0) {
          setActiveDevice(data.devices[0].name);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load lab");
      } finally {
        setLoading(false);
      }
    };
    fetchSubmission();
  }, [submissionId]);

  useEffect(() => {
    if (timeRemaining <= 0) return;
    const interval = setInterval(() => {
      setTimeRemaining((prev) => Math.max(0, prev - 1));
    }, 1000);
    return () => clearInterval(interval);
  }, [timeRemaining]);

  const formatTime = useCallback((seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  }, []);

  const wsUrl =
    typeof window !== "undefined"
      ? `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}/ws/lab/${submissionId}/${activeDevice || ""}`
      : "";

  const toggleTask = (idx: number) => {
    setCheckedTasks((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  const handleGrade = async () => {
    setGrading(true);
    try {
      const scores = await labsApi.getScores(submissionId);
      const score = Array.isArray(scores) ? scores.reduce((sum: number, s: any) => sum + (s.score || 0), 0) : 0;
      const max = submission?.max_score || 0;
      setGradeResult({ score, max_score: max });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to grade lab");
    } finally {
      setGrading(false);
    }
  };

  const handleEndLab = async () => {
    if (!confirm("Are you sure you want to end this lab session?")) return;
    try {
      await labsApi.stopSubmission(submissionId);
      window.location.href = "/labs";
    } catch {
      alert("Failed to stop lab");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[100dvh] bg-zinc-50 dark:bg-zinc-950">
        <div className="flex flex-col items-center gap-4">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
          <p className="text-zinc-500 dark:text-zinc-400 text-sm">Starting lab environment...</p>
        </div>
      </div>
    );
  }

  if (error || !submission) {
    return (
      <div className="flex items-center justify-center min-h-[100dvh] bg-zinc-50 dark:bg-zinc-950 px-4">
        <div className="text-center max-w-md">
          <WarningCircle className="h-12 w-12 mx-auto mb-4 text-red-500" weight="fill" />
          <p className="text-zinc-900 dark:text-zinc-100 text-lg font-medium mb-2">Failed to load lab</p>
          <p className="text-zinc-500 dark:text-zinc-400 text-sm mb-6">{error || "Unknown error"}</p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      </div>
    );
  }

  const progress = defaultTasks.length ? Math.round((checkedTasks.size / defaultTasks.length) * 100) : 0;

  const workspace = (
    <div className="flex flex-col h-full min-h-[100dvh] bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
      {/* Header */}
      <header className="flex items-center justify-between gap-3 px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/70 backdrop-blur-xl shrink-0 z-10">
        <div className="flex items-center gap-3 min-w-0">
          <div className="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-900/20">
            <Terminal className="h-4 w-4 text-emerald-600 dark:text-emerald-400" weight="fill" />
          </div>
          <div className="min-w-0">
            <h1 className="text-sm font-semibold truncate">Lab Workspace</h1>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 truncate">Pod {submission.pod_id}</p>
          </div>
          <Badge variant={submission.status === "running" ? "success" : "warning"} pulse={submission.status === "running"}>
            {submission.status}
          </Badge>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-1.5 text-xs">
            <Trophy className="h-3.5 w-3.5 text-emerald-500" weight="fill" />
            <span className="text-zinc-500 dark:text-zinc-400">Score:</span>
            <span className="font-medium text-zinc-900 dark:text-zinc-100">
              {gradeResult ? gradeResult.score : submission.current_score}/{gradeResult ? gradeResult.max_score : submission.max_score}
            </span>
          </div>
          <div
            className={cn(
              "font-mono text-sm font-bold",
              timeRemaining < 300 && "text-red-500 animate-pulse",
              timeRemaining >= 300 && timeRemaining < 900 && "text-amber-500",
              timeRemaining >= 900 && "text-emerald-600 dark:text-emerald-400"
            )}
          >
            {formatTime(timeRemaining)}
          </div>
          <div className="hidden md:flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={handleGrade} loading={grading}>
              <Trophy className="h-3.5 w-3.5 mr-1.5" weight="fill" />
              Grade
            </Button>
            <Button variant="danger" size="sm" onClick={handleEndLab}>
              <X className="h-3.5 w-3.5 mr-1.5" weight="bold" />
              End
            </Button>
            <Button variant="ghost" size="icon" onClick={() => setFullscreen((v) => !v)}>
              {fullscreen ? <CornersIn className="h-4 w-4" /> : <CornersOut className="h-4 w-4" />}
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile panel toggles */}
      <div className="flex md:hidden items-center gap-2 px-4 py-2 border-b border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 shrink-0">
        <Button
          variant={mobilePanel === "devices" ? "primary" : "outline"}
          size="sm"
          className="flex-1"
          onClick={() => setMobilePanel((p) => (p === "devices" ? null : "devices"))}
        >
          <Network className="h-3.5 w-3.5 mr-1.5" weight="fill" />
          Devices
        </Button>
        <Button
          variant={mobilePanel === "tasks" ? "primary" : "outline"}
          size="sm"
          className="flex-1"
          onClick={() => setMobilePanel((p) => (p === "tasks" ? null : "tasks"))}
        >
          <ListChecks className="h-3.5 w-3.5 mr-1.5" weight="fill" />
          Tasks
        </Button>
      </div>

      {/* Main */}
      <div className="flex flex-1 overflow-hidden">
        {/* Device sidebar */}
        <aside
          className={cn(
            "w-full md:w-72 shrink-0 border-r border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 overflow-y-auto",
            "absolute md:relative z-20 inset-x-0 top-[112px] md:top-0 bottom-0 md:bottom-auto md:inset-auto",
            mobilePanel === "devices" ? "block" : "hidden md:block"
          )}
        >
          <div className="p-4">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-3">
              Devices
            </h2>
            <div className="space-y-2">
              {(submission.devices || []).map((device) => (
                <button
                  key={device.name}
                  onClick={() => {
                    setActiveDevice(device.name);
                    setMobilePanel(null);
                  }}
                  className={cn(
                    "w-full flex items-center gap-3 p-3 rounded-xl text-left transition-all border",
                    activeDevice === device.name
                      ? "bg-emerald-50 dark:bg-emerald-900/10 border-emerald-200 dark:border-emerald-900/30"
                      : "bg-zinc-50 dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 hover:border-emerald-300 dark:hover:border-emerald-800"
                  )}
                >
                  <div className="flex-shrink-0 w-9 h-9 rounded-lg bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center">
                    <DeviceIcon kind={device.kind} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{device.name}</div>
                    <div className="flex items-center gap-1.5 mt-0.5">
                      <span
                        className={cn(
                          "w-1.5 h-1.5 rounded-full",
                          device.status === "running" && "bg-emerald-500",
                          device.status === "starting" && "bg-amber-500",
                          device.status !== "running" && device.status !== "starting" && "bg-red-500"
                        )}
                      />
                      <span className="text-xs text-zinc-500 dark:text-zinc-400">{device.status}</span>
                    </div>
                  </div>
                  {activeDevice === device.name && <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />}
                </button>
              ))}
            </div>

            <div className="mt-6">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-3">
                Topology
              </h2>
              <TopologyPlaceholder />
            </div>
          </div>
        </aside>

        {/* Terminal */}
        <main className="flex-1 flex flex-col overflow-hidden min-w-0">
          <div className="flex items-center bg-white/50 dark:bg-zinc-900/50 border-b border-zinc-200 dark:border-zinc-800 shrink-0 overflow-x-auto">
            {(submission.devices || []).map((device) => (
              <button
                key={device.name}
                onClick={() => setActiveDevice(device.name)}
                className={cn(
                  "flex items-center gap-1.5 px-4 py-2 text-xs border-b-2 transition-all whitespace-nowrap",
                  activeDevice === device.name
                    ? "border-emerald-500 text-zinc-900 dark:text-zinc-100 bg-emerald-50/50 dark:bg-emerald-900/10"
                    : "border-transparent text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300"
                )}
              >
                <span
                  className={cn(
                    "w-1.5 h-1.5 rounded-full",
                    device.status === "running" ? "bg-emerald-500" : "bg-amber-500"
                  )}
                />
                {device.name}
              </button>
            ))}
          </div>
          <div className="flex-1 overflow-hidden bg-zinc-950">
            {activeDevice && wsUrl && (
              <LabTerminal key={activeDevice} deviceName={activeDevice} wsUrl={wsUrl} className="h-full rounded-none border-0" />
            )}
          </div>

          {/* Mobile end/grade */}
          <div className="flex md:hidden items-center gap-2 p-3 border-t border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 shrink-0">
            <Button variant="outline" size="sm" className="flex-1" onClick={handleGrade} loading={grading}>
              <Trophy className="h-3.5 w-3.5 mr-1.5" weight="fill" />
              Grade
            </Button>
            <Button variant="danger" size="sm" className="flex-1" onClick={handleEndLab}>
              <X className="h-3.5 w-3.5 mr-1.5" weight="bold" />
              End Lab
            </Button>
          </div>
        </main>

        {/* Tasks panel */}
        <aside
          className={cn(
            "w-full lg:w-80 shrink-0 border-l border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 overflow-y-auto",
            "absolute lg:relative z-20 inset-x-0 top-[112px] lg:top-0 bottom-0 lg:bottom-auto lg:inset-auto",
            mobilePanel === "tasks" ? "block" : "hidden lg:block"
          )}
        >
          <div className="p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                Task Checklist
              </h2>
              <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400">{progress}%</span>
            </div>
            <div className="h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden mb-4">
              <motion.div
                className="h-full bg-emerald-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={springTransition}
              />
            </div>

            <div className="space-y-2 mb-6">
              {defaultTasks.map((task, idx) => {
                const checked = checkedTasks.has(idx);
                return (
                  <button
                    key={idx}
                    onClick={() => toggleTask(idx)}
                    className={cn(
                      "w-full flex items-start gap-3 p-3 rounded-xl text-left transition-all border",
                      checked
                        ? "bg-emerald-50 dark:bg-emerald-900/10 border-emerald-200 dark:border-emerald-900/30"
                        : "bg-zinc-50 dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700"
                    )}
                  >
                    {checked ? (
                      <CheckCircle className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" weight="fill" />
                    ) : (
                      <Circle className="h-4 w-4 text-zinc-400 shrink-0 mt-0.5" weight="regular" />
                    )}
                    <span className={cn("text-sm", checked && "line-through text-zinc-400")}>{task}</span>
                  </button>
                );
              })}
            </div>

            {gradeResult && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-900/10 border border-emerald-200 dark:border-emerald-900/30 mb-4"
              >
                <div className="text-xs text-zinc-500 dark:text-zinc-400 uppercase tracking-wider mb-1">
                  Latest grade
                </div>
                <div className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
                  {gradeResult.score} / {gradeResult.max_score}
                </div>
              </motion.div>
            )}

            <BentoCard className="p-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-2">
                Lab Info
              </h3>
              <div className="space-y-1 text-xs text-zinc-600 dark:text-zinc-400">
                <p>
                  Status: <span className="text-zinc-900 dark:text-zinc-100 capitalize">{submission.status}</span>
                </p>
                <p>
                  Devices: <span className="text-zinc-900 dark:text-zinc-100">{(submission.devices || []).length}</span>
                </p>
                <p>
                  Started: <span className="text-zinc-900 dark:text-zinc-100">{new Date(submission.started_at).toLocaleTimeString()}</span>
                </p>
              </div>
            </BentoCard>
          </div>
        </aside>
      </div>
    </div>
  );

  return fullscreen ? (
    <div className="fixed inset-0 z-50">{workspace}</div>
  ) : (
    <div className="flex flex-col h-full">{workspace}</div>
  );
}
