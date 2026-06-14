"use client";

import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Flag } from "@phosphor-icons/react";

interface QuestionNavProps {
  total: number;
  currentIndex: number;
  answers: Record<string, string>;
  flagged: Set<string>;
  questionIds: string[];
  onGoTo: (index: number) => void;
  onToggleFlag: () => void;
  answeredLabel: string;
  unansweredLabel: string;
  flaggedLabel: string;
  submitLabel: string;
  onSubmit: () => void;
  submitting: boolean;
}

export function QuestionNav({
  total,
  currentIndex,
  answers,
  flagged,
  questionIds,
  onGoTo,
  onToggleFlag,
  answeredLabel,
  unansweredLabel,
  flaggedLabel,
  submitLabel,
  onSubmit,
  submitting,
}: QuestionNavProps) {
  const answeredCount = questionIds.filter((id) => !!answers[id]).length;

  return (
    <div className="w-64 border-l border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 p-4 overflow-y-auto hidden lg:block">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-zinc-500 dark:text-zinc-400">Questions</h3>
        <button
          onClick={onToggleFlag}
          className={`p-1.5 rounded-lg transition-colors ${
            flagged.has(questionIds[currentIndex])
              ? "text-amber-400 bg-amber-400/10"
              : "text-zinc-500 hover:text-zinc-300"
          }`}
        >
          <Flag className="h-4 w-4" weight="regular" />
        </button>
      </div>

      <div className="grid grid-cols-5 gap-1.5">
        {questionIds.map((qId, idx) => {
          const isAnswered = !!answers[qId];
          const isFlagged = flagged.has(qId);
          const isCurrent = idx === currentIndex;

          return (
            <button
              key={qId}
              onClick={() => onGoTo(idx)}
              className={`w-8 h-8 rounded-lg text-xs font-medium transition-all ${
                isCurrent
                  ? "ring-2 ring-emerald-500 bg-emerald-500/20 text-zinc-900 dark:text-white"
                  : isAnswered
                  ? "bg-emerald-500/20 text-emerald-600 dark:text-emerald-400"
                  : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
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
          <span>
            {answeredLabel} ({answeredCount})
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs text-zinc-500">
          <div className="w-3 h-3 rounded bg-zinc-800" />
          <span>
            {unansweredLabel} ({total - answeredCount})
          </span>
        </div>
        <div className="flex items-center gap-2 text-xs text-zinc-500">
          <div className="w-3 h-3 rounded border border-amber-500" />
          <span>
            {flaggedLabel} ({flagged.size})
          </span>
        </div>
      </div>

      <Button
        variant="primary"
        className="w-full mt-6"
        size="sm"
        onClick={onSubmit}
        disabled={submitting}
      >
        {submitting ? <Spinner className="h-4 w-4 mr-2" /> : null}
        {submitLabel}
      </Button>
    </div>
  );
}
