"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi, examsApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";
import { ExamHeader } from "./components/ExamHeader";
import { QuestionCard } from "./components/QuestionCard";
import { QuestionNav } from "./components/QuestionNav";
import { ExamResults } from "./components/ExamResults";
import {
  BookOpen,
  ArrowLeft,
  CaretLeft,
  CaretRight,
  Flag,
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
  const { t } = useTranslation();

  const [exam, setExam] = useState<any>(null);
  const [attempt, setAttempt] = useState<any>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [multiAnswers, setMultiAnswers] = useState<Record<string, string[]>>({});
  const [textAnswers, setTextAnswers] = useState<Record<string, string>>({});
  const [flagged, setFlagged] = useState<Set<string>>(new Set());
  const [timeLeft, setTimeLeft] = useState(-1);
  const [pageReady, setPageReady] = useState(false);
  const [starting, setStarting] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [questionTimes, setQuestionTimes] = useState<Record<string, number>>({});

  const questionTimesRef = useRef<Record<string, number>>({});
  const questionStartRef = useRef(Date.now());
  const submittingRef = useRef(false);
  const handleCompleteRef = useRef<() => Promise<void>>(async () => {});

  const totalQuestions = questions.length;
  const currentQuestion = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;

  useEffect(() => {
    if (authLoading) return;
    if (!isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    if (examId) {
      examsApi
        .get(examId)
        .then(setExam)
        .catch((err) => {
          console.error("Failed to load exam:", err);
          setError(err.message || t("exam.loadQuestionsError"));
        })
        .finally(() => setPageReady(true));
    }
  }, [isAuthenticated, authLoading, examId, router, t]);

  const startExam = async () => {
    setStarting(true);
    setError(null);
    try {
      const att = await attemptsApi.start({
        exam_id: examId,
        mode: "exam",
      });
      setAttempt(att);

      const qs = await attemptsApi.getQuestions(att.id);
      if (!qs || qs.length === 0) {
        throw new Error(t("exam.noQuestionsError"));
      }

      const sanitized = qs.map((q: any) => ({
        ...q,
        body: q.body.replace(/\\n/g, "\n").replace(/^Exhibit:\s*---/gm, "---"),
        options: (q.options || []).map((opt: any) => ({
          id: opt.id,
          text: opt.text,
        })),
      }));

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

  useEffect(() => {
    if (timeLeft === 0 && attempt && !completed && !submittingRef.current) {
      handleCompleteRef.current().catch((err) =>
        console.error("Timer-triggered completion failed:", err)
      );
    }
  }, [timeLeft, attempt, completed]);

  const handleAnswer = (optionId: string) => {
    if (!currentQuestion) return;
    if (currentQuestion.question_type === "multiple-choice") {
      const current = multiAnswers[currentQuestion.id] || [];
      const exists = current.includes(optionId);
      const next = exists ? current.filter((id) => id !== optionId) : [...current, optionId];
      setAnswers((prev) => ({ ...prev, [currentQuestion.id]: next.join(",") }));
      setMultiAnswers((prev) => ({ ...prev, [currentQuestion.id]: next }));
    } else {
      setAnswers((prev) => ({ ...prev, [currentQuestion.id]: optionId }));
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
      if (next.has(currentQuestion.id)) next.delete(currentQuestion.id);
      else next.add(currentQuestion.id);
      return next;
    });
  };

  const recordTimeForCurrentQuestion = useCallback(() => {
    if (!currentQuestion) return;
    const spent = Math.floor((Date.now() - questionStartRef.current) / 1000);
    if (spent > 0) {
      questionTimesRef.current[currentQuestion.id] =
        (questionTimesRef.current[currentQuestion.id] || 0) + spent;
    }
    questionStartRef.current = Date.now();
  }, [currentQuestion]);

  const goToQuestion = (index: number) => {
    recordTimeForCurrentQuestion();
    setCurrentIndex(index);
    questionStartRef.current = Date.now();
  };

  useEffect(() => {
    if (!questions.length || completed) return;
    const handler = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement)?.tagName?.toLowerCase();
      if (tag === "input" || tag === "textarea") return;

      switch (e.key) {
        case "ArrowRight":
        case "d":
        case "D":
        case "л":
        case "Л":
          e.preventDefault();
          if (currentIndex < totalQuestions - 1) goToQuestion(currentIndex + 1);
          break;
        case "ArrowLeft":
        case "a":
        case "A":
        case "ф":
        case "Ф":
          e.preventDefault();
          if (currentIndex > 0) goToQuestion(currentIndex - 1);
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          if (answers[currentQuestion?.id] && currentIndex < totalQuestions - 1) {
            goToQuestion(currentIndex + 1);
          }
          break;
        default: {
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
      recordTimeForCurrentQuestion();
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

  if (!pageReady) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-50 dark:bg-zinc-950">
        <Spinner className="h-8 w-8 text-emerald-500 animate-spin" />
      </div>
    );
  }

  if (!attempt) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 px-4">
        <div className="max-w-lg text-center">
          <BookOpen className="h-16 w-16 mx-auto mb-6 text-emerald-500" weight="light" />
          <h1 className="text-3xl font-bold tracking-tight mb-2 text-zinc-900 dark:text-zinc-100">
            {exam?.name || t("exam.examLabel")}
          </h1>
          <p className="text-zinc-400 mb-2 font-mono text-sm">{exam?.code}</p>
          <div className="flex justify-center gap-4 mb-8 text-sm text-zinc-500">
            <span>
              {exam?.total_questions || 10} {t("exam.questions")}
            </span>
            <span>
              {exam?.duration_minutes || 90} {t("exam.minutes")}
            </span>
            <span>
              {exam?.passing_score || 65}
              {t("exam.toPass")}
            </span>
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
              {starting ? <Spinner className="h-5 w-5 mr-2" /> : null}
              {t("exam.startExam")}
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (completed && result) {
    return (
      <div className="exam-mode">
        <ExamResults
          score={result?.score || 0}
          passingScore={exam?.passing_score || 65}
          congratulations={t("exam.congratulations")}
          keepPracticing={t("exam.keepPracticing")}
          youPassed={t("exam.youPassed")}
          youFailed={t("exam.youFailed")}
          requiredToPass={t("exam.requiredToPass")}
          reviewAnswers={t("exam.reviewAnswers")}
          backToExams={t("exam.backToExamsBtn")}
          attemptId={attempt?.id}
        />
      </div>
    );
  }

  return (
    <div className="exam-mode flex flex-col">
      <ExamHeader
        code={exam?.code}
        label={t("exam.examLabel")}
        currentIndex={currentIndex}
        total={totalQuestions}
        answeredCount={answeredCount}
        timeLeft={timeLeft}
        submitting={submitting}
        onSubmit={handleComplete}
        confirmText={t("exam.confirmSubmit")}
        submitLabel={t("exam.submit")}
      />

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          {currentQuestion && (
            <div className="max-w-3xl mx-auto">
              <QuestionCard
                question={currentQuestion}
                index={currentIndex}
                total={totalQuestions}
                selectedAnswer={answers[currentQuestion.id]}
                selectedAnswers={multiAnswers[currentQuestion.id] || []}
                textAnswer={textAnswers[currentQuestion.id]}
                onSelect={handleAnswer}
                onTextChange={handleTextAnswer}
                questionLabel={t("exam.question")}
                easyLabel={t("exam.easy")}
                mediumLabel={t("exam.medium")}
                hardLabel={t("exam.hard")}
                typeCommand={t("exam.typeCommand")}
                fillBlankHint={t("exam.fillBlankHint")}
              />

              {/* Navigation buttons */}
              <div className="flex items-center justify-between mt-8">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => goToQuestion(Math.max(0, currentIndex - 1))}
                  disabled={currentIndex === 0}
                >
                  <CaretLeft className="h-4 w-4 mr-2" weight="regular" />
                  {t("exam.previous")}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={toggleFlag}
                  className={flagged.has(currentQuestion.id) ? "text-amber-600 border-amber-500/30 dark:text-amber-400" : ""}
                >
                  <Flag className="h-4 w-4 mr-2" weight="regular" />
                  {flagged.has(currentQuestion.id) ? t("exam.flagged") : t("exam.flag")}
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => goToQuestion(Math.min(totalQuestions - 1, currentIndex + 1))}
                  disabled={currentIndex === totalQuestions - 1}
                >
                  {t("exam.next")}
                  <CaretRight className="h-4 w-4 ml-2" weight="regular" />
                </Button>
              </div>
            </div>
          )}
        </div>

        <QuestionNav
          total={totalQuestions}
          currentIndex={currentIndex}
          answers={answers}
          flagged={flagged}
          questionIds={questions.map((q) => q.id)}
          onGoTo={goToQuestion}
          onToggleFlag={toggleFlag}
          answeredLabel={t("exam.answered")}
          unansweredLabel={t("exam.unanswered")}
          flaggedLabel={t("exam.flagged")}
          submitLabel={t("exam.submitExam")}
          onSubmit={handleComplete}
          submitting={submitting}
        />
      </div>

      {/* Mobile bottom nav */}
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
            className={`p-2 rounded-lg ${
              flagged.has(currentQuestion?.id || "") ? "text-amber-400" : "text-zinc-500"
            }`}
          >
            <Flag className="h-4 w-4" weight="regular" />
          </button>
          <span className="text-sm font-mono text-zinc-400">
            {currentIndex + 1}/{totalQuestions}
          </span>
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
