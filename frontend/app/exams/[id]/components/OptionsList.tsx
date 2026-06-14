"use client";

import { CheckCircle } from "@phosphor-icons/react";

interface Option {
  id: string;
  text: string;
}

interface OptionsListProps {
  questionType: string;
  options: Option[];
  selectedAnswer?: string;
  selectedAnswers?: string[];
  textAnswer?: string;
  onSelect: (optionId: string) => void;
  onTextChange: (value: string) => void;
  typeCommand: string;
  fillBlankHint: string;
}

export function OptionsList({
  questionType,
  options,
  selectedAnswer,
  selectedAnswers = [],
  textAnswer,
  onSelect,
  onTextChange,
  typeCommand,
  fillBlankHint,
}: OptionsListProps) {
  if (questionType === "fill-blank") {
    return (
      <div className="space-y-3">
        <input
          type="text"
          value={textAnswer || ""}
          onChange={(e) => onTextChange(e.target.value)}
          placeholder={typeCommand}
          className="w-full px-4 py-3 rounded-xl border border-zinc-300 bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/50 outline-none transition-all font-mono text-base dark:border-zinc-700 dark:bg-zinc-900 dark:text-white dark:placeholder-zinc-500"
          autoComplete="off"
          spellCheck={false}
        />
        <p className="text-xs text-zinc-500 dark:text-zinc-400">{fillBlankHint}</p>
      </div>
    );
  }

  if (questionType === "multiple-choice") {
    return (
      <div className="space-y-3">
        {options.map((opt) => {
          const isSelected = selectedAnswers.includes(opt.id);
          return (
            <button
              key={opt.id}
              onClick={() => onSelect(opt.id)}
              className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
                isSelected
                  ? "border-emerald-500 bg-emerald-500/10 text-zinc-900 shadow-[inset_0_0_0_1px_rgba(16,185,129,0.3)] dark:text-white"
                  : "border-zinc-200 hover:border-zinc-400 text-zinc-700 hover:text-zinc-900 bg-white dark:border-zinc-800 dark:hover:border-zinc-600 dark:text-zinc-300 dark:hover:text-white dark:bg-zinc-900"
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${
                    isSelected ? "border-emerald-500 bg-emerald-500" : "border-zinc-400 dark:border-zinc-500"
                  }`}
                >
                  {isSelected && <CheckCircle className="h-3 w-3 text-white" weight="bold" />}
                </div>
                <span>{opt.text}</span>
              </div>
            </button>
          );
        })}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {options.map((opt) => {
        const isSelected = selectedAnswer === opt.id;
        return (
          <button
            key={opt.id}
            onClick={() => onSelect(opt.id)}
            className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
              isSelected
                ? "border-emerald-500 bg-emerald-500/10 text-zinc-900 shadow-[inset_0_0_0_1px_rgba(16,185,129,0.3)] dark:text-white"
                : "border-zinc-200 hover:border-zinc-400 text-zinc-700 hover:text-zinc-900 bg-white dark:border-zinc-800 dark:hover:border-zinc-600 dark:text-zinc-300 dark:hover:text-white dark:bg-zinc-900"
            }`}
          >
            <div className="flex items-center gap-3">
              <div
                className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-colors ${
                  isSelected ? "border-emerald-500 bg-emerald-500" : "border-zinc-400 dark:border-zinc-500"
                }`}
              >
                {isSelected && <CheckCircle className="h-3 w-3 text-white" weight="fill" />}
              </div>
              <span>{opt.text}</span>
            </div>
          </button>
        );
      })}
    </div>
  );
}
