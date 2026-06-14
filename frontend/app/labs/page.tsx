"use client";

import { useEffect, useMemo, useState, Suspense } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Lightning,
  Clock,
  Network,
  ShieldCheck,
  ComputerTower,
  Cloud,
  Trophy,
  CaretRight,
  ListChecks,
  Spinner,
} from "@phosphor-icons/react";

import { withAuth } from "@/lib/with-auth";
import { useTranslation } from "@/lib/i18n/context";
import { tracksApi, quickLabsApi } from "@/lib/api";
import { springTransition, staggerContainer, fadeInUp } from "@/lib/motion";

import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton, SkeletonText } from "@/components/ui/skeleton";
import { BentoCard } from "@/components/ui/card";
import { SpotlightCard } from "@/components/motion/SpotlightCard";
import { SectionReveal } from "@/components/motion/SectionReveal";

const trackIcons: Record<string, React.ElementType> = {
  "junos-ent": Network,
  "junos-sp": Network,
  "junos-sec": ShieldCheck,
  "junos-dc": ComputerTower,
  "junos-aut": Cloud,
  "cisco": Trophy,
};

const difficultyLabels = ["", "Beginner", "Easy", "Medium", "Hard", "Expert"];

interface QuickLab {
  id: string;
  slug: string;
  title: string;
  description: string;
  level: string;
  technology: string;
  difficulty: number;
  estimated_minutes: number;
  track_slug?: string;
}

function getDifficultyVariant(d: number) {
  if (d <= 2) return "success";
  if (d === 3) return "warning";
  return "danger";
}

function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      {Array.from({ length: 6 }).map((_, i) => (
        <BentoCard key={i} className="h-60 flex flex-col">
          <div className="flex items-start justify-between mb-4">
            <Skeleton className="h-10 w-10 rounded-xl" />
            <Skeleton className="h-5 w-20 rounded-full" />
          </div>
          <Skeleton className="h-5 w-3/4 mb-2" />
          <SkeletonText lines={2} />
          <div className="mt-auto flex items-center gap-3 pt-4">
            <Skeleton className="h-4 w-16" />
            <Skeleton className="h-4 w-16" />
          </div>
        </BentoCard>
      ))}
    </div>
  );
}

function LabsPageContent() {
  const { t } = useTranslation();

  const [tracks, setTracks] = useState<any[]>([]);
  const [quickLabs, setQuickLabs] = useState<QuickLab[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTrack, setActiveTrack] = useState<string>("all");

  useEffect(() => {
    const load = async () => {
      try {
        const tData = await tracksApi.list();
        setTracks(tData || []);

        const all: QuickLab[] = [];
        for (const track of tData || []) {
          try {
            const list = await quickLabsApi.list(track.id);
            all.push(
              ...(list || []).map((l: QuickLab) => ({
                ...l,
                track_slug: (l as any).track_slug || track.slug,
              }))
            );
          } catch {
            // ignore per-track errors
          }
        }
        setQuickLabs(all);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load labs");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = useMemo(() => {
    if (activeTrack === "all") return quickLabs;
    return quickLabs.filter((l) => l.track_slug === activeTrack);
  }, [quickLabs, activeTrack]);

  return (
    <PageShell className="min-h-[100dvh]">
      <PageHeader
        badge={
          <Badge variant="secondary">
            <Lightning className="h-3 w-3 mr-1" weight="fill" />
            {t("labs.badge")}
          </Badge>
        }
        title={t("labs.title")}
        subtitle={t("labs.subtitle")}
      />

      <SectionReveal className="mb-8">
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setActiveTrack("all")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
              activeTrack === "all"
                ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
                : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
            }`}
          >
            {t("exams.allTracks")}
          </button>
          {tracks.map((track) => {
            const Icon = trackIcons[track.slug] || ComputerTower;
            return (
              <button
                key={track.slug}
                onClick={() => setActiveTrack(track.slug)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                  activeTrack === track.slug
                    ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                    : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700"
                }`}
              >
                <Icon className="h-3.5 w-3.5" weight="fill" />
                {track.name}
              </button>
            );
          })}
        </div>
      </SectionReveal>

      {error && (
        <SectionReveal className="mb-6 p-4 rounded-xl bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-900/30 text-red-600 dark:text-red-300 text-sm">
          {error}
        </SectionReveal>
      )}

      {loading ? (
        <LoadingSkeleton />
      ) : (
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
        >
          <AnimatePresence mode="popLayout">
            {filtered.map((lab) => {
              const track = tracks.find((tr) => tr.slug === lab.track_slug);
              const Icon = track ? trackIcons[track.slug] || Lightning : Lightning;
              return (
                <motion.div key={lab.id} layout variants={fadeInUp} transition={springTransition}>
                  <SpotlightCard className="h-full">
                    <BentoCard className="h-full flex flex-col p-0 bg-transparent border-0 shadow-none">
                      <div className="p-6 flex flex-col h-full">
                        <div className="flex items-start justify-between gap-3 mb-4">
                          <div className="p-2.5 rounded-xl bg-emerald-100 dark:bg-emerald-900/20">
                            <Icon className="h-5 w-5 text-emerald-600 dark:text-emerald-400" weight="fill" />
                          </div>
                          <div className="flex gap-1.5 flex-wrap justify-end">
                            <Badge variant="outline">{lab.level}</Badge>
                            <Badge variant={getDifficultyVariant(lab.difficulty)}>
                              {difficultyLabels[lab.difficulty] || "Unknown"}
                            </Badge>
                          </div>
                        </div>

                        <h3 className="font-semibold text-lg text-zinc-900 dark:text-zinc-100 mb-1">
                          {lab.title}
                        </h3>
                        <p className="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2 flex-1">
                          {lab.description || "Short practice lab."}
                        </p>

                        <div className="flex items-center gap-3 mt-4 pt-4 border-t border-zinc-200 dark:border-zinc-800 text-sm text-zinc-500 dark:text-zinc-400">
                          <span className="flex items-center gap-1.5">
                            <ListChecks className="h-3.5 w-3.5" weight="regular" />
                            Guided
                          </span>
                          <span className="flex items-center gap-1.5">
                            <Clock className="h-3.5 w-3.5" weight="regular" />
                            {lab.estimated_minutes || 0}m
                          </span>
                        </div>

                        <div className="mt-4">
                          <Link href={`/labs/${lab.id}`}>
                            <Button className="w-full group" size="sm">
                              <Lightning className="h-3.5 w-3.5 mr-1.5" weight="fill" />
                              {t("labs.start")}
                              <CaretRight className="h-4 w-4 ml-auto transition-transform group-hover:translate-x-0.5" weight="regular" />
                            </Button>
                          </Link>
                        </div>
                      </div>
                    </BentoCard>
                  </SpotlightCard>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      )}

      {!loading && filtered.length === 0 && (
        <SectionReveal className="text-center py-20">
          <Lightning className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
            {t("labs.noLabs")}
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400 mb-6">{t("labs.noLabsDesc")}</p>
          <Button variant="outline" onClick={() => setActiveTrack("all")}>
            {t("labs.viewAll")}
          </Button>
        </SectionReveal>
      )}
    </PageShell>
  );
}

function LabsPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
        </div>
      }
    >
      <LabsPageContent />
    </Suspense>
  );
}

export default withAuth(LabsPage);
