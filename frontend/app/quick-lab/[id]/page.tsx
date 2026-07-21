"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { quickLabsApi } from "@/lib/api";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
import {
  ArrowLeft,
  Clock,
  Lightning,
  Network,
  CheckCircle,
  Lightbulb,
  Key,
  BookOpen,
  CaretDown,
  CaretRight,
  ListChecks,
  Terminal,
  Copy,
  Check,
} from "@phosphor-icons/react";

interface QuickLabTask {
  order: number;
  title: string;
  description: string;
  verification_commands?: string[];
  expected_output_summary?: string;
}

interface QuickLabHint {
  order: number;
  title: string;
  content: string;
}

interface QuickLabAnswer {
  order: number;
  task_order: number;
  content: string;
}

interface QuickLabExplanation {
  order: number;
  title: string;
  content: string;
}

interface QuickLabSolutionCommand {
  order: number;
  task_order: number;
  commands: string[];
  expected_output?: string;
}

interface QuickLab {
  id: string;
  slug: string;
  title: string;
  description: string;
  level: string;
  difficulty: number;
  estimated_minutes: number;
  technology: string;
  topology_svg?: string;
  pnetlab_instructions: string;
  tasks: QuickLabTask[];
  hints: QuickLabHint[];
  answers: QuickLabAnswer[];
  explanations: QuickLabExplanation[];
  solution_commands: QuickLabSolutionCommand[];
  prerequisite_topics: string[];
}

type TabKey = "tasks" | "hints" | "answers" | "explanations" | "solutions";

const tabs: { key: TabKey; label: string; icon: any }[] = [
  { key: "tasks", label: "Tasks", icon: ListChecks },
  { key: "hints", label: "Hints", icon: Lightbulb },
  { key: "answers", label: "Answers", icon: Key },
  { key: "explanations", label: "Breakdown", icon: BookOpen },
  { key: "solutions", label: "Solution", icon: Terminal },
];

const getDifficultyLabel = (d: number) => {
  const labels = ["", "Beginner", "Easy", "Medium", "Hard", "Expert"];
  return labels[d] || "Unknown";
};

const getDifficultyColor = (d: number) => {
  const colors: Record<number, string> = {
    1: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300",
    2: "bg-sky-100 text-sky-700 dark:bg-sky-900/20 dark:text-sky-300",
    3: "bg-amber-100 text-amber-700 dark:bg-amber-900/20 dark:text-amber-300",
    4: "bg-orange-100 text-orange-700 dark:bg-orange-900/20 dark:text-orange-300",
    5: "bg-rose-100 text-rose-700 dark:bg-rose-900/20 dark:text-rose-300",
  };
  return colors[d] || "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300";
};

export default function QuickLabPage() {
  const { id } = useParams();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();

  const [lab, setLab] = useState<QuickLab | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabKey>("tasks");
  const [completedTasks, setCompletedTasks] = useState<Set<number>>(new Set());
  const [expandedHints, setExpandedHints] = useState<Set<number>>(new Set());
  const [expandedAnswers, setExpandedAnswers] = useState<Set<number>>(new Set());
  const [expandedExplanations, setExpandedExplanations] = useState<Set<number>>(new Set());
  const [expandedSolutions, setExpandedSolutions] = useState<Set<number>>(new Set());
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    if (id) loadLab();
  }, [id, isAuthenticated, authLoading, router]);

  const loadLab = async () => {
    try {
      const data = await quickLabsApi.get(id as string);
      setLab(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load quick lab");
    } finally {
      setLoading(false);
    }
  };

  const toggleTask = (order: number) => {
    setCompletedTasks((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  };

  const toggleHint = (order: number) => {
    setExpandedHints((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  };

  const toggleAnswer = (order: number) => {
    setExpandedAnswers((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  };

  const toggleExplanation = (order: number) => {
    setExpandedExplanations((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  };

  const toggleSolution = (order: number) => {
    setExpandedSolutions((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  };

  const copyCommand = async (cmd: string) => {
    try {
      await navigator.clipboard.writeText(cmd);
      setCopiedCmd(cmd);
      setTimeout(() => setCopiedCmd(null), 2000);
    } catch {
      // ignore
    }
  };

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    );
  }

  if (error || !lab) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-16">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
            Failed to load quick lab
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400 mb-6">{error || "Not found"}</p>
          <Link href="/labs" className="text-emerald-600 hover:underline">
            Back to Labs
          </Link>
        </div>
      </div>
    );
  }

  const progress = lab.tasks.length > 0 ? Math.round((completedTasks.size / lab.tasks.length) * 100) : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back link */}
      <Link href="/labs" className="inline-flex items-center gap-1.5 text-sm text-zinc-500 hover:text-emerald-600 transition-colors mb-6">
        <ArrowLeft className="h-4 w-4" weight="regular" />
        Back to Labs
      </Link>

      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <Badge variant="outline" className="text-xs font-mono">
            {lab.technology}
          </Badge>
          <Badge variant="secondary" className={`text-xs ${getDifficultyColor(lab.difficulty)}`}>
            {getDifficultyLabel(lab.difficulty)}
          </Badge>
          <Badge variant="outline" className="text-xs">
            {lab.level}
          </Badge>
          <span className="flex items-center gap-1 text-xs text-zinc-500 dark:text-zinc-400">
            <Clock className="h-3 w-3" weight="regular" />
            {lab.estimated_minutes}m
          </span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100 mb-2">
          {lab.title}
        </h1>
        <p className="text-zinc-500 dark:text-zinc-400 max-w-3xl">
          {lab.description}
        </p>

        {/* Progress bar */}
        {lab.tasks.length > 0 && (
          <div className="mt-4 flex items-center gap-3">
            <div className="flex-1 h-2 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-emerald-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ type: "spring", stiffness: 100, damping: 20 }}
              />
            </div>
            <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400 min-w-[3rem] text-right">
              {completedTasks.size}/{lab.tasks.length}
            </span>
          </div>
        )}
      </div>

      {/* Main layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left panel: Topology + Instructions */}
        <div className="lg:col-span-1 space-y-6">
          {/* Topology SVG */}
          {lab.topology_svg && (
            <div className="bento-card p-4">
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-3 flex items-center gap-2">
                <Network className="h-4 w-4 text-emerald-600" weight="regular" />
                Topology
              </h3>
              <div
                className="rounded-lg overflow-hidden bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800"
                dangerouslySetInnerHTML={{ __html: lab.topology_svg }}
              />
            </div>
          )}

          {/* PNETlab Instructions */}
          <div className="bento-card p-4">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-3 flex items-center gap-2">
              <Lightning className="h-4 w-4 text-amber-500" weight="regular" />
              PNETlab Setup
            </h3>
            <div className="prose prose-sm dark:prose-invert prose-zinc max-w-none">
              <div
                className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed"
                dangerouslySetInnerHTML={{
                  __html: lab.pnetlab_instructions
                    .replace(/\n/g, "<br/>")
                    .replace(/## (.*)/g, '<h4 class="text-sm font-semibold mt-3 mb-1">$1</h4>')
                    .replace(/^(\d+)\.\s(.*)/gm, '<p class="mb-1"><span class="font-medium">$1.</span> $2</p>'),
                }}
              />
            </div>
          </div>

          {/* Prerequisite topics */}
          {lab.prerequisite_topics && lab.prerequisite_topics.length > 0 && (
            <div className="bento-card p-4">
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                Prerequisites
              </h3>
              <div className="flex flex-wrap gap-1.5">
                {lab.prerequisite_topics.map((topic) => (
                  <span
                    key={topic}
                    className="px-2 py-0.5 rounded-md text-xs bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right panel: Tabs with content */}
        <div className="lg:col-span-2">
          {/* Tab bar */}
          <div className="flex items-center gap-1 mb-6 border-b border-zinc-200 dark:border-zinc-800 overflow-x-auto">
            {tabs.map((tab) => {
              const count =
                tab.key === "tasks" ? lab.tasks.length :
                tab.key === "hints" ? lab.hints.length :
                tab.key === "answers" ? lab.answers.length :
                tab.key === "explanations" ? lab.explanations.length :
                tab.key === "solutions" ? lab.solution_commands.length : 0;
              const Icon = tab.icon;
              return (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`flex items-center gap-1.5 px-3 py-2.5 text-xs font-medium border-b-2 transition-all whitespace-nowrap ${
                    activeTab === tab.key
                      ? "border-emerald-500 text-emerald-600 dark:text-emerald-400"
                      : "border-transparent text-zinc-500 dark:text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-300"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" weight="regular" />
                  {tab.label}
                  {count > 0 && (
                    <span className="ml-0.5 px-1.5 py-0.5 rounded-full text-[10px] bg-zinc-100 dark:bg-zinc-800 text-zinc-500">
                      {count}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Tab content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.2 }}
            >
              {/* Tasks Tab */}
              {activeTab === "tasks" && (
                <div className="space-y-3">
                  {lab.tasks.map((task) => {
                    const isDone = completedTasks.has(task.order);
                    return (
                      <div
                        key={task.order}
                        className={`bento-card p-4 transition-all ${
                          isDone ? "border-emerald-200 dark:border-emerald-900/30 bg-emerald-50/30 dark:bg-emerald-900/10" : ""
                        }`}
                      >
                        <div className="flex items-start gap-3">
                          <button
                            onClick={() => toggleTask(task.order)}
                            className={`mt-0.5 flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                              isDone
                                ? "bg-emerald-500 border-emerald-500"
                                : "border-zinc-300 dark:border-zinc-600 hover:border-emerald-400"
                            }`}
                          >
                            {isDone && <CheckCircle className="h-3.5 w-3.5 text-white" weight="fill" />}
                          </button>
                          <div className="flex-1 min-w-0">
                            <h4 className={`text-sm font-semibold mb-1 ${isDone ? "line-through text-zinc-400 dark:text-zinc-600" : "text-zinc-900 dark:text-zinc-100"}`}>
                              {task.order}. {task.title}
                            </h4>
                            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-2">
                              {task.description}
                            </p>
                            {task.verification_commands && task.verification_commands.length > 0 && (
                              <div className="mt-2">
                                <p className="text-xs font-medium text-zinc-400 dark:text-zinc-500 mb-1.5">
                                  Verification commands:
                                </p>
                                <div className="space-y-1.5">
                                  {task.verification_commands.map((cmd, i) => (
                                    <div
                                      key={i}
                                      className="flex items-center gap-2 px-2.5 py-1.5 rounded-md bg-zinc-900 dark:bg-zinc-950 border border-zinc-800"
                                    >
                                      <code className="text-xs font-mono text-emerald-400 flex-1 truncate">
                                        {cmd}
                                      </code>
                                      <button
                                        onClick={() => copyCommand(cmd)}
                                        className="flex-shrink-0 text-zinc-500 hover:text-emerald-400 transition-colors"
                                        title="Copy"
                                      >
                                        {copiedCmd === cmd ? (
                                          <Check className="h-3 w-3" weight="bold" />
                                        ) : (
                                          <Copy className="h-3 w-3" weight="regular" />
                                        )}
                                      </button>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                            {task.expected_output_summary && (
                              <div className="mt-2 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-800">
                                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                                  <span className="font-medium text-zinc-700 dark:text-zinc-300">Expected:</span>{" "}
                                  {task.expected_output_summary}
                                </p>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Hints Tab */}
              {activeTab === "hints" && (
                <div className="space-y-3">
                  {lab.hints.map((hint) => {
                    const isOpen = expandedHints.has(hint.order);
                    return (
                      <div key={hint.order} className="bento-card p-0 overflow-hidden">
                        <button
                          onClick={() => toggleHint(hint.order)}
                          className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                        >
                          <span className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                            {hint.title}
                          </span>
                          <CaretDown
                            className={`h-4 w-4 text-zinc-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                            weight="regular"
                          />
                        </button>
                        <AnimatePresence>
                          {isOpen && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="overflow-hidden"
                            >
                              <div className="px-4 pb-4 text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                                {hint.content}
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Answers Tab */}
              {activeTab === "answers" && (
                <div className="space-y-3">
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">
                    Reveal answers only after attempting the task yourself.
                  </p>
                  {lab.answers.map((answer) => {
                    const isOpen = expandedAnswers.has(answer.order);
                    const task = lab.tasks.find((t) => t.order === answer.task_order);
                    return (
                      <div key={answer.order} className="bento-card p-0 overflow-hidden">
                        <button
                          onClick={() => toggleAnswer(answer.order)}
                          className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                        >
                          <span className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                            Answer for Task {answer.task_order}{task ? `: ${task.title}` : ""}
                          </span>
                          <CaretDown
                            className={`h-4 w-4 text-zinc-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                            weight="regular"
                          />
                        </button>
                        <AnimatePresence>
                          {isOpen && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="overflow-hidden"
                            >
                              <div className="px-4 pb-4">
                                <div className="flex items-start gap-2 px-3 py-2.5 rounded-lg bg-zinc-900 dark:bg-zinc-950 border border-zinc-800">
                                  <code className="text-sm font-mono text-emerald-400 flex-1 whitespace-pre-wrap">
                                    {answer.content}
                                  </code>
                                  <button
                                    onClick={() => copyCommand(answer.content)}
                                    className="flex-shrink-0 text-zinc-500 hover:text-emerald-400 transition-colors mt-0.5"
                                  >
                                    {copiedCmd === answer.content ? (
                                      <Check className="h-3.5 w-3.5" weight="bold" />
                                    ) : (
                                      <Copy className="h-3.5 w-3.5" weight="regular" />
                                    )}
                                  </button>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Explanations Tab */}
              {activeTab === "explanations" && (
                <div className="space-y-3">
                  {lab.explanations.map((exp) => {
                    const isOpen = expandedExplanations.has(exp.order);
                    return (
                      <div key={exp.order} className="bento-card p-0 overflow-hidden">
                        <button
                          onClick={() => toggleExplanation(exp.order)}
                          className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                        >
                          <span className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                            {exp.title}
                          </span>
                          <CaretDown
                            className={`h-4 w-4 text-zinc-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                            weight="regular"
                          />
                        </button>
                        <AnimatePresence>
                          {isOpen && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="overflow-hidden"
                            >
                              <div className="px-4 pb-4 text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                                {exp.content}
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Solutions Tab */}
              {activeTab === "solutions" && (
                <div className="space-y-3">
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">
                    Step-by-step solution commands. Run these on your PNETlab devices.
                  </p>
                  {lab.solution_commands.map((sol) => {
                    const isOpen = expandedSolutions.has(sol.order);
                    const task = lab.tasks.find((t) => t.order === sol.task_order);
                    return (
                      <div key={sol.order} className="bento-card p-0 overflow-hidden">
                        <button
                          onClick={() => toggleSolution(sol.order)}
                          className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
                        >
                          <span className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                            Solution for Task {sol.task_order}{task ? `: ${task.title}` : ""}
                          </span>
                          <CaretDown
                            className={`h-4 w-4 text-zinc-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                            weight="regular"
                          />
                        </button>
                        <AnimatePresence>
                          {isOpen && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.2 }}
                              className="overflow-hidden"
                            >
                              <div className="px-4 pb-4 space-y-2">
                                {sol.commands.map((cmd, i) => (
                                  <div
                                    key={i}
                                    className="flex items-center gap-2 px-3 py-2 rounded-md bg-zinc-900 dark:bg-zinc-950 border border-zinc-800"
                                  >
                                    <span className="text-xs text-zinc-600 dark:text-zinc-500 font-mono select-none">
                                      {i + 1}
                                    </span>
                                    <code className="text-sm font-mono text-emerald-400 flex-1 whitespace-pre-wrap">
                                      {cmd}
                                    </code>
                                    <button
                                      onClick={() => copyCommand(cmd)}
                                      className="flex-shrink-0 text-zinc-500 hover:text-emerald-400 transition-colors"
                                    >
                                      {copiedCmd === cmd ? (
                                        <Check className="h-3.5 w-3.5" weight="bold" />
                                      ) : (
                                        <Copy className="h-3.5 w-3.5" weight="regular" />
                                      )}
                                    </button>
                                  </div>
                                ))}
                                {sol.expected_output && (
                                  <div className="mt-2 px-3 py-2 rounded-lg bg-zinc-50 dark:bg-zinc-900/50 border border-zinc-200 dark:border-zinc-800">
                                    <p className="text-xs text-zinc-500 dark:text-zinc-400">
                                      <span className="font-medium text-zinc-700 dark:text-zinc-300">Expected output:</span>{" "}
                                      {sol.expected_output}
                                    </p>
                                  </div>
                                )}
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
