"use client";

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { CheckCircle, Warning } from "@phosphor-icons/react";

interface ExamResultsProps {
  score: number;
  passingScore: number;
  congratulations: string;
  keepPracticing: string;
  youPassed: string;
  youFailed: string;
  requiredToPass: string;
  reviewAnswers: string;
  backToExams: string;
  attemptId?: string;
}

export function ExamResults({
  score,
  passingScore,
  congratulations,
  keepPracticing,
  youPassed,
  youFailed,
  requiredToPass,
  reviewAnswers,
  backToExams,
  attemptId,
}: ExamResultsProps) {
  const router = useRouter();
  const passed = score >= passingScore;

  return (
    <div className="min-h-[100dvh] flex items-center justify-center px-4 bg-zinc-50 dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100">
      <div className="max-w-md text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 150, damping: 15 }}
        >
          <div
            className={`p-4 rounded-full inline-flex mb-6 ${
              passed ? "bg-emerald-500/20" : "bg-red-500/20"
            }`}
          >
            {passed ? (
              <CheckCircle className="h-16 w-16 text-emerald-500" weight="fill" />
            ) : (
              <Warning className="h-16 w-16 text-red-500" weight="fill" />
            )}
          </div>
        </motion.div>
        <h1 className="text-3xl font-bold tracking-tight mb-2 text-zinc-900 dark:text-zinc-100">
          {passed ? congratulations : keepPracticing}
        </h1>
        <p className="text-zinc-500 dark:text-zinc-400 mb-6">{passed ? youPassed : youFailed}</p>
        <div className="text-6xl font-bold tracking-tighter mb-2 text-zinc-900 dark:text-zinc-100">
          {Math.round(score)}%
        </div>
        <p className="text-zinc-500 dark:text-zinc-500 mb-8">
          {passingScore}
          {requiredToPass}
        </p>
        <div className="flex justify-center gap-4">
          <Button
            variant="outline"
            onClick={() => router.push(attemptId ? `/review/${attemptId}` : "/review")}
          >
            {reviewAnswers}
          </Button>
          <Button variant="primary" onClick={() => router.push("/exams")}>
            {backToExams}
          </Button>
        </div>
      </div>
    </div>
  );
}
