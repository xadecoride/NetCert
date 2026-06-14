"use client";

import { useEffect, useMemo, useRef, useState, Suspense } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  Lightning,
  Clock,
  ListChecks,
  Network,
  CaretDown,
  Terminal,
  CheckCircle,
  Circle,
  Spinner,
  Warning,
  Play,
  Code,
  BookOpen,
  Check,
} from "@phosphor-icons/react";

import { withAuth } from "@/lib/with-auth";
import { useTranslation } from "@/lib/i18n/context";
import { quickLabsApi } from "@/lib/api";
import { springTransition, fadeInUp } from "@/lib/motion";

import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BentoCard } from "@/components/ui/card";
import { SectionReveal } from "@/components/motion/SectionReveal";
import { AnimatedCounter } from "@/components/motion/AnimatedCounter";

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

interface QuickLabSolutionCommand {
  order: number;
  task_order: number;
  commands: string[];
  expected_output?: string;
}

interface QuickLab {
  id: string;
  title: string;
  description: string;
  level: string;
  technology: string;
  difficulty: number;
  estimated_minutes: number;
  topology_svg?: string;
  pnetlab_instructions?: string;
  tasks?: QuickLabTask[];
  hints?: QuickLabHint[];
  solution_commands?: QuickLabSolutionCommand[];
  prerequisite_topics?: string[];
}

const difficultyLabels = ["", "Beginner", "Easy", "Medium", "Hard", "Expert"];

function getDifficultyVariant(d: number) {
  if (d <= 2) return "success";
  if (d === 3) return "warning";
  return "danger";
}

function progressKey(labId: string) {
  return `netcert-quicklab-${labId}`;
}

function TopologyPlaceholder() {
  return (
    <div className="w-full aspect-video rounded-xl bg-zinc-100 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center relative overflow-hidden">
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

function TaskCard({
  task,
  hint,
  solution,
  completed,
  onToggle,
}: {
  task: QuickLabTask;
  hint?: QuickLabHint;
  solution?: QuickLabSolutionCommand;
  completed: boolean;
  onToggle: () => void;
}) {
  const { t } = useTranslation();
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  return (
    <BentoCard className={completed ? "border-emerald-200 dark:border-emerald-900/30" : ""}>
      <div className="flex items-start gap-4">
        <button
          onClick={onToggle}
          className="flex-shrink-0 w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-semibold text-sm hover:bg-emerald-200 dark:hover:bg-emerald-900/30 transition-colors"
          aria-label={completed ? t("quickLab.markIncomplete") : t("quickLab.markComplete")}
        >
          {completed ? (
            <CheckCircle className="h-5 w-5" weight="fill" />
          ) : (
            <Circle className="h-5 w-5" weight="regular" />
          )}
        </button>
        <div className="flex-1 min-w-0">
          <h3 className={`font-semibold text-zinc-900 dark:text-zinc-100 mb-1 ${completed ? "line-through text-zinc-500 dark:text-zinc-400" : ""}`}>
            {task.title}
          </h3>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">{task.description}</p>

          {task.verification_commands && task.verification_commands.length > 0 && (
            <div className="mb-4">
              <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1.5 flex items-center gap-1.5">
                <Terminal className="h-3.5 w-3.5" weight="fill" />
                {t("quickLab.verificationCommands")}
              </p>
              <div className="bg-zinc-900 rounded-xl p-3 overflow-x-auto">
                <code className="text-zinc-300 font-mono text-xs whitespace-pre">
                  {task.verification_commands.join("\n")}
                </code>
              </div>
            </div>
          )}

          {task.expected_output_summary && (
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-4">
              {t("quickLab.expectedOutput")}: {task.expected_output_summary}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-2">
            {hint && (
              <Button variant="outline" size="sm" onClick={() => setShowHint((v) => !v)}>
                <BookOpen className="h-3.5 w-3.5 mr-1.5" weight="regular" />
                {showHint ? t("quickLab.hideHint") : t("quickLab.showHint")}
              </Button>
            )}
            {solution && (
              <Button variant="secondary" size="sm" onClick={() => setShowSolution((v) => !v)}>
                <Code className="h-3.5 w-3.5 mr-1.5" weight="regular" />
                {showSolution ? t("quickLab.hideSolution") : t("quickLab.showSolution")}
              </Button>
            )}
          </div>

          <AnimatePresence>
            {showHint && hint && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={springTransition}
                className="overflow-hidden"
              >
                <div className="mt-4 p-4 rounded-xl bg-sky-50 dark:bg-sky-900/10 border border-sky-200 dark:border-sky-900/30">
                  <p className="text-sm font-medium text-sky-800 dark:text-sky-300 mb-1">{hint.title}</p>
                  <p className="text-sm text-sky-700 dark:text-sky-200 whitespace-pre-wrap">{hint.content}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {showSolution && solution && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={springTransition}
                className="overflow-hidden"
              >
                <div className="mt-4 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-900/10 border border-emerald-200 dark:border-emerald-900/30">
                  <p className="text-xs font-medium text-emerald-800 dark:text-emerald-300 mb-2">
                    {t("quickLab.solutionCommands")}
                  </p>
                  <div className="bg-zinc-900 rounded-xl p-3 overflow-x-auto mb-3">
                    <code className="text-zinc-300 font-mono text-xs whitespace-pre">
                      {solution.commands.join("\n")}
                    </code>
                  </div>
                  {solution.expected_output && (
                    <p className="text-xs text-emerald-700 dark:text-emerald-200">
                      {t("quickLab.expectedOutput")}: {solution.expected_output}
                    </p>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </BentoCard>
  );
}

function LabDetailPageContent() {
  const { t } = useTranslation();
  const params = useParams();
  const router = useRouter();
  const labId = params.id as string;

  const [lab, setLab] = useState<QuickLab | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [started, setStarted] = useState(false);
  const [completedTasks, setCompletedTasks] = useState<Set<number>>(new Set());
  const tasksRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!labId) return;
    quickLabsApi
      .get(labId)
      .then((data) => {
        setLab(data);
        try {
          const saved = localStorage.getItem(progressKey(labId));
          if (saved) {
            const parsed = JSON.parse(saved);
            setCompletedTasks(new Set((parsed.completedTasks || []).map(Number)));
            if (parsed.started) setStarted(true);
          }
        } catch {}
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load lab"))
      .finally(() => setLoading(false));
  }, [labId]);

  useEffect(() => {
    if (!labId) return;
    localStorage.setItem(
      progressKey(labId),
      JSON.stringify({ started, completedTasks: Array.from(completedTasks) })
    );
  }, [started, completedTasks, labId]);

  const tasks = lab?.tasks || [];
  const hintsByOrder = useMemo(() => new Map((lab?.hints || []).map((h) => [h.order, h])), [lab?.hints]);
  const solutionsByTask = useMemo(
    () => new Map((lab?.solution_commands || []).map((s) => [s.task_order, s])),
    [lab?.solution_commands]
  );

  const progress = tasks.length ? Math.round((completedTasks.size / tasks.length) * 100) : 0;
  const allCompleted = tasks.length > 0 && completedTasks.size === tasks.length;

  const handleStart = () => {
    setStarted(true);
    setTimeout(() => tasksRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
  };

  const toggleTask = (order: number) => {
    setCompletedTasks((prev) => {
      const next = new Set(prev);
      if (next.has(order)) next.delete(order);
      else next.add(order);
      return next;
    });
  };

  if (loading) {
    return (
      <PageShell className="min-h-[100dvh] flex items-center justify-center">
        <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
      </PageShell>
    );
  }

  if (error || !lab) {
    return (
      <PageShell className="min-h-[100dvh]">
        <div className="text-center py-24">
          <Warning className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">{t("labs.noLabs")}</h2>
          <p className="text-zinc-500 dark:text-zinc-400 mb-6">{error || t("labs.noLabsDesc")}</p>
          <div className="flex items-center justify-center gap-3">
            <Link href="/labs">
              <Button variant="outline">{t("review.backToExams")}</Button>
            </Link>
            <Button onClick={() => window.location.reload()}>{t("common.retry")}</Button>
          </div>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell className="min-h-[100dvh]">
      <motion.div variants={fadeInUp}>
        <Link
          href="/labs"
          className="inline-flex items-center gap-1.5 text-sm text-zinc-500 hover:text-emerald-600 transition-colors mb-6"
        >
          <ArrowLeft className="h-4 w-4" weight="regular" />
          {t("exam.backToExams")}
        </Link>
      </motion.div>

      <PageHeader
        badge={
          <Badge variant="secondary">
            <Lightning className="h-3 w-3 mr-1" weight="fill" />
            {lab.technology}
          </Badge>
        }
        title={lab.title}
        subtitle={lab.description}
      />

      <SectionReveal>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2 space-y-6">
            <BentoCard>
              <div className="flex flex-wrap items-center gap-2 mb-6">
                <Badge variant="outline">{lab.level}</Badge>
                <Badge variant={getDifficultyVariant(lab.difficulty)}>
                  {difficultyLabels[lab.difficulty] || "Unknown"}
                </Badge>
                <span className="flex items-center gap-1.5 text-sm text-zinc-500 dark:text-zinc-400 ml-auto">
                  <Clock className="h-3.5 w-3.5" weight="regular" />
                  {lab.estimated_minutes || 0}m
                </span>
              </div>

              {lab.prerequisite_topics && lab.prerequisite_topics.length > 0 && (
                <div className="mb-6">
                  <p className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-2">
                    {t("quickLab.prerequisites")}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {lab.prerequisite_topics.map((topic) => (
                      <Badge key={topic} variant="secondary" className="text-xs">
                        {topic}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {!started ? (
                <Button variant="primary" onClick={handleStart} size="lg">
                  <Play className="h-4 w-4 mr-2" weight="fill" />
                  {t("labs.start")}
                </Button>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-zinc-500 dark:text-zinc-400">{t("quickLab.progress")}</span>
                    <span className="font-semibold text-emerald-600 dark:text-emerald-400">
                      <AnimatedCounter value={progress} suffix="%" />
                    </span>
                  </div>
                  <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-emerald-500 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${progress}%` }}
                      transition={springTransition}
                    />
                  </div>
                  {allCompleted && (
                    <div className="flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400">
                      <Check className="h-4 w-4" weight="bold" />
                      {t("quickLab.allTasksCompleted")}
                    </div>
                  )}
                </div>
              )}
            </BentoCard>

            <div ref={tasksRef} className="flex items-center justify-between mb-2">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white flex items-center gap-2">
                <ListChecks className="h-5 w-5 text-emerald-500" weight="fill" />
                {t("quickLab.tasks")} ({tasks.length})
              </h2>
            </div>

            <div className="space-y-4">
              {!started ? (
                <BentoCard className="text-center py-12">
                  <Play className="h-10 w-10 mx-auto mb-3 text-zinc-300 dark:text-zinc-600" weight="fill" />
                  <p className="text-zinc-500 dark:text-zinc-400 mb-4">{t("quickLab.startPrompt")}</p>
                  <Button variant="primary" onClick={handleStart}>
                    <Play className="h-4 w-4 mr-2" weight="fill" />
                    {t("labs.start")}
                  </Button>
                </BentoCard>
              ) : tasks.length === 0 ? (
                <BentoCard className="text-center py-12">
                  <ListChecks className="h-10 w-10 mx-auto mb-3 text-zinc-300 dark:text-zinc-600" weight="light" />
                  <p className="text-zinc-500 dark:text-zinc-400">{t("quickLab.noTasks")}</p>
                </BentoCard>
              ) : (
                tasks.map((task) => (
                  <TaskCard
                    key={task.order}
                    task={task}
                    hint={hintsByOrder.get(task.order)}
                    solution={solutionsByTask.get(task.order)}
                    completed={completedTasks.has(task.order)}
                    onToggle={() => toggleTask(task.order)}
                  />
                ))
              )}
            </div>
          </div>

          <div className="space-y-6">
            <BentoCard>
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-4">
                {t("quickLab.topology")}
              </h3>
              {lab.topology_svg ? (
                <div
                  className="w-full aspect-video rounded-xl overflow-hidden bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800"
                  dangerouslySetInnerHTML={{ __html: lab.topology_svg }}
                />
              ) : (
                <TopologyPlaceholder />
              )}
            </BentoCard>

            {lab.pnetlab_instructions && (
              <BentoCard>
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-2">
                  {t("quickLab.pnetlabInstructions")}
                </h3>
                <p className="text-sm text-zinc-500 dark:text-zinc-400 whitespace-pre-wrap">
                  {lab.pnetlab_instructions}
                </p>
              </BentoCard>
            )}

            <BentoCard className="p-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 mb-2">
                {t("quickLab.labInfo")}
              </h3>
              <div className="space-y-1 text-xs text-zinc-600 dark:text-zinc-400">
                <p>
                  {t("quickLab.level")}: <span className="text-zinc-900 dark:text-zinc-100">{lab.level}</span>
                </p>
                <p>
                  {t("quickLab.difficulty")}: <span className="text-zinc-900 dark:text-zinc-100">{difficultyLabels[lab.difficulty]}</span>
                </p>
                <p>
                  {t("quickLab.technology")}: <span className="text-zinc-900 dark:text-zinc-100">{lab.technology}</span>
                </p>
                <p>
                  {t("quickLab.estimatedTime")}: <span className="text-zinc-900 dark:text-zinc-100">{lab.estimated_minutes} min</span>
                </p>
              </div>
            </BentoCard>
          </div>
        </div>
      </SectionReveal>
    </PageShell>
  );
}

function LabDetailPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
        </div>
      }
    >
      <LabDetailPageContent />
    </Suspense>
  );
}

export default withAuth(LabDetailPage);
