"use client";

import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { BentoCard } from "@/components/ui/card";
import { OptionsList } from "./OptionsList";

interface Option {
  id: string;
  text: string;
}

interface Question {
  id: string;
  body: string;
  options: Option[];
  question_type: string;
  difficulty: number;
}

interface QuestionCardProps {
  question: Question;
  index: number;
  total: number;
  selectedAnswer?: string;
  selectedAnswers?: string[];
  textAnswer?: string;
  onSelect: (optionId: string) => void;
  onTextChange: (value: string) => void;
  questionLabel: string;
  easyLabel: string;
  mediumLabel: string;
  hardLabel: string;
  typeCommand: string;
  fillBlankHint: string;
}

export function QuestionCard({
  question,
  index,
  total,
  selectedAnswer,
  selectedAnswers,
  textAnswer,
  onSelect,
  onTextChange,
  questionLabel,
  easyLabel,
  mediumLabel,
  hardLabel,
  typeCommand,
  fillBlankHint,
}: QuestionCardProps) {
  const difficultyLabel =
    question.difficulty <= 2 ? easyLabel : question.difficulty <= 3 ? mediumLabel : hardLabel;
  const difficultyColor =
    question.difficulty <= 2
      ? "text-emerald-400 border-emerald-500/30"
      : question.difficulty <= 3
      ? "text-amber-400 border-amber-500/30"
      : "text-red-400 border-red-500/30";

  return (
    <motion.div
      key={question.id}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
    >
      <BentoCard className="bg-white/80 border-zinc-200 dark:bg-zinc-900/70 dark:border-zinc-800">
        <div className="flex items-center gap-2 mb-4">
          <Badge variant="outline" className="text-zinc-500 border-zinc-300 dark:text-zinc-400 dark:border-zinc-700 text-xs">
            {questionLabel} {index + 1}/{total}
          </Badge>
          {question.difficulty > 0 && (
            <Badge variant="outline" className={`text-xs ${difficultyColor}`}>
              {difficultyLabel}
            </Badge>
          )}
        </div>

        <h2 className="text-xl lg:text-2xl font-medium mb-8 leading-relaxed text-zinc-900 dark:text-zinc-100 whitespace-pre-wrap">
          {question.body}
        </h2>

        <OptionsList
          questionType={question.question_type}
          options={question.options}
          selectedAnswer={selectedAnswer}
          selectedAnswers={selectedAnswers}
          textAnswer={textAnswer}
          onSelect={onSelect}
          onTextChange={onTextChange}
          typeCommand={typeCommand}
          fillBlankHint={fillBlankHint}
        />
      </BentoCard>
    </motion.div>
  );
}
