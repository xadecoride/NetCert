"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi, explanationsApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
import ExplanationPanel from "@/components/ExplanationPanel";
import {
  CheckCircle,
  XCircle,
  ArrowLeft,
  BookOpen,
  Clock,
  ChartBar,
  TrendUp,
  CaretDown,
  CaretUp,
  Flag,
  ClockAfternoon,
} from "@phosphor-icons/react";

interface QuestionOption {
  id: string;
  text: string;
  is_correct?: boolean;
}

interface ReviewQuestion {
  id: string;
  body: string;
  options: QuestionOption[];
  question_type: string;
  difficulty: number;
  explanation: string;
  reference_urls: string[];
  blueprint_section: string;
  user_answer: string;
  is_correct: boolean | null;
  was_flagged: boolean;
  time_spent_seconds: number;
}

interface AttemptDetails {
  id: string;
  score: number;
  questions_total: number;
  questions_answered: number;
  questions_correct: number;
  started_at: string;
  completed_at: string;
  duration_seconds: number;
  mode: string;
  status: string;
  questions: ReviewQuestion[];
}

export default function ReviewPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const attemptId = params.id as string;

  const [attempt, setAttempt] = useState<AttemptDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set());
  const { t, locale } = useTranslation();

  // Telemetry batching for explanation interactions
  const telemetryBuffer = useRef<any[]>([]);
  const telemetryTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const reviewSessionIdRef = useRef(crypto.randomUUID()); // Stable session ID for entire review

  const flushTelemetry = useCallback(() => {
    if (telemetryBuffer.current.length === 0) return;
    const batch = [...telemetryBuffer.current];
    telemetryBuffer.current = [];
    explanationsApi.sendTelemetry(batch).catch((err) => {
      console.warn("Failed to flush explanation telemetry:", err);
    });
  }, []);

  const handleTelemetryEvent = useCallback((event: any) => {
    telemetryBuffer.current.push({
      ...event,
      session_id: reviewSessionIdRef.current,
    });
    // Flush every 30 seconds or when buffer > 50
    if (telemetryBuffer.current.length >= 50) {
      flushTelemetry();
    }
  }, [flushTelemetry]);

  // Periodic telemetry flush
  useEffect(() => {
    telemetryTimerRef.current = setInterval(flushTelemetry, 30000);
    return () => {
      if (telemetryTimerRef.current) clearInterval(telemetryTimerRef.current);
      // Flush remaining events on unmount
      flushTelemetry();
    };
  }, [flushTelemetry]);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    if (isAuthenticated && attemptId) {
      attemptsApi.getDetails(attemptId)
        .then((data) => {
          setAttempt(data);
          setLoading(false);
        })
        .catch(() => {
          // Fallback to basic attempt data if details endpoint fails
          attemptsApi.get(attemptId)
            .then((data) => {
              setAttempt(data);
              setLoading(false);
            })
            .catch(() => setLoading(false));
        });
    }
  }, [isAuthenticated, authLoading, attemptId, router]);

  const toggleQuestion = (qId: string) => {
    setExpandedQuestions((prev) => {
      const next = new Set(prev);
      if (next.has(qId)) next.delete(qId);
      else next.add(qId);
      return next;
    });
  };

  if (authLoading || loading) {
    return (
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    );
  }

  if (!attempt) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <BookOpen className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
        <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-white mb-4">{t("review.notFound")}</h1>
        <p className="text-zinc-500 dark:text-zinc-400 mb-8">{t("review.notFoundDesc")}</p>
        <Link href="/exams">
          <Button variant="primary">{t("review.backToExams")}</Button>
        </Link>
      </div>
    );
  }

  const score = attempt.score || 0;
  const passed = score >= 70;
  const duration = attempt.duration_seconds || 0;
  const minutes = Math.floor(duration / 60);
  const questions = attempt.questions || [];

  // If no questions array, show simple summary (fallback for legacy attempts)
  if (!questions.length) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.button
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          onClick={() => router.push("/dashboard")}
          className="flex items-center gap-2 text-sm text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 mb-6 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" weight="regular" />
          {t("review.backToDashboard")}
        </motion.button>
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold mb-2">{t("review.title")}</h2>
          <div className={`text-5xl font-bold font-mono mb-4 ${passed ? "text-emerald-500" : "text-red-500"}`}>
            {Math.round(score)}%
          </div>
          <Badge variant={passed ? "success" : "danger"}>{passed ? t("review.passed") : t("review.failed")}</Badge>
        </div>
      </div>
    );
  }

  const correctCount = questions.filter((q) => q.is_correct === true).length;
  const incorrectCount = questions.filter((q) => q.is_correct === false).length;
  const unansweredCount = questions.filter((q) => q.is_correct === null).length;

  // For multiple-choice, parse user answer into selected IDs
  const getSelectedOptionIds = (q: ReviewQuestion): string[] => {
    if (q.question_type === "multiple-choice" && q.user_answer) {
      return q.user_answer.split(",").map((s) => s.trim()).filter(Boolean);
    }
    return q.user_answer ? [q.user_answer] : [];
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back button */}
      <motion.button
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        onClick={() => router.push("/dashboard")}
        className="flex items-center gap-2 text-sm text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 mb-6 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" weight="regular" />
        {t("review.backToDashboard")}
      </motion.button>

      {/* Result header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8"
      >
        <div>
          <Badge variant="secondary" className="mb-3">{t("review.badge")}</Badge>
          <h1 className="text-3xl font-bold tracking-tighter text-zinc-900 dark:text-white">
            {t("review.title")}
          </h1>
          <p className="text-zinc-500 dark:text-zinc-400 mt-1">
            {new Date(attempt.started_at).toLocaleDateString(locale === "ru" ? "ru-RU" : "en-US", {
              weekday: "long",
              month: "long",
              day: "numeric",
              year: "numeric",
            })}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 150, damping: 15, delay: 0.2 }}
              className={`text-5xl font-bold tracking-tighter font-mono ${passed ? "text-emerald-500" : "text-red-500"}`}
            >
              {Math.round(score)}%
            </motion.div>
            <Badge variant={passed ? "success" : "danger"} className="mt-1">
              {passed ? t("review.passed") : t("review.failed")}
            </Badge>
          </div>
        </div>
      </motion.div>

      {/* Stats cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, type: "spring", stiffness: 100, damping: 20 }}
        className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8"
      >
        {[
          { icon: CheckCircle, label: t("review.correct"), value: `${correctCount}/${questions.length}`, color: "text-emerald-500" },
          { icon: XCircle, label: t("review.incorrect"), value: `${incorrectCount}/${questions.length}`, color: "text-red-500" },
          { icon: Clock, label: t("review.duration"), value: `${minutes}m`, color: "text-sky-500" },
          { icon: ChartBar, label: t("review.answered"), value: `${attempt.questions_answered || questions.length}/${questions.length}`, color: "text-violet-500" },
        ].map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label}>
              <CardContent className="p-4 text-center">
                <Icon className={`h-5 w-5 mx-auto mb-1 ${stat.color}`} weight="fill" />
                <p className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-white font-mono">{stat.value}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">{stat.label}</p>
              </CardContent>
            </Card>
          );
        })}
      </motion.div>

      {/* Per-question score breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15, type: "spring", stiffness: 100, damping: 20 }}
      >
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendUp className="h-5 w-5 text-emerald-600" weight="fill" />
              {t("review.scoreBreakdown")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-2">
              <div className="flex justify-between text-xs text-zinc-500 mb-1">
                <span>{t("review.correct")}: {correctCount}/{questions.length} ({questions.length > 0 ? Math.round(correctCount / questions.length * 100) : 0}%)</span>
                <span>{t("review.incorrect")}: {incorrectCount}/{questions.length} ({questions.length > 0 ? Math.round(incorrectCount / questions.length * 100) : 0}%)</span>
                {unansweredCount > 0 && (
                  <span>{t("review.unanswered")}: {unansweredCount}/{questions.length} ({Math.round(unansweredCount / questions.length * 100)}%)</span>
                )}
              </div>
              {/* Progress bar */}
              <div className="w-full h-2 rounded-full bg-zinc-200 dark:bg-zinc-700 overflow-hidden flex">
                {correctCount > 0 && (
                  <div
                    className="h-full bg-emerald-500 transition-all duration-700"
                    style={{ width: `${(correctCount / questions.length) * 100}%` }}
                  />
                )}
                {incorrectCount > 0 && (
                  <div
                    className="h-full bg-red-500 transition-all duration-700"
                    style={{ width: `${(incorrectCount / questions.length) * 100}%` }}
                  />
                )}
                {unansweredCount > 0 && (
                  <div
                    className="h-full bg-zinc-400 dark:bg-zinc-500 transition-all duration-700"
                    style={{ width: `${(unansweredCount / questions.length) * 100}%` }}
                  />
                )}
              </div>
            </div>
            {/* Per-question bar chart */}
            <div className="flex items-end gap-[1px] h-24 mt-4">
              {questions.map((q, i) => {
                const isQCorrect = q.is_correct === true;
                const isQIncorrect = q.is_correct === false;
                const isQUnanswered = q.is_correct === null;
                let bgColor: string;
                if (isQCorrect) {
                  bgColor = "rgb(16, 185, 129)";
                } else if (isQIncorrect) {
                  bgColor = "rgb(239, 68, 68)";
                } else {
                  bgColor = "rgb(161, 161, 170)";
                }
                return (
                  <div
                    key={q.id || i}
                    className="flex-1 min-w-[2px] rounded-t transition-all duration-300 hover:opacity-80 relative group"
                    style={{
                      height: isQCorrect ? "100%" : "35%",
                      backgroundColor: bgColor,
                      opacity: isQUnanswered ? 0.5 : 0.85,
                    }}
                    title={`Q${i+1}: ${isQCorrect ? '✓ Correct' : isQIncorrect ? '✗ Incorrect' : '— Unanswered'}`}
                  >
                    {/* Tooltip on hover */}
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 text-[10px] px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10">
                      Q{i+1}: {isQCorrect ? '✓' : isQIncorrect ? '✗' : '—'}
                    </div>
                  </div>
                );
              })}
            </div>
            <div className="flex justify-between mt-1 text-[10px] text-zinc-400">
              <span>{t("exam.question")} 1</span>
              <span>{t("exam.question")} {questions.length}</span>
            </div>
            {/* Legend */}
            <div className="flex items-center gap-4 mt-3 pt-3 border-t border-zinc-100 dark:border-zinc-800">
              <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                <div className="w-2.5 h-2.5 rounded-sm bg-emerald-500" />
                <span>{t("review.correct")}</span>
              </div>
              <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                <div className="w-2.5 h-2.5 rounded-sm bg-red-500" />
                <span>{t("review.incorrect")}</span>
              </div>
              {unansweredCount > 0 && (
                <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                  <div className="w-2.5 h-2.5 rounded-sm bg-zinc-400" />
                  <span>{t("review.unanswered")}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, type: "spring", stiffness: 100, damping: 20 }}
        className="flex flex-col sm:flex-row gap-3 mb-8"
      >
        <Link href="/exams">
          <Button variant="primary">
            <BookOpen className="h-4 w-4 mr-2" weight="regular" />
            {t("review.takeAnother")}
          </Button>
        </Link>
        <Link href="/dashboard">
          <Button variant="outline">
            <ChartBar className="h-4 w-4 mr-2" weight="regular" />
            {t("review.viewDashboard")}
          </Button>
        </Link>
      </motion.div>

      {/* Questions review */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25, type: "spring", stiffness: 100, damping: 20 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-emerald-600" weight="fill" />
              {t("review.questionReview")} ({questions.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {questions.map((q, i) => {
                const qId = q.id;
                const isExpanded = expandedQuestions.has(qId);
                const isCorrect = q.is_correct === true;
                const isIncorrect = q.is_correct === false;
                const selectedOptionIds = getSelectedOptionIds(q);

                return (
                  <div
                    key={qId}
                    className={`border rounded-xl overflow-hidden transition-all duration-200 ${
                      isCorrect
                        ? "border-emerald-200 dark:border-emerald-900"
                        : isIncorrect
                        ? "border-red-200 dark:border-red-900"
                        : "border-zinc-200 dark:border-zinc-800"
                    }`}
                  >
                    <button
                      onClick={() => toggleQuestion(qId)}
                      className="w-full flex items-center justify-between p-4 hover:bg-zinc-50 dark:hover:bg-zinc-800/30 transition-colors"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        {isCorrect ? (
                          <CheckCircle className="h-5 w-5 text-emerald-500 shrink-0" weight="fill" />
                        ) : isIncorrect ? (
                          <XCircle className="h-5 w-5 text-red-500 shrink-0" weight="fill" />
                        ) : (
                          <div className="h-5 w-5 rounded-full border-2 border-zinc-400 shrink-0" />
                        )}
                        <span className="font-medium text-sm text-zinc-900 dark:text-zinc-100 truncate">
                          {t("exam.question")} {i + 1}
                        </span>
                        {q.was_flagged && (
                          <Flag className="h-3.5 w-3.5 text-amber-500 shrink-0" weight="fill" />
                        )}
                        <Badge
                          variant={isCorrect ? "success" : isIncorrect ? "danger" : "outline"}
                          className="text-xs shrink-0"
                        >
                          {isCorrect
                            ? t("review.correctLabel")
                            : isIncorrect
                            ? t("review.incorrectLabel")
                            : t("review.unanswered")}
                        </Badge>
                        {q.time_spent_seconds > 0 && (
                          <span className="text-xs text-zinc-400 shrink-0 hidden sm:inline">
                            <ClockAfternoon className="h-3 w-3 inline mr-0.5" weight="regular" />
                            {q.time_spent_seconds}s
                          </span>
                        )}
                      </div>
                      {isExpanded ? (
                        <CaretUp className="h-4 w-4 text-zinc-400 shrink-0" weight="regular" />
                      ) : (
                        <CaretDown className="h-4 w-4 text-zinc-400 shrink-0" weight="regular" />
                      )}
                    </button>

                    {isExpanded && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        className="px-4 pb-4 border-t border-zinc-200 dark:border-zinc-800 pt-4 space-y-4"
                      >
                        {/* Question body */}
                        <div className="p-3 rounded-lg bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-700">
                          <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                            {t("exam.question")}:
                          </p>
                          <p className="text-sm text-zinc-900 dark:text-zinc-100 whitespace-pre-wrap leading-relaxed">
                            {q.body}
                          </p>
                        </div>

                        {/* Options with user's answer highlighted */}
                        <div>
                          <p className="text-xs font-medium text-zinc-500 mb-2 uppercase tracking-wider">
                            {q.question_type === 'fill-blank' ? t("review.yourAnswer") : (t("review.yourAnswer") + " / " + t("review.correctAnswer"))}
                          </p>
                          <div className="space-y-1.5">
                            {q.options.map((opt) => {
                              const isUserSelected = selectedOptionIds.includes(opt.id);
                              // Use per-option is_correct from the backend (available because this is the review endpoint)
                              const optionIsCorrect = opt.is_correct;
                              const isOptionCorrect = isUserSelected && optionIsCorrect;
                              const isOptionWrong = isUserSelected && !optionIsCorrect;
                              const isOptionMissed = !isUserSelected && optionIsCorrect;

                              let borderClass = "border-zinc-200 dark:border-zinc-700";
                              let bgClass = "bg-zinc-50 dark:bg-zinc-800/30";
                              let textClass = "text-zinc-600 dark:text-zinc-400";

                              if (isOptionCorrect) {
                                borderClass = "border-emerald-400 dark:border-emerald-600";
                                bgClass = "bg-emerald-50 dark:bg-emerald-900/10";
                                textClass = "text-emerald-700 dark:text-emerald-300";
                              } else if (isOptionWrong) {
                                borderClass = "border-red-400 dark:border-red-600";
                                bgClass = "bg-red-50 dark:bg-red-900/10";
                                textClass = "text-red-700 dark:text-red-300";
                              } else if (isOptionMissed) {
                                borderClass = "border-emerald-300 dark:border-emerald-700 border-dashed";
                                bgClass = "bg-emerald-50/50 dark:bg-emerald-900/5";
                                textClass = "text-emerald-600 dark:text-emerald-400";
                              }

                              // For fill-blank, show user's answer vs correct answer
                              if (q.question_type === "fill-blank") {
                                return (
                                  <div key={opt.id} className="space-y-1">
                                    <div className={`p-3 rounded-lg border text-sm border-emerald-400 dark:border-emerald-600 bg-emerald-50 dark:bg-emerald-900/10 text-emerald-700 dark:text-emerald-300`}>
                                      <span className="font-medium block mb-1">{t("review.correctAnswer")}:</span>
                                      <code className="text-sm font-mono">{opt.text}</code>
                                    </div>
                                    <div className={`p-3 rounded-lg border text-sm ${
                                      isCorrect
                                        ? "border-emerald-400 dark:border-emerald-600 bg-emerald-50 dark:bg-emerald-900/10 text-emerald-700 dark:text-emerald-300"
                                        : "border-red-400 dark:border-red-600 bg-red-50 dark:bg-red-900/10 text-red-700 dark:text-red-300"
                                    }`}>
                                      <span className="font-medium block mb-1">{t("review.yourAnswer")}:</span>
                                      <code className="text-sm font-mono">{q.user_answer || t("review.noAnswer")}</code>
                                    </div>
                                  </div>
                                );
                              }

                              return (
                                <div
                                  key={opt.id}
                                  className={`p-3 rounded-lg border text-sm flex items-start gap-2.5 ${borderClass} ${bgClass} ${textClass}`}
                                >
                                  <div className={`mt-0.5 w-4 h-4 shrink-0 flex items-center justify-center ${
                                    q.question_type === "multiple-choice" ? "rounded" : "rounded-full"
                                  } ${
                                    isOptionCorrect
                                      ? "bg-emerald-500 border-emerald-500 border-2"
                                      : isOptionWrong
                                      ? "bg-red-500 border-red-500 border-2"
                                      : isOptionMissed
                                      ? "border-2 border-emerald-400 border-dashed bg-emerald-500/10"
                                      : "border-2 border-zinc-400"
                                  }`}>
                                    {(isOptionCorrect || isOptionWrong) && (
                                      <CheckCircle className="h-2.5 w-2.5 text-white" weight="bold" />
                                    )}
                                    {isOptionMissed && (
                                      <span className="text-emerald-500 text-xs font-bold">!</span>
                                    )}
                                  </div>
                                  <div className="flex-1">
                                    <span className="block">{opt.text}</span>
                                    {isOptionCorrect && (
                                      <span className="text-xs text-emerald-500 font-medium mt-0.5 block">
                                        {t("review.correctLabel")} {t("review.selected")}
                                      </span>
                                    )}
                                    {isOptionWrong && (
                                      <span className="text-xs text-red-500 font-medium mt-0.5 block">
                                        {t("review.incorrectLabel")} {t("review.selected")}
                                      </span>
                                    )}
                                    {isOptionMissed && (
                                      <span className="text-xs text-emerald-500 font-medium mt-0.5 block">
                                        {t("review.missed")}
                                      </span>
                                    )}
                                    {!isUserSelected && !isOptionMissed && !optionIsCorrect && (
                                      <span className="text-xs text-zinc-400 mt-0.5 block">{t("review.notSelected")}</span>
                                    )}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>

                        {/* Explanation */}
                        {q.explanation && (
                          <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800">
                            <p className="text-sm font-medium text-blue-700 dark:text-blue-300 mb-1">
                              {t("review.explanation")}
                            </p>
                            <p className="text-sm text-blue-600 dark:text-blue-400">
                              {q.explanation}
                            </p>
                          </div>
                        )}

                        {/* Reference links */}
                        {q.reference_urls && q.reference_urls.length > 0 && (
                          <div className="flex flex-wrap gap-2">
                            {q.reference_urls.map((url, idx) => (
                              <a
                                key={idx}
                                href={url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400 hover:underline"
                              >
                                <BookOpen className="h-3 w-3" weight="regular" />
                                {t("review.viewDocs")} #{idx + 1}
                              </a>
                            ))}
                          </div>
                        )}

                        {/* Deep-Dive Explanation (Knowledge Base) */}
                        <ExplanationPanel
                          questionId={q.id}
                          selectedOptionIds={selectedOptionIds}
                          isCorrect={q.is_correct}
                          onTelemetryEvent={(event) => {
                            handleTelemetryEvent({
                              ...event,
                              question_id: q.id,
                              session_id: reviewSessionIdRef.current,
                            });
                          }}
                        />
                      </motion.div>
                    )}
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
