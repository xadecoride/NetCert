"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";
import { Clock, CheckCircle, BookOpen, PaperPlaneTilt } from "@phosphor-icons/react";

interface ExamHeaderProps {
  code: string;
  label: string;
  currentIndex: number;
  total: number;
  answeredCount: number;
  timeLeft: number;
  submitting: boolean;
  onSubmit: () => void;
  confirmText: string;
  submitLabel: string;
}

function formatTime(seconds: number) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s
    .toString()
    .padStart(2, "0")}`;
}

export function ExamHeader({
  code,
  label,
  currentIndex,
  total,
  answeredCount,
  timeLeft,
  submitting,
  onSubmit,
  confirmText,
  submitLabel,
}: ExamHeaderProps) {
  const progress = total > 0 ? ((currentIndex + 1) / total) * 100 : 0;

  return (
    <div className="flex flex-col gap-3 px-4 sm:px-6 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/50 backdrop-blur-xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <BookOpen className="h-5 w-5 text-emerald-500" weight="regular" />
          <span className="font-medium text-sm text-zinc-900 dark:text-zinc-100">{code || label}</span>
          <span className="text-zinc-500 text-sm font-mono">
            {currentIndex + 1}/{total}
          </span>
        </div>
        <div className="flex items-center gap-3 sm:gap-4">
          <div className="flex items-center gap-1.5 text-sm text-zinc-500 dark:text-zinc-400">
            <CheckCircle className="h-4 w-4 text-emerald-500" weight="fill" />
            <span className="font-mono">
              {answeredCount}/{total}
            </span>
          </div>
          <Badge
            variant="outline"
            className={`flex items-center gap-2 text-sm font-mono px-3 py-1 rounded-lg ${
              timeLeft < 300
                ? "bg-red-50 text-red-600 border-red-200 dark:bg-red-900/40 dark:text-red-400 dark:border-red-800 timer-warning"
                : "bg-zinc-100 text-zinc-700 border-zinc-200 dark:bg-zinc-800 dark:text-zinc-200 dark:border-zinc-700"
            }`}
          >
            <Clock className="h-4 w-4" weight="regular" />
            {formatTime(timeLeft)}
          </Badge>
          <Button
            variant="danger"
            size="sm"
            onClick={() => {
              if (confirm(confirmText)) {
                onSubmit();
              }
            }}
            disabled={submitting}
            className="hidden sm:flex"
          >
            {submitting ? (
              <Spinner className="h-4 w-4 mr-1.5" />
            ) : (
              <PaperPlaneTilt className="h-4 w-4 mr-1.5" weight="regular" />
            )}
            {submitLabel}
          </Button>
        </div>
      </div>
      <div className="w-full h-1 bg-zinc-800 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-emerald-500 rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.4, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
