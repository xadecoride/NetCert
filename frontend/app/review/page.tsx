"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Exam,
  CheckCircle,
  XCircle,
  Clock,
  Calendar,
  CaretRight,
  Spinner,
  Warning,
  ArrowRight,
} from "@phosphor-icons/react";

import { withAuth } from "@/lib/with-auth";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi } from "@/lib/api";
import { springTransition, staggerContainer, fadeInUp } from "@/lib/motion";

import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BentoCard } from "@/components/ui/card";
import { SpotlightCard } from "@/components/motion/SpotlightCard";
import { SectionReveal } from "@/components/motion/SectionReveal";
import { AnimatedCounter } from "@/components/motion/AnimatedCounter";

function formatDate(locale: string, iso: string) {
  return new Date(iso).toLocaleDateString(locale === "ru" ? "ru-RU" : "en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function formatDuration(seconds: number) {
  const m = Math.floor((seconds || 0) / 60);
  const s = (seconds || 0) % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function ReviewListPageContent() {
  const { t, locale } = useTranslation();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    attemptsApi
      .history()
      .then((h) => setHistory(h || []))
      .catch((err) => setError(err instanceof Error ? err.message : String(err)))
      .finally(() => setLoading(false));
  }, []);

  const stats = useMemo(() => {
    const total = history.length;
    const completed = history.filter((a) => a.status === "completed" || a.completed_at).length;
    const scored = history.filter((a) => Number.isFinite(a.score));
    const passed = scored.filter((a) => a.score >= (a.passing_score || 70)).length;
    const avg =
      scored.length > 0
        ? Math.round(
            scored.reduce((sum, a) => sum + (Number.isFinite(a.score) ? a.score : 0), 0) /
              scored.length
          )
        : 0;
    return { total, completed, passed, avg };
  }, [history]);

  return (
    <PageShell className="min-h-[100dvh]">
      <PageHeader
        badge={
          <Badge variant="secondary">
            <Exam className="h-3 w-3 mr-1" weight="fill" />
            {t("review.badge")}
          </Badge>
        }
        title={t("review.title")}
        subtitle="Review your past exam attempts, see what you missed, and track improvement."
      />

      {error && (
        <SectionReveal className="mb-6 p-4 rounded-xl bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/30 text-red-600 dark:text-red-300 text-sm">
          {error}
        </SectionReveal>
      )}

      {!loading && (
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
        >
          {[
            { label: "Total attempts", value: stats.total, suffix: "" },
            { label: "Completed", value: stats.completed, suffix: "" },
            { label: "Passed", value: stats.passed, suffix: "" },
            { label: "Average score", value: stats.avg, suffix: "%" },
          ].map((s) => (
            <motion.div key={s.label} variants={fadeInUp}>
              <BentoCard className="text-center">
                <p className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
                  <AnimatedCounter value={s.value} suffix={s.suffix} />
                </p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">{s.label}</p>
              </BentoCard>
            </motion.div>
          ))}
        </motion.div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-24">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
        </div>
      ) : history.length === 0 ? (
        <SectionReveal className="text-center py-24">
          <div className="p-4 rounded-2xl bg-zinc-100 dark:bg-zinc-800 inline-flex mb-4">
            <Exam className="h-10 w-10 text-zinc-400" weight="light" />
          </div>
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-1">
            No attempts yet
          </h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6 max-w-xs mx-auto">
            Complete your first exam to see a detailed review here.
          </p>
          <Link href="/exams">
            <Button variant="primary">
              {t("exams.startExam")}
              <ArrowRight className="h-4 w-4 ml-2" weight="regular" />
            </Button>
          </Link>
        </SectionReveal>
      ) : (
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
        >
          <AnimatePresence mode="popLayout">
            {history.map((attempt) => {
              const rawScore = Number.isFinite(attempt.score) ? attempt.score : null;
              const passingScore = Number.isFinite(attempt.passing_score) ? attempt.passing_score : 70;
              const passed = rawScore != null && rawScore >= passingScore;
              const completed = attempt.status === "completed" || attempt.completed_at;
              return (
                <motion.div key={attempt.id} layout variants={fadeInUp} transition={springTransition}>
                  <Link href={`/review/${attempt.id}`}>
                    <SpotlightCard className="h-full group cursor-pointer">
                      <BentoCard className="h-full flex flex-col p-0 bg-transparent border-0 shadow-none">
                        <div className="p-6 flex flex-col h-full">
                          <div className="flex items-start justify-between gap-3 mb-4">
                            <div className="p-2.5 rounded-xl bg-emerald-100 dark:bg-emerald-900/20">
                              <Exam className="h-5 w-5 text-emerald-600 dark:text-emerald-400" weight="fill" />
                            </div>
                            <Badge variant={passed ? "success" : completed ? "danger" : "warning"}>
                              {completed ? (passed ? t("review.passed") : t("review.failed")) : attempt.status}
                            </Badge>
                          </div>

                          <h3 className="font-semibold text-lg text-zinc-900 dark:text-zinc-100 mb-1">
                            {attempt.exam_name || attempt.exam_id?.slice(0, 8)}
                          </h3>
                          <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-4">
                            {formatDate(locale, attempt.started_at)}
                          </p>

                          <div className="flex items-center gap-4 mt-auto pt-4 border-t border-zinc-200 dark:border-zinc-800 text-sm text-zinc-500 dark:text-zinc-400">
                            <span className="flex items-center gap-1.5">
                              {passed ? (
                                <CheckCircle className="h-4 w-4 text-emerald-500" weight="fill" />
                              ) : completed ? (
                                <XCircle className="h-4 w-4 text-red-500" weight="fill" />
                              ) : (
                                <Warning className="h-4 w-4 text-amber-500" weight="fill" />
                              )}
                              {rawScore != null ? `${Math.round(rawScore)}%` : "—"}
                            </span>
                            <span className="flex items-center gap-1.5">
                              <Clock className="h-3.5 w-3.5" weight="regular" />
                              {formatDuration(attempt.duration_seconds)}
                            </span>
                            <span className="flex items-center gap-1.5 ml-auto">
                              <Calendar className="h-3.5 w-3.5" weight="regular" />
                              {attempt.questions_answered}/{attempt.questions_total}
                            </span>
                          </div>

                          <div className="flex items-center text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0 mt-3">
                            {t("review.questionReview")}
                            <CaretRight className="h-4 w-4 ml-1" weight="regular" />
                          </div>
                        </div>
                      </BentoCard>
                    </SpotlightCard>
                  </Link>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      )}
    </PageShell>
  );
}

function ReviewListPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
        </div>
      }
    >
      <ReviewListPageContent />
    </Suspense>
  );
}

export default withAuth(ReviewListPage);
