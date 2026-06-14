"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen,
  MagnifyingGlass,
  Network,
  ShieldCheck,
  ComputerTower,
  Cloud,
  Trophy,
  CaretDown,
  CheckCircle,
  Circle,
  Code,
  Copy,
  Check,
  ArrowsDownUp,
  Gauge,
  Terminal,
} from "@phosphor-icons/react";

import { useAuth } from "@/lib/auth-context";
import { withAuth } from "@/lib/with-auth";
import { useTranslation } from "@/lib/i18n/context";
import { useStudyContent } from "@/lib/i18n/use-study-content";
import type { GuideSection, TechnologyGuide } from "@/lib/i18n/study-content";
import { tracksApi, studyProgressApi } from "@/lib/api";
import { springTransition, staggerContainer, fadeInUp } from "@/lib/motion";

import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { BentoCard } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { SectionReveal } from "@/components/motion/SectionReveal";
import { SpotlightCard } from "@/components/motion/SpotlightCard";

const trackIcons: Record<string, React.ElementType> = {
  "junos-ent": Network,
  "junos-sp": Network,
  "junos-sec": ShieldCheck,
  "junos-dc": ComputerTower,
  "junos-aut": Cloud,
  "cisco": Trophy,
};

const trackLabels: Record<string, string> = {
  "junos-ent": "Enterprise",
  "junos-sp": "Service Provider",
  "junos-sec": "Security",
  "junos-dc": "Data Center",
  "junos-aut": "Automation",
  "cisco": "Cisco",
};

const sectionBg: Record<GuideSection["type"], string> = {
  text: "",
  code: "bg-zinc-900 dark:bg-zinc-950 border border-zinc-800",
  command: "bg-black border border-zinc-800",
  note: "bg-sky-900/10 border border-sky-800/20",
  tip: "bg-emerald-900/10 border border-emerald-800/20",
  warning: "bg-amber-900/10 border border-amber-800/20",
};

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      }}
      className="absolute top-2 right-2 p-1.5 rounded-lg bg-zinc-800/50 hover:bg-zinc-700 text-zinc-400 hover:text-zinc-200 transition-all opacity-0 group-hover:opacity-100"
      title="Copy"
    >
      {copied ? (
        <Check className="h-3.5 w-3.5 text-emerald-400" weight="bold" />
      ) : (
        <Copy className="h-3.5 w-3.5" weight="regular" />
      )}
    </button>
  );
}

function SectionBlock({ section }: { section: GuideSection }) {
  if (section.type === "code" || section.type === "command") {
    return (
      <div className="relative group">
        <pre
          className={`${sectionBg[section.type]} text-zinc-200 font-mono text-sm p-4 rounded-xl overflow-x-auto leading-relaxed`}
        >
          <code>{section.content}</code>
        </pre>
        <CopyButton text={section.content} />
      </div>
    );
  }

  if (section.type === "note" || section.type === "tip" || section.type === "warning") {
    const icon =
      section.type === "note" ? (
        <BookOpen className="h-4 w-4 text-sky-400 shrink-0 mt-0.5" weight="fill" />
      ) : section.type === "tip" ? (
        <Check className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" weight="bold" />
      ) : (
        <ArrowsDownUp className="h-4 w-4 text-amber-400 shrink-0 mt-0.5" weight="fill" />
      );
    return (
      <div className={`${sectionBg[section.type]} rounded-xl p-4 flex gap-3`}>
        {icon}
        <p className="text-sm text-zinc-300 whitespace-pre-wrap leading-relaxed">{section.content}</p>
      </div>
    );
  }

  return <p className="text-zinc-300 leading-relaxed text-sm">{section.content}</p>;
}

function TopicDetail({ guide, completed, onToggle }: { guide: TechnologyGuide; completed: boolean; onToggle: () => void }) {
  const { t } = useTranslation();
  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      transition={springTransition}
      className="overflow-hidden"
    >
      <div className="pt-4 space-y-4">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Badge variant="secondary">{guide.level}</Badge>
            <Badge variant="outline">{guide.technology}</Badge>
          </div>
          <Button
            variant={completed ? "secondary" : "primary"}
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            {completed ? (
              <>
                <CheckCircle className="h-4 w-4" weight="fill" />
                {t("studyPage.completed")}
              </>
            ) : (
              <>
                <Circle className="h-4 w-4" weight="regular" />
                {t("studyPage.markAsCompleted")}
              </>
            )}
          </Button>
        </div>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">{guide.summary}</p>
        <div className="space-y-4">
          {guide.sections.map((section, idx) => (
            <div key={idx} className="space-y-2">
              {section.title && (
                <h4 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                  {section.type === "code" || section.type === "command" ? (
                    <Code className="h-3.5 w-3.5 text-emerald-500" weight="fill" />
                  ) : null}
                  {section.title}
                </h4>
              )}
              <SectionBlock section={section} />
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function StudyPageContent() {
  const { t } = useTranslation();
  const studyContent = useStudyContent();
  const guides = studyContent.guides;

  const [tracks, setTracks] = useState<any[]>([]);
  const [activeTrack, setActiveTrack] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [completedGuides, setCompletedGuides] = useState<Set<string>>(new Set());
  const [saving, setSaving] = useState<Set<string>>(new Set());

  useEffect(() => {
    tracksApi.list().then(setTracks).catch(() => {});
    studyProgressApi
      .getProgress()
      .then((progress) => setCompletedGuides(new Set(progress.map((p: any) => p.guide_id))))
      .catch(() => {});
  }, []);

  const filteredGuides = useMemo(() => {
    return guides.filter((g) => {
      if (activeTrack !== "all" && g.track !== activeTrack) return false;
      if (!searchQuery) return true;
      const q = searchQuery.toLowerCase();
      return (
        g.title.toLowerCase().includes(q) ||
        g.summary.toLowerCase().includes(q) ||
        g.sections.some((s) => s.content.toLowerCase().includes(q))
      );
    });
  }, [guides, activeTrack, searchQuery]);

  const completedCount = guides.filter((g) => completedGuides.has(g.id)).length;
  const progressPercent = guides.length ? Math.round((completedCount / guides.length) * 100) : 0;

  const toggleGuide = async (guideId: string) => {
    const nextCompleted = new Set(completedGuides);
    const willComplete = !nextCompleted.has(guideId);
    if (willComplete) nextCompleted.add(guideId);
    else nextCompleted.delete(guideId);
    setSaving((prev) => new Set(prev).add(guideId));
    setCompletedGuides(nextCompleted);
    try {
      await studyProgressApi.toggleGuide({ guide_id: guideId, completed: willComplete });
    } catch {
      setCompletedGuides(completedGuides);
    } finally {
      setSaving((prev) => {
        const next = new Set(prev);
        next.delete(guideId);
        return next;
      });
    }
  };

  return (
    <PageShell className="min-h-[100dvh]">
      <PageHeader
        badge={
          <Badge variant="secondary">
            <BookOpen className="h-3 w-3 mr-1" weight="fill" />
            {t("studyPage.badge")}
          </Badge>
        }
        title={t("studyPage.title")}
        subtitle={t("studyPage.subtitle")}
      />

      <SectionReveal>
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 mb-10">
          <div className="flex-1">
            {guides.length > 0 && (
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 text-sm font-medium text-zinc-700 dark:text-zinc-300">
                    <Gauge className="h-4 w-4 text-emerald-500" weight="fill" />
                    {t("studyPage.studyProgress")}
                  </div>
                  <span className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                    {completedCount} / {guides.length} ({progressPercent}%)
                  </span>
                </div>
                <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-emerald-500 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progressPercent}%` }}
                    transition={{ type: "spring", stiffness: 100, damping: 20 }}
                  />
                </div>
              </div>
            )}

            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => setActiveTrack("all")}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                  activeTrack === "all"
                    ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                    : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
                }`}
              >
                All tracks
              </button>
              {tracks.map((track) => (
                <button
                  key={track.slug}
                  onClick={() => setActiveTrack(track.slug)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                    activeTrack === track.slug
                      ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                      : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
                  }`}
                >
                  {track.name}
                </button>
              ))}
            </div>
          </div>

          <div className="w-full lg:w-80">
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={t("studyPage.searchPlaceholder")}
              rightElement={<MagnifyingGlass className="h-4 w-4" weight="regular" />}
            />
          </div>
        </div>
      </SectionReveal>

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
      >
        <AnimatePresence mode="popLayout">
          {filteredGuides.map((guide) => {
            const Icon = trackIcons[guide.track] || BookOpen;
            const isExpanded = expandedId === guide.id;
            const completed = completedGuides.has(guide.id);
            return (
              <motion.div
                key={guide.id}
                layout
                variants={fadeInUp}
                className="contents"
              >
                <SpotlightCard className="h-full">
                  <BentoCard className="h-full flex flex-col p-0 bg-transparent border-0 shadow-none">
                    <button
                      onClick={() => setExpandedId(isExpanded ? null : guide.id)}
                      className="text-left w-full p-6 flex flex-col h-full"
                    >
                      <div className="flex items-start justify-between gap-3 mb-4">
                        <div className="p-2.5 rounded-xl bg-emerald-100 dark:bg-emerald-900/20">
                          <Icon className="h-5 w-5 text-emerald-600 dark:text-emerald-400" weight="fill" />
                        </div>
                        <div className="flex items-center gap-1.5">
                          {completed ? (
                            <CheckCircle className="h-5 w-5 text-emerald-500" weight="fill" />
                          ) : (
                            <Circle className="h-5 w-5 text-zinc-300 dark:text-zinc-600" weight="regular" />
                          )}
                          <CaretDown
                            className={`h-4 w-4 text-zinc-400 transition-transform ${isExpanded ? "rotate-180" : ""}`}
                            weight="bold"
                          />
                        </div>
                      </div>

                      <h3 className="font-semibold text-lg text-zinc-900 dark:text-zinc-100 mb-1">
                        {guide.title}
                      </h3>
                      <p className="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2 flex-1">
                        {guide.summary}
                      </p>

                      <div className="flex items-center gap-2 mt-4">
                        <Badge variant="outline">{guide.level}</Badge>
                        <Badge variant="secondary">{trackLabels[guide.track] || guide.track}</Badge>
                      </div>

                      <AnimatePresence>
                        {isExpanded && (
                          <TopicDetail
                            guide={guide}
                            completed={completed}
                            onToggle={() => toggleGuide(guide.id)}
                          />
                        )}
                      </AnimatePresence>
                    </button>
                  </BentoCard>
                </SpotlightCard>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </motion.div>

      {filteredGuides.length === 0 && (
        <SectionReveal className="text-center py-20">
          <BookOpen className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
            {t("studyPage.noGuidesFound")}
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400">{t("studyPage.tryChangingFilters")}</p>
        </SectionReveal>
      )}
    </PageShell>
  );
}

function StudyPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner />
        </div>
      }
    >
      <StudyPageContent />
    </Suspense>
  );
}

export default withAuth(StudyPage);
