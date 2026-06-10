"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "@/lib/i18n/context";
import { explanationsApi } from "@/lib/api";
import { Spinner } from "@/components/ui/spinner";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  CaretDown,
  CaretUp,
  BookOpen,
  Command,
  Copy,
  MagnifyingGlass,
  Lightbulb,
  ChartBar,
  Network,
  Bug,
  Clock,
} from "@phosphor-icons/react";

interface DistractorAnalysis {
  option_id: string;
  why_wrong: string;
  common_mistake: boolean;
}

interface Section {
  section_type: string;
  title: string;
  content: string;
  is_collapsible: boolean;
  sort_order: number;
}

interface Explanation {
  id: string;
  question_id: string;
  version: number;
  sections: Section[];
  summary: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface ExplanationPanelProps {
  questionId: string;
  selectedOptionIds: string[];
  isCorrect: boolean | null;
  onTelemetryEvent?: (event: {
    event_type: string;
    section_type?: string;
    distractor_option_id?: string;
    time_spent_seconds: number;
  }) => void;
}

const SECTION_ICONS: Record<string, React.ElementType> = {
  tl_dr: Lightbulb,
  scenario: BookOpen,
  why_correct: ChartBar,
  distractor_analysis: Bug,
  cli_examples: Command,
  visualization: Network,
  vendor_nuances: MagnifyingGlass,
};

export default function ExplanationPanel({
  questionId,
  selectedOptionIds,
  isCorrect,
  onTelemetryEvent,
}: ExplanationPanelProps) {
  const { t } = useTranslation();
  const [explanation, setExplanation] = useState<Explanation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [expandedAll, setExpandedAll] = useState(false);
  const sessionStartRef = useRef(Date.now());
  const sessionIdRef = useRef(crypto.randomUUID());

  // Load explanation on mount
  useEffect(() => {
    setLoading(true);
    setError(null);
    explanationsApi
      .get(questionId)
      .then((data) => {
        const explanation = data as Explanation;
        setExplanation(explanation);
        // Auto-expand distractor_analysis if user got it wrong
        const autoExpand = new Set<string>();
        autoExpand.add("tl_dr"); // Always show TL;DR
        if (isCorrect === false) {
          autoExpand.add("distractor_analysis");
          autoExpand.add("why_correct");
        } else if (isCorrect === true) {
          autoExpand.add("why_correct");
        }
        setExpandedSections(autoExpand);
        // Send telemetry: opened
        onTelemetryEvent?.({
          event_type: "explanation_opened",
          section_type: undefined,
          time_spent_seconds: 0,
        });
      })
      .catch((err) => {
        // Don't show error if 404 — just means no explanation yet
        if (err?.status !== 404) {
          setError(err?.message || "Failed to load explanation");
        }
      })
      .finally(() => setLoading(false));
  }, [questionId, isCorrect, onTelemetryEvent]);

  // Send telemetry on unmount (time spent)
  useEffect(() => {
    return () => {
      const totalTime = Math.floor((Date.now() - sessionStartRef.current) / 1000);
      if (totalTime > 0 && explanation) {
        onTelemetryEvent?.({
          event_type: "time_spent",
          section_type: undefined,
          time_spent_seconds: totalTime,
        });
      }
    };
  }, [explanation, onTelemetryEvent]);

  const toggleSection = useCallback(
    (sectionType: string) => {
      setExpandedSections((prev) => {
        const next = new Set(prev);
        if (next.has(sectionType)) {
          next.delete(sectionType);
        } else {
          next.add(sectionType);
        }
        return next;
      });
      onTelemetryEvent?.({
        event_type: "section_expanded",
        section_type: sectionType,
        time_spent_seconds: 0,
      });
    },
    [onTelemetryEvent]
  );

  const toggleAll = useCallback(() => {
    if (expandedAll) {
      // Only keep TL;DR expanded
      setExpandedSections(new Set(["tl_dr"]));
    } else {
      setExpandedSections(new Set(explanation?.sections.map((s) => s.section_type) || []));
    }
    setExpandedAll(!expandedAll);
  }, [expandedAll, explanation]);

  const handleCopyCode = useCallback(
    (code: string) => {
      navigator.clipboard.writeText(code);
      onTelemetryEvent?.({
        event_type: "code_copied",
        section_type: "cli_examples",
        time_spent_seconds: 0,
      });
    },
    [onTelemetryEvent]
  );

  const handleDistractorView = useCallback(
    (optionId: string) => {
      const wasSelected = selectedOptionIds.includes(optionId);
      onTelemetryEvent?.({
        event_type: "distractor_viewed",
        section_type: "distractor_analysis",
        distractor_option_id: optionId,
        time_spent_seconds: wasSelected ? 1 : 0,
      });
    },
    [selectedOptionIds, onTelemetryEvent]
  );

  // Parse CLI examples from content (text between ``` markers)
  const parseCLIBlocks = (content: string) => {
    const parts = content.split(/(```[\w]*\n[\s\S]*?```)/g);
    return parts.map((part, i) => {
      const match = part.match(/```(\w*)\n([\s\S]*?)```/);
      if (match) {
        const [, lang, code] = match;
        return (
          <div key={i} className="relative group my-2">
            <div className="flex items-center justify-between px-3 py-1.5 rounded-t-lg bg-zinc-800 dark:bg-zinc-700 text-xs text-zinc-400">
              <span>{lang || "cli"}</span>
              <button
                onClick={() => handleCopyCode(code.trim())}
                className="flex items-center gap-1 text-zinc-500 hover:text-zinc-200 transition-colors"
              >
                <Copy className="h-3 w-3" weight="regular" />
                <span>{t("explanation.copy")}</span>
              </button>
            </div>
            <pre className="p-3 rounded-b-lg bg-zinc-900 dark:bg-zinc-950 text-sm font-mono text-emerald-300 overflow-x-auto border border-zinc-800 leading-relaxed">
              <code>{code.trim()}</code>
            </pre>
          </div>
        );
      }
      // Regular text — handle inline `code`
      const withInlineCode = part.split(/(`[^`]+`)/g).map((segment, j) => {
        if (segment.startsWith("`") && segment.endsWith("`")) {
          return (
            <code
              key={j}
              className="px-1 py-0.5 rounded bg-zinc-200 dark:bg-zinc-700 text-emerald-600 dark:text-emerald-400 text-sm font-mono"
            >
              {segment.slice(1, -1)}
            </code>
          );
        }
        return <span key={j}>{segment}</span>;
      });
      return <p key={i} className="text-sm leading-relaxed mb-2 last:mb-0">{withInlineCode}</p>;
    });
  };

  // Parse distractor_analysis JSON content
  const renderDistractorAnalysis = (content: string) => {
    try {
      const distractors: DistractorAnalysis[] = JSON.parse(content);
      return (
        <div className="space-y-2">
          {distractors.map((d, i) => {
            const isUserSelected = selectedOptionIds.includes(d.option_id);
            return (
              <button
                key={i}
                onClick={() => handleDistractorView(d.option_id)}
                className={`w-full text-left p-3 rounded-lg border text-sm transition-all ${
                  isUserSelected
                    ? "border-red-300 dark:border-red-700 bg-red-50 dark:bg-red-900/10"
                    : "border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800/30 hover:border-zinc-300 dark:hover:border-zinc-600"
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant={isUserSelected ? "danger" : "outline"} className="text-xs font-mono">
                    {d.option_id}
                  </Badge>
                  {d.common_mistake && (
                    <Badge variant="warning" className="text-xs">
                      {t("explanation.commonMistake")}
                    </Badge>
                  )}
                  {isUserSelected && (
                    <Badge variant="danger" className="text-xs">
                      {t("explanation.yourChoice")}
                    </Badge>
                  )}
                </div>
                <p className="text-zinc-700 dark:text-zinc-300">{d.why_wrong}</p>
              </button>
            );
          })}
        </div>
      );
    } catch {
      return <p className="text-sm text-zinc-500">{content}</p>;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center gap-2 py-4 text-sm text-zinc-500">
        <Spinner size="sm" />
        {t("explanation.loading")}
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-2 text-sm text-red-500">
        {t("explanation.error")}
      </div>
    );
  }

  if (!explanation) {
    return null; // No explanation available — silently hide
  }

  const sortedSections = [...explanation.sections].sort((a, b) => a.sort_order - b.sort_order);
  const allExpanded = expandedSections.size === explanation.sections.length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
      className="mt-4 pt-4 border-t border-blue-200 dark:border-blue-800"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-blue-600 dark:text-blue-400" weight="fill" />
          <span className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            {t("explanation.title")}
          </span>
          <Badge variant="outline" className="text-[10px] text-zinc-400 font-mono">
            v{explanation.version}
          </Badge>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={toggleAll}
            className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
          >
            {allExpanded ? t("explanation.collapseAll") : t("explanation.expandAll")}
          </button>
          <Clock className="h-3 w-3 text-zinc-400" weight="regular" />
          <span className="text-[10px] text-zinc-400 font-mono">
            {new Date(explanation.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      {/* Sections */}
      <div className="space-y-1.5">
        {sortedSections.map((section) => {
          const Icon = SECTION_ICONS[section.section_type] || BookOpen;
          const isExpanded = expandedSections.has(section.section_type);

          return (
            <div
              key={section.section_type}
              className="rounded-lg border border-zinc-200 dark:border-zinc-700 overflow-hidden"
            >
              {section.is_collapsible ? (
                <>
                  <button
                    onClick={() => toggleSection(section.section_type)}
                    className="w-full flex items-center justify-between px-3 py-2 bg-zinc-50 dark:bg-zinc-800/30 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-colors text-sm"
                  >
                    <div className="flex items-center gap-2">
                      <Icon
                        className={`h-3.5 w-3.5 text-blue-600 dark:text-blue-400 ${section.section_type === "distractor_analysis" && isCorrect === false ? "text-red-500" : ""}`}
                        weight="fill"
                      />
                      <span className="font-medium text-zinc-700 dark:text-zinc-300">
                        {section.title}
                      </span>
                      {section.section_type === "distractor_analysis" && isCorrect === false && (
                        <Badge variant="danger" className="text-[10px]">
                          {t("explanation.recommended")}
                        </Badge>
                      )}
                    </div>
                    {isExpanded ? (
                      <CaretUp className="h-3.5 w-3.5 text-zinc-400" weight="regular" />
                    ) : (
                      <CaretDown className="h-3.5 w-3.5 text-zinc-400" weight="regular" />
                    )}
                  </button>
                  <AnimatePresence initial={false}>
                    {isExpanded && (
                      <motion.div
                        key="content"
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="overflow-hidden"
                      >
                        <div className="px-3 py-3 space-y-2">
                          {section.section_type === "distractor_analysis"
                            ? renderDistractorAnalysis(section.content)
                            : section.section_type === "cli_examples" || section.section_type === "scenario"
                            ? parseCLIBlocks(section.content)
                            : parseCLIBlocks(section.content)}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </>
              ) : (
                <div className="px-3 py-2 text-sm text-zinc-600 dark:text-zinc-400 bg-blue-50/50 dark:bg-blue-900/5">
                  {parseCLIBlocks(section.content)}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
