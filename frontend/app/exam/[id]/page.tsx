"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi, examsApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Clock,
  Flag,
  CaretLeft,
  CaretRight,
  CheckCircle,
  Warning,
  BookOpen,
  ArrowLeft,
  PaperPlaneTilt,
  Spinner,
} from "@phosphor-icons/react";

interface Question {
  id: string;
  body: string;
  options: { id: string; text: string }[];
  question_type: string;
  difficulty: number;
}

export default function ExamSessionPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const examId = params.id as string;

  const [exam, setExam] = useState<any>(null);
  const [attempt, setAttempt] = useState<any>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  // For multiple-choice: track selected option IDs per question
  const [multiAnswers, setMultiAnswers] = useState<Record<string, string[]>>({});
  // For fill-blank: text input per question
  const [textAnswers, setTextAnswers] = useState<Record<string, string>>({});
  const [flagged, setFlagged] = useState<Set<string>>(new Set());
  const [timeLeft, setTimeLeft] = useState(-1);
  const [pageReady, setPageReady] = useState(false);
  const [starting, setStarting] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [result, setResult] = useState<any>(null);
  const { t, locale } = useTranslation();
  const [questionTimes, setQuestionTimes] = useState<Record<string, number>>({});
  const questionTimesRef = useRef<Record<string, number>>({});
  const [error, setError] = useState<string | null>(null);
  const questionStartRef = useRef(Date.now());
  const submittingRef = useRef(false);
  const handleCompleteRef = useRef<() => Promise<void>>(async () => {});

  const totalQuestions = questions.length;
  const currentQuestion = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;

  // Initialize
  useEffect(() => {
    if (authLoading) return;
    if (!isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    if (examId) {
      examsApi.get(examId)
        .then(setExam)
        .catch((err) => {
          console.error("Failed to load exam:", err);
          setError(err.message || t("exam.loadQuestionsError"));
        })
        .finally(() => setPageReady(true));
    }
  }, [isAuthenticated, authLoading, examId, router]);

  const startExam = async () => {
    setStarting(true);
    setError(null);
    try {
      // Step 1: Create attempt on backend — it selects random subset of questions
      const att = await attemptsApi.start({
        exam_id: examId,
        mode: "exam",
      });
      setAttempt(att);

      // Step 2: Fetch only the selected questions (not all 10k from the bank!)
      const qs = await attemptsApi.getQuestions(att.id);
      if (!qs || qs.length === 0) {
        throw new Error(t("exam.noQuestionsError"));
      }

      const sanitized = qs.map((q: any) => ({
        ...q,
        body: q.body
          .replace(/\\n/g, '\n')
          .replace(/^Exhibit:\s*---/gm, '---'),
        options: (q.options || []).map((opt: any) => ({
          id: opt.id,
          text: opt.text,
        })),
      }));

      // Questions are already in random order from backend but shuffle client-side too
      for (let i = sanitized.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [sanitized[i], sanitized[j]] = [sanitized[j], sanitized[i]];
      }

      setQuestions(sanitized);
      setTimeLeft(att.duration_seconds || exam?.duration_minutes * 60 || 5400);
      questionStartRef.current = Date.now();
    } catch (err: any) {
      console.error("Failed to start exam:", err);
      setError(err.message || t("exam.loadQuestionsError"));
    } finally {
      setStarting(false);
    }
  };

  // Timer — tick every second
  useEffect(() => {
    if (!timeLeft || completed) return;
    if (timeLeft <= 0) return;
    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [timeLeft, completed]);

  // Auto-submit when timer hits 0
  useEffect(() => {
    if (timeLeft === 0 && attempt && !completed && !submittingRef.current) {
      handleCompleteRef.current().catch((err) =>
        console.error("Timer-triggered completion failed:", err)
      );
    }
  }, [timeLeft, attempt, completed]);

  const handleAnswer = (optionId: string) => {
    if (!currentQuestion) return;
    if (currentQuestion.question_type === 'multiple-choice') {
      const current = multiAnswers[currentQuestion.id] || [];
      const exists = current.includes(optionId);
      const next = exists
        ? current.filter((id) => id !== optionId)
        : [...current, optionId];
      // Store as comma-separated for backend
      setAnswers((prev) => ({ ...prev, [currentQuestion.id]: next.join(',') }));
      setMultiAnswers((prev) => ({ ...prev, [currentQuestion.id]: next }));
    } else {
      setAnswers((prev) => ({ ...prev, [currentQuestion?.id || '']: optionId }));
    }
  };

  const handleTextAnswer = (value: string) => {
    if (!currentQuestion) return;
    setTextAnswers((prev) => ({ ...prev, [currentQuestion.id]: value }));
    setAnswers((prev) => ({ ...prev, [currentQuestion.id]: value }));
  };

  const toggleFlag = () => {
    if (!currentQuestion) return;
    setFlagged((prev) => {
      const next = new Set(prev);
      if (next.has(currentQuestion.id)) {
        next.delete(currentQuestion.id);
      } else {
        next.add(currentQuestion.id);
      }
      return next;
    });
  };

  const recordTimeForCurrentQuestion = useCallback(() => {
    if (!currentQuestion) return;
    const spent = Math.floor((Date.now() - questionStartRef.current) / 1000);
    if (spent > 0) {
      questionTimesRef.current[currentQuestion.id] = (questionTimesRef.current[currentQuestion.id] || 0) + spent;
    }
    questionStartRef.current = Date.now();
  }, [currentQuestion]);

  const goToQuestion = (index: number) => {
    recordTimeForCurrentQuestion();
    setCurrentIndex(index);
    questionStartRef.current = Date.now();
  };

  // Keyboard navigation: Arrow keys / A-D / 1-9
  useEffect(() => {
    if (!questions.length || completed) return;
    const handler = (e: KeyboardEvent) => {
      // Ignore if user is typing in an input/textarea
      const tag = (e.target as HTMLElement)?.tagName?.toLowerCase();
      if (tag === "input" || tag === "textarea") return;

      switch (e.key) {
        case "ArrowRight":
        case "d":
        case "D":
        case "л":
        case "Л":
          e.preventDefault();
          if (currentIndex < totalQuestions - 1) {
            goToQuestion(currentIndex + 1);
          }
          break;
        case "ArrowLeft":
        case "a":
        case "A":
        case "ф":
        case "Ф":
          e.preventDefault();
          if (currentIndex > 0) {
            goToQuestion(currentIndex - 1);
          }
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          // If answer selected and not last question, advance
          if (answers[currentQuestion?.id] && currentIndex < totalQuestions - 1) {
            goToQuestion(currentIndex + 1);
          }
          break;
        default: {
          // Number keys 1-9 jump to question N
          const num = parseInt(e.key, 10);
          if (!isNaN(num) && num >= 1 && num <= totalQuestions) {
            e.preventDefault();
            goToQuestion(num - 1);
          }
          break;
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [questions.length, completed, currentIndex, totalQuestions, answers, currentQuestion?.id]);

  const handleComplete = useCallback(async () => {
    if (!attempt || submittingRef.current) return;
    submittingRef.current = true;
    setSubmitting(true);
    try {
      // Record time for the current/last question before submitting
      recordTimeForCurrentQuestion();
      // Sync ref to state for any post-submit rendering
      setQuestionTimes({ ...questionTimesRef.current });

      for (const [qId, answer] of Object.entries(answers)) {
        if (!answer) continue;
        await attemptsApi.submitAnswer(attempt.id, {
          question_id: qId,
          answer,
          time_spent_seconds: questionTimesRef.current[qId] || 0,
          was_flagged: flagged.has(qId),
        });
      }
      const res = await attemptsApi.complete(attempt.id);
      setResult(res);
      setCompleted(true);
    } catch (err) {
      console.error("Failed to complete exam:", err);
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg || t("exam.submitError"));
    } finally {
      submittingRef.current = false;
      setSubmitting(false);
    }
  }, [attempt, answers, flagged, t, recordTimeForCurrentQuestion]);

  handleCompleteRef.current = handleComplete;

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  if (!pageReady) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-950">
        <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
      </div>
    );
  }

  // Start screen
  if (!attempt) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-950 text-white px-4">
        <div className="max-w-lg text-center">
          <BookOpen className="h-16 w-16 mx-auto mb-6 text-emerald-500" weight="light" />
          <h1 className="text-3xl font-bold tracking-tight mb-2 text-white">{exam?.name || t("exam.examLabel")}</h1>
          <p className="text-zinc-400 mb-2 font-mono text-sm">{exam?.code}</p>
          <div className="flex justify-center gap-4 mb-8 text-sm text-zinc-500">
            <span>{exam?.total_questions || 10} {t("exam.questions")}</span>
            <span>{exam?.duration_minutes || 90} {t("exam.minutes")}</span>
            <span>{exam?.passing_score || 65}{t("exam.toPass")}</span>
          </div>
          <p className="text-zinc-600 text-sm mb-8 max-w-sm mx-auto">
            {t("exam.startDescription")}
          </p>
          {error && (
            <div className="mb-6 p-3 rounded-lg bg-red-900/20 border border-red-800 text-sm text-red-400">
              {error}
            </div>
          )}
          <div className="flex justify-center gap-4">
            <Button variant="outline" onClick={() => router.push("/exams")}>
              <ArrowLeft className="h-4 w-4 mr-2" weight="regular" />
              {t("exam.backToExams")}
            </Button>
            <Button variant="primary" onClick={startExam} disabled={starting} size="lg">
              {starting ? (
                <Spinner className="h-5 w-5 animate-spin mr-2" weight="bold" />
              ) : null}
              {t("exam.startExam")}
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // Results
  if (completed && result) {
    const rawScore = Number.isFinite(result?.score) ? result.score : 0;
    const score = Math.round(rawScore);
    const passingScore = Number.isFinite(exam?.passing_score) ? exam.passing_score : 65;
    const passed = rawScore >= passingScore;

    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-950 text-white px-4">
        <div className="max-w-md text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 150, damping: 15 }}
          >
            <div className={`p-4 rounded-full inline-flex mb-6 ${passed ? "bg-emerald-500/20" : "bg-red-500/20"}`}>
              {passed ? (
                <CheckCircle className="h-16 w-16 text-emerald-500" weight="fill" />
              ) : (
                <Warning className="h-16 w-16 text-red-500" weight="fill" />
              )}
            </div>
          </motion.div>
          <h1 className="text-3xl font-bold tracking-tight mb-2 text-white">
            {passed ? t("exam.congratulations") : t("exam.keepPracticing")}
          </h1>
          <p className="text-zinc-400 mb-6">
            {passed ? t("exam.youPassed") : t("exam.youFailed")}
          </p>
          <div className="text-6xl font-bold tracking-tighter mb-2 text-white">{score}%</div>
          <p className="text-zinc-500 mb-8">{exam?.passing_score || 65}{t("exam.requiredToPass")}</p>
          <div className="flex justify-center gap-4">
            <Button variant="outline" onClick={() => router.push(`/review/${attempt?.id}`)}>
              {t("exam.reviewAnswers")}
            </Button>
            <Button variant="primary" onClick={() => router.push("/exams")}>
              {t("exam.backToExamsBtn")}
            </Button>
          </div>
        </div>
      </div>
    );
  }

  // In-progress exam
  return (
    <div className="exam-mode flex flex-col">
      {/* Top bar */}
      <div className="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-zinc-800 bg-zinc-900/50 backdrop-blur-xl">
        <div className="flex items-center gap-3">
          <BookOpen className="h-5 w-5 text-emerald-500" weight="regular" />
          <span className="font-medium text-sm text-zinc-100">{exam?.code || t("exam.examLabel")}</span>
          <span className="text-zinc-500 text-sm font-mono">
            {currentIndex + 1}/{totalQuestions}
          </span>
        </div>
        <div className="flex items-center gap-3 sm:gap-4">
          <div className="flex items-center gap-1.5 text-sm text-zinc-400">
            <CheckCircle className="h-4 w-4 text-emerald-500" weight="fill" />
            <span className="font-mono">{answeredCount}/{totalQuestions}</span>
          </div>
          <div className={`flex items-center gap-2 text-sm font-mono px-3 py-1 rounded-lg ${
            timeLeft < 300 ? "bg-red-900/40 text-red-400 timer-warning" : "bg-zinc-800 text-zinc-200"
          }`}>
            <Clock className="h-4 w-4" weight="regular" />
            {formatTime(timeLeft)}
          </div>
          <Button
            variant="danger"
            size="sm"
            onClick={() => {
              if (confirm(t("exam.confirmSubmit"))) {
                handleComplete();
              }
            }}
            disabled={submitting}
            className="hidden sm:flex"
          >
            {submitting ? <Spinner className="h-4 w-4 animate-spin" weight="bold" /> : <PaperPlaneTilt className="h-4 w-4" weight="regular" />}                  <span className="ml-1.5">{t("exam.submit")}</span>
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Question panel */}
        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          {currentQuestion && (
            <motion.div
              key={currentQuestion.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ type: "spring", stiffness: 100, damping: 20 }}
              className="max-w-3xl mx-auto"
            >
              <div className="flex items-center gap-2 mb-4">
                <Badge variant="outline" className="text-zinc-400 border-zinc-700 text-xs">
                  {t("exam.question")} {currentIndex + 1}
                </Badge>
                {currentQuestion.difficulty && (
                  <Badge variant="outline" className={`border-zinc-700 text-xs ${
                    currentQuestion.difficulty <= 2 ? "text-emerald-400" :
                    currentQuestion.difficulty <= 3 ? "text-amber-400" : "text-red-400"
                  }`}>
                    {currentQuestion.difficulty <= 2 ? t("exam.easy") : currentQuestion.difficulty <= 3 ? t("exam.medium") : t("exam.hard")}
                  </Badge>
                )}
              </div>

              <h2 className="text-xl lg:text-2xl font-medium mb-8 leading-relaxed text-zinc-100 whitespace-pre-wrap">
                {currentQuestion.body}
              </h2>

              {/* Fill-blank: text input */}
              {currentQuestion.question_type === 'fill-blank' && (
                <div className="space-y-3">
                  <input
                    type="text"
                    value={textAnswers[currentQuestion.id] || ''}
                    onChange={(e) => handleTextAnswer(e.target.value)}
                    placeholder={t('exam.typeCommand')}
                    className="w-full px-4 py-3 rounded-xl border border-zinc-700 bg-zinc-900 text-white placeholder-zinc-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/50 outline-none transition-all font-mono text-base"
                    autoComplete="off"
                    spellCheck={false}
                  />
                  <p className="text-xs text-zinc-500">{t('exam.fillBlankHint')}</p>
                </div>
              )}

              {/* Multiple-choice: checkboxes */}
              {currentQuestion.question_type === 'multiple-choice' && (
                <div className="space-y-3">
                  {currentQuestion.options.map((opt) => {
                    const selectedOptions = multiAnswers[currentQuestion.id] || [];
                    const isSelected = selectedOptions.includes(opt.id);
                    return (
                      <button
                        key={opt.id}
                        onClick={() => handleAnswer(opt.id)}
                        className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
                          isSelected
                            ? "border-emerald-500 bg-emerald-500/10 text-white shadow-[0_0_20px_rgba(16,185,129,0.15)]"
                            : "border-zinc-800 hover:border-zinc-600 text-zinc-300 hover:text-white bg-zinc-900"
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${
                            isSelected ? "border-emerald-500 bg-emerald-500" : "border-zinc-500"
                          }`}>
                            {isSelected && (
                              <CheckCircle className="h-3 w-3 text-white" weight="bold" />
                            )}
                          </div>
                          <span>{opt.text}</span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}

              {/* Single-choice: radio buttons */}
              {(!currentQuestion.question_type || currentQuestion.question_type === 'single-choice') && (
                <div className="space-y-3">
                  {currentQuestion.options.map((opt) => {
                    const isSelected = answers[currentQuestion.id] === opt.id;
                    return (
                      <button
                        key={opt.id}
                        onClick={() => handleAnswer(opt.id)}
                        className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
                          isSelected
                            ? "border-emerald-500 bg-emerald-500/10 text-white shadow-[0_0_20px_rgba(16,185,129,0.15)]"
                            : "border-zinc-800 hover:border-zinc-600 text-zinc-300 hover:text-white bg-zinc-900"
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-colors ${
                            isSelected ? "border-emerald-500 bg-emerald-500" : "border-zinc-500"
                          }`}>
                            {isSelected && (
                              <CheckCircle className="h-3 w-3 text-white" weight="fill" />
                            )}
                          </div>
                          <span>{opt.text}</span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </motion.div>
          )}
        </div>

        {/* Navigation sidebar */}
        <div className="w-64 border-l border-zinc-800 bg-zinc-900/50 p-4 overflow-y-auto hidden lg:block">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-zinc-400">{t("exam.questions")}</h3>
            <button
              onClick={toggleFlag}
              className={`p-1.5 rounded-lg transition-colors ${
                currentQuestion && flagged.has(currentQuestion.id)
                  ? "text-amber-400 bg-amber-400/10"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
              title={t("exam.question")}
            >
              <Flag className="h-4 w-4" weight="regular" />
            </button>
          </div>

          <div className="grid grid-cols-5 gap-1.5">
            {questions.map((q, idx) => {
              const isAnswered = !!answers[q.id];
              const isFlagged = flagged.has(q.id);
              const isCurrent = idx === currentIndex;

              return (
                <button
                  key={q.id}
                  onClick={() => goToQuestion(idx)}
                  className={`w-8 h-8 rounded-lg text-xs font-medium transition-all ${
                    isCurrent
                      ? "ring-2 ring-emerald-500 bg-emerald-500/20 text-white"
                      : isAnswered
                      ? "bg-emerald-500/20 text-emerald-400"
                      : "bg-zinc-800 text-zinc-400 hover:bg-zinc-700"
                  } ${isFlagged ? "ring-1 ring-amber-500" : ""}`}
                >
                  {idx + 1}
                </button>
              );
            })}
          </div>

          <div className="mt-6 space-y-2">
            <div className="flex items-center gap-2 text-xs text-zinc-500">
              <div className="w-3 h-3 rounded bg-emerald-500/20" />
              <span>{t("exam.answered")} ({answeredCount})</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-zinc-500">
              <div className="w-3 h-3 rounded bg-zinc-800" />
              <span>{t("exam.unanswered")} ({totalQuestions - answeredCount})</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-zinc-500">
              <div className="w-3 h-3 rounded border border-amber-500" />
              <span>{t("exam.flagged")} ({flagged.size})</span>
            </div>
          </div>

          <Button
            variant="primary"
            className="w-full mt-6"
            size="sm"
            onClick={() => handleComplete()}
            disabled={submitting}
          >
            {submitting ? (
              <Spinner className="h-4 w-4 animate-spin mr-2" weight="bold" />
            ) : null}
            {t("exam.submitExam")}
          </Button>
        </div>
      </div>

      {/* Bottom nav (mobile) */}
      <div className="lg:hidden flex items-center justify-between p-4 border-t border-zinc-800 bg-zinc-900">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => goToQuestion(Math.max(0, currentIndex - 1))}
          disabled={currentIndex === 0}
        >
          <CaretLeft className="h-4 w-4" weight="regular" />
        </Button>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleFlag}
            className={`p-2 rounded-lg ${flagged.has(currentQuestion?.id || "") ? "text-amber-400" : "text-zinc-500"}`}
          >
            <Flag className="h-4 w-4" weight="regular" />
          </button>
          <span className="text-sm font-mono text-zinc-400">{currentIndex + 1}/{totalQuestions}</span>
        </div>

        <Button
          variant="ghost"
          size="sm"
          onClick={() => goToQuestion(Math.min(totalQuestions - 1, currentIndex + 1))}
          disabled={currentIndex === totalQuestions - 1}
        >
          <CaretRight className="h-4 w-4" weight="regular" />
        </Button>
      </div>
    </div>
  );
}
