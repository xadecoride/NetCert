"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  Warning,
  Clock,
  Calendar,
  CaretDown,
  Spinner,
  ArrowSquareOut,
  BookOpen,
} from "@phosphor-icons/react";

import { withAuth } from "@/lib/with-auth";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi } from "@/lib/api";
import { springTransition, fadeInUp } from "@/lib/motion";

import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BentoCard } from "@/components/ui/card";
import { SectionReveal } from "@/components/motion/SectionReveal";
import { AnimatedCounter } from "@/components/motion/AnimatedCounter";

function formatDate(locale: string, iso: string) {
  return new Date(iso).toLocaleDateString(locale === "ru" ? "ru-RU" : "en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatDuration(seconds: number) {
  const m = Math.floor((seconds || 0) / 60);
  const s = (seconds || 0) % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

interface ReviewQuestion {
  id: string;
  body: string;
  options?: { id: string; text: string; is_correct?: boolean }[];
  question_type: string;
  difficulty: number;
  explanation?: string;
  reference_urls?: string[];
  user_answer: string;
  is_correct?: boolean;
  was_flagged: boolean;
  time_spent_seconds: number;
}

function QuestionReviewCard({ q, index, locale }: { q: ReviewQuestion; index: number; locale: string }) {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(true);

  const userAnswerIds = useMemo(() => {
    if (!q.user_answer) return [];
    return q.question_type === "multiple-choice" ? q.user_answer.split(",") : [q.user_answer];
  }, [q.user_answer, q.question_type]);

  const correctOptionIds = useMemo(() => {
    return (q.options || []).filter((o) => o.is_correct).map((o) => o.id);
  }, [q.options]);

  return (
    <BentoCard className={q.is_correct === true ? "border-emerald-200 dark:border-emerald-900/30" : q.is_correct === false ? "border-red-200 dark:border-red-900/30" : ""}>
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-start justify-between gap-4 text-left"
      >
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="outline" className="text-xs">
              {t("exam.question")} {index + 1}
            </Badge>
            {q.is_correct === true ? (
              <Badge variant="success" className="text-xs">
                <CheckCircle className="h-3 w-3 mr-1" weight="fill" />
                {t("review.correct")}
              </Badge>
            ) : q.is_correct === false ? (
              <Badge variant="danger" className="text-xs">
                <XCircle className="h-3 w-3 mr-1" weight="fill" />
                {t("review.incorrect")}
              </Badge>
            ) : (
              <Badge variant="warning" className="text-xs">
                <Warning className="h-3 w-3 mr-1" weight="fill" />
                {t("review.unanswered")}
              </Badge>
            )}
            {q.was_flagged && (
              <Badge variant="outline" className="text-amber-600 border-amber-500/30 text-xs">
                {t("exam.flagged")}
              </Badge>
            )}
          </div>
          <p className="text-zinc-900 dark:text-zinc-100 font-medium whitespace-pre-wrap">{q.body}</p>
        </div>
        <CaretDown
          className={`h-5 w-5 text-zinc-400 transition-transform shrink-0 ${expanded ? "rotate-180" : ""}`}
          weight="bold"
        />
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={springTransition}
            className="overflow-hidden"
          >
            <div className="pt-4 mt-4 border-t border-zinc-200 dark:border-zinc-800 space-y-4">
              {q.question_type !== "fill-blank" && q.options && q.options.length > 0 ? (
                <div className="space-y-2">
                  {q.options.map((opt) => {
                    const selected = userAnswerIds.includes(opt.id);
                    const isCorrect = opt.is_correct;
                    return (
                      <div
                        key={opt.id}
                        className={`flex items-center gap-3 p-3 rounded-xl border text-sm ${
                          isCorrect
                            ? "bg-emerald-50 dark:bg-emerald-900/10 border-emerald-200 dark:border-emerald-900/30 text-emerald-700 dark:text-emerald-300"
                            : selected
                            ? "bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-900/30 text-red-700 dark:text-red-300"
                            : "bg-zinc-50 dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400"
                        }`}
                      >
                        <div
                          className={`w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 ${
                            isCorrect
                              ? "border-emerald-500 bg-emerald-500"
                              : selected
                              ? "border-red-500 bg-red-500"
                              : "border-zinc-400"
                          }`}
                        >
                          {isCorrect ? (
                            <CheckCircle className="h-3 w-3 text-white" weight="fill" />
                          ) : selected ? (
                            <XCircle className="h-3 w-3 text-white" weight="fill" />
                          ) : null}
                        </div>
                        <span className="flex-1">{opt.text}</span>
                        {selected && (
                          <span className="text-xs font-medium">
                            {t("review.yourAnswer")}
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="space-y-2">
                  <div className="p-3 rounded-xl bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800">
                    <p className="text-xs text-zinc-500 mb-1">{t("review.yourAnswer")}</p>
                    <p className="font-mono text-sm text-zinc-900 dark:text-zinc-100">
                      {q.user_answer || t("review.noAnswer")}
                    </p>
                  </div>
                </div>
              )}

              {q.explanation && (
                <div className="p-4 rounded-xl bg-sky-50 dark:bg-sky-900/10 border border-sky-200 dark:border-sky-900/30">
                  <p className="text-sm font-medium text-sky-800 dark:text-sky-300 mb-1 flex items-center gap-2">
                    <BookOpen className="h-4 w-4" weight="fill" />
                    {t("review.explanation")}
                  </p>
                  <p className="text-sm text-sky-700 dark:text-sky-200 whitespace-pre-wrap">{q.explanation}</p>
                </div>
              )}

              {q.reference_urls && q.reference_urls.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {q.reference_urls.map((url) => (
                    <a
                      key={url}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-emerald-600 hover:text-emerald-500"
                    >
                      {t("review.viewDocs")}
                      <ArrowSquareOut className="h-3 w-3" weight="bold" />
                    </a>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </BentoCard>
  );
}

function ReviewDetailPageContent() {
  const { t, locale } = useTranslation();
  const router = useRouter();
  const params = useParams();
  const attemptId = params.id as string;

  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!attemptId) return;
    attemptsApi
      .getDetails(attemptId)
      .then(setData)
      .catch((err) => setError(err instanceof Error ? err.message : String(err)))
      .finally(() => setLoading(false));
  }, [attemptId]);

  if (loading) {
    return (
      <PageShell className="min-h-[100dvh] flex items-center justify-center">
        <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
      </PageShell>
    );
  }

  if (error || !data) {
    return (
      <PageShell className="min-h-[100dvh]">
        <div className="text-center py-24">
          <Warning className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
            {t("review.notFound")}
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400 mb-6">{error || t("review.notFoundDesc")}</p>
          <div className="flex items-center justify-center gap-3">
            <Link href="/review">
              <Button variant="outline">{t("review.backToExams")}</Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="primary">{t("review.viewDashboard")}</Button>
            </Link>
          </div>
        </div>
      </PageShell>
    );
  }

  const attempt = data;
  const questions: ReviewQuestion[] = attempt.questions || [];
  const rawScore = Number.isFinite(attempt.score) ? attempt.score : 0;
  const score = Math.round(rawScore);
  const passingScore = Number.isFinite(attempt.passing_score) ? attempt.passing_score : 70;
  const passed = rawScore >= passingScore;

  return (
    <PageShell className="min-h-[100dvh]">
      <motion.div variants={fadeInUp}>
        <Link
          href="/review"
          className="inline-flex items-center gap-1.5 text-sm text-zinc-500 hover:text-emerald-600 transition-colors mb-6"
        >
          <ArrowLeft className="h-4 w-4" weight="regular" />
          {t("review.backToExams")}
        </Link>
      </motion.div>

      <PageHeader
        badge={
          <Badge variant={passed ? "success" : "danger"}>
            {passed ? t("review.passed") : t("review.failed")}
          </Badge>
        }
        title={attempt.exam_name || `${t("exam.examLabel")} ${attempt.exam_id?.slice(0, 8)}`}
        subtitle={formatDate(locale, attempt.started_at)}
      />

      <SectionReveal>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <BentoCard className="text-center">
            <p className="text-3xl font-bold text-zinc-900 dark:text-white">
              <AnimatedCounter value={score} suffix="%" />
            </p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">{t("exam.toPass")?.replace(" to pass", "")}</p>
          </BentoCard>
          <BentoCard className="text-center">
            <p className="text-3xl font-bold text-zinc-900 dark:text-white">
              <AnimatedCounter value={attempt.questions_correct || 0} />
            </p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">{t("review.correct")}</p>
          </BentoCard>
          <BentoCard className="text-center">
            <p className="text-3xl font-bold text-zinc-900 dark:text-white">
              <AnimatedCounter value={attempt.questions_answered || 0} />
            </p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">{t("review.answered")}</p>
          </BentoCard>
          <BentoCard className="text-center">
            <p className="text-3xl font-bold text-zinc-900 dark:text-white">
              {formatDuration(attempt.duration_seconds)}
            </p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">{t("review.duration")}</p>
          </BentoCard>
        </div>
      </SectionReveal>

      <SectionReveal>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
            {t("review.questionReview")}
          </h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            {questions.length} {t("exam.questions")}
          </p>
        </div>
      </SectionReveal>

      <div className="space-y-4">
        {questions.map((q, idx) => (
          <SectionReveal key={q.id} delay={idx * 0.02}>
            <QuestionReviewCard q={q} index={idx} locale={locale} />
          </SectionReveal>
        ))}
      </div>

      <SectionReveal className="mt-10 flex flex-wrap items-center gap-3">
        <Link href="/exams">
          <Button variant="primary">
            {t("review.takeAnother")}
            <ArrowLeft className="h-4 w-4 ml-2 rotate-180" weight="regular" />
          </Button>
        </Link>
        <Link href="/dashboard">
          <Button variant="outline">{t("review.viewDashboard")}</Button>
        </Link>
      </SectionReveal>
    </PageShell>
  );
}

function ReviewDetailPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
        </div>
      }
    >
      <ReviewDetailPageContent />
    </Suspense>
  );
}

export default withAuth(ReviewDetailPage);
