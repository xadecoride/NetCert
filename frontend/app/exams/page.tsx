"use client";

import { useState, useEffect, Suspense, useMemo } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { tracksApi, attemptsApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { SpotlightCard } from "@/components/motion/SpotlightCard";
import { PageShell, PageHeader } from "@/components/layout/page-shell";
import {
  BookOpen,
  Clock,
  ChartBar,
  Network,
  ShieldCheck,
  ComputerTower,
  Cloud,
  Trophy,
  CaretRight,
  MagnifyingGlass,
  Funnel,
  CheckCircle,
  X,
} from "@phosphor-icons/react";
import { Spinner } from "@/components/ui/spinner";
import { staggerContainer, fadeInUp } from "@/lib/motion";

const trackIcons: Record<string, any> = {
  "junos-ent": Network,
  "junos-sp": Network,
  "junos-sec": ShieldCheck,
  "junos-dc": ComputerTower,
  "junos-aut": Cloud,
  "cisco-ccna": Trophy,
};

const filters = ["all", "active", "completed"] as const;
type Filter = (typeof filters)[number];

function ExamsSkeleton() {
  return (
    <PageShell>
      <div className="mb-8 md:mb-10">
        <Skeleton className="h-5 w-20 rounded-full mb-3" />
        <Skeleton className="h-10 md:h-14 w-1/2 max-w-md mb-2" />
        <Skeleton className="h-5 w-1/3 max-w-sm" />
      </div>
      <div className="flex flex-wrap items-center gap-3 mb-8">
        <Skeleton className="h-9 w-20 rounded-lg" />
        <Skeleton className="h-9 w-24 rounded-lg" />
        <Skeleton className="h-9 w-24 rounded-lg" />
        <Skeleton className="h-9 w-24 rounded-lg" />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-56 w-full rounded-2xl" />
        ))}
      </div>
    </PageShell>
  );
}

function ExamsPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { t } = useTranslation();
  const router = useRouter();
  const searchParams = useSearchParams();
  const selectedTrack = searchParams.get("track");

  const [tracks, setTracks] = useState<any[]>([]);
  const [exams, setExams] = useState<Record<string, any[]>>({});
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState<Filter>("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    loadData();
  }, [isAuthenticated, authLoading, router]);

  const loadData = async () => {
    try {
      const [tr, h] = await Promise.all([
        tracksApi.list(),
        attemptsApi.history().catch(() => []),
      ]);
      setTracks(tr || []);
      setHistory(h || []);
      const examMap: Record<string, any[]> = {};
      for (const track of tr || []) {
        try {
          const e = await tracksApi.getExams(track.slug);
          examMap[track.slug] = (e || []).map((exam: any) => ({
            ...exam,
            trackSlug: track.slug,
            trackName: track.name,
            trackVendor: track.vendor,
          }));
        } catch {
          examMap[track.slug] = [];
        }
      }
      setExams(examMap);
    } catch (err) {
      console.error("Failed to load exams:", err);
    } finally {
      setLoading(false);
    }
  };

  const examStatus = useMemo(() => {
    const status: Record<string, { completed: boolean; active: boolean }> = {};
    for (const attempt of history) {
      const id = attempt.exam_id;
      if (!id) continue;
      if (!status[id]) status[id] = { completed: false, active: false };
      if (attempt.status === "completed" || attempt.completed_at) {
        status[id].completed = true;
      } else {
        status[id].active = true;
      }
    }
    return status;
  }, [history]);

  const allExams = useMemo(() => {
    return Object.values(exams).flat();
  }, [exams]);

  const filteredExams = useMemo(() => {
    let list = allExams;
    if (selectedTrack) {
      list = list.filter((e) => e.trackSlug === selectedTrack);
    }
    if (activeFilter === "completed") {
      list = list.filter((e) => examStatus[e.id]?.completed);
    } else if (activeFilter === "active") {
      list = list.filter((e) => examStatus[e.id]?.active);
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter(
        (e) =>
          e.name?.toLowerCase().includes(q) ||
          e.code?.toLowerCase().includes(q) ||
          e.description?.toLowerCase().includes(q)
      );
    }
    return list;
  }, [allExams, selectedTrack, activeFilter, search, examStatus]);

  const grouped = useMemo(() => {
    const groups: Record<string, any[]> = {};
    for (const exam of filteredExams) {
      if (!groups[exam.trackSlug]) groups[exam.trackSlug] = [];
      groups[exam.trackSlug].push(exam);
    }
    return groups;
  }, [filteredExams]);

  if (authLoading || loading) {
    return <ExamsSkeleton />;
  }

  return (
    <PageShell className="min-h-[100dvh]">
      <PageHeader
        badge={<Badge variant="secondary">{t("exams.badge")}</Badge>}
        title={t("exams.title")}
        subtitle={t("exams.subtitle")}
      />

      {/* Controls */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8"
      >
        <div className="flex flex-wrap items-center gap-2">
          <Funnel className="h-4 w-4 text-zinc-400" weight="regular" />
          {filters.map((f) => (
            <button
              key={f}
              onClick={() => setActiveFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                activeFilter === f
                  ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                  : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
              }`}
            >
              {f === "all" ? "All" : f === "active" ? "Active" : "Completed"}
            </button>
          ))}
          {selectedTrack && (
            <Badge variant="outline" className="gap-1 pl-2">
              {selectedTrack}
              <button
                onClick={() => router.push("/exams")}
                className="p-0.5 hover:text-emerald-500"
              >
                <X className="h-3 w-3" weight="bold" />
              </button>
            </Badge>
          )}
        </div>
        <div className="w-full md:w-72">
          <Input
            placeholder="Search exams..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            rightElement={<MagnifyingGlass className="h-4 w-4" weight="regular" />}
          />
        </div>
      </motion.div>

      {/* Empty state */}
      {filteredExams.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: "spring", stiffness: 100, damping: 20 }}
          className="flex flex-col items-center justify-center py-24 text-center"
        >
          <div className="p-4 rounded-2xl bg-zinc-100 dark:bg-zinc-800 mb-4">
            <BookOpen className="h-10 w-10 text-zinc-400" weight="light" />
          </div>
          <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-1">
            No exams found
          </h3>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 max-w-xs mb-6">
            Try changing filters or search query.
          </p>
          <Button variant="outline" onClick={() => { setActiveFilter("all"); setSearch(""); }}>
            Clear filters
          </Button>
        </motion.div>
      ) : (
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="space-y-10"
        >
          <AnimatePresence>
            {Object.entries(grouped).map(([slug, trackExams]) => {
              const track = tracks.find((t) => t.slug === slug);
              const Icon = trackIcons[slug] || BookOpen;
              const isJuniper = track?.vendor === "juniper";
              return (
                <motion.div key={slug} variants={fadeInUp}>
                  <div className="flex items-center gap-3 mb-5">
                    <div
                      className={`p-2.5 rounded-xl ${
                        isJuniper
                          ? "bg-emerald-100 dark:bg-emerald-900/20"
                          : "bg-sky-100 dark:bg-sky-900/20"
                      }`}
                    >
                      <Icon
                        className={`h-5 w-5 ${
                          isJuniper
                            ? "text-emerald-600 dark:text-emerald-400"
                            : "text-sky-600 dark:text-sky-400"
                        }`}
                        weight="fill"
                      />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h2 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                          {track?.name || slug}
                        </h2>
                        <Badge variant="outline" className="text-xs">
                          {isJuniper ? "Juniper" : "Cisco"}
                        </Badge>
                      </div>
                      <p className="text-sm text-zinc-500 dark:text-zinc-400">
                        {track?.description}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
                    {trackExams.map((exam) => {
                      const status = examStatus[exam.id];
                      const progress = status?.completed
                        ? 100
                        : status?.active
                        ? 50
                        : 0;
                      return (
                        <Link key={exam.id} href={`/exams/${exam.id}`}>
                          <SpotlightCard className="group cursor-pointer h-full p-5">
                            <div className="flex items-start justify-between mb-4">
                              <Badge variant="outline" className="font-mono text-xs">
                                {exam.code}
                              </Badge>
                              <Badge
                                variant={
                                  status?.completed
                                    ? "success"
                                    : status?.active
                                    ? "warning"
                                    : "secondary"
                                }
                                className="text-xs"
                              >
                                {status?.completed
                                  ? "Completed"
                                  : status?.active
                                  ? "In Progress"
                                  : exam.level}
                              </Badge>
                            </div>
                            <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-emerald-600 transition-colors mb-2">
                              {exam.name}
                            </h3>
                            <p className="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2 mb-4">
                              {exam.description || "Practice exam for certification preparation."}
                            </p>
                            <div className="flex items-center gap-4 text-xs text-zinc-500 dark:text-zinc-400 mb-4">
                              <span className="flex items-center gap-1.5">
                                <BookOpen className="h-3.5 w-3.5" weight="regular" />
                                {exam.total_questions} {t("exams.questions")}
                              </span>
                              <span className="flex items-center gap-1.5">
                                <Clock className="h-3.5 w-3.5" weight="regular" />
                                {exam.duration_minutes} {t("exams.min")}
                              </span>
                              <span className="flex items-center gap-1.5">
                                <ChartBar className="h-3.5 w-3.5" weight="regular" />
                                {exam.passing_score}%
                              </span>
                            </div>
                            <div className="space-y-1.5 mb-4">
                              <div className="flex items-center justify-between text-xs">
                                <span className="text-zinc-500 dark:text-zinc-400">Progress</span>
                                <span className="font-mono text-zinc-700 dark:text-zinc-300">
                                  {progress}%
                                </span>
                              </div>
                              <div className="w-full h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                                <motion.div
                                  className="h-full rounded-full bg-emerald-500"
                                  initial={{ width: 0 }}
                                  animate={{ width: `${progress}%` }}
                                  transition={{ duration: 0.8, ease: "easeOut" }}
                                />
                              </div>
                            </div>
                            <div className="flex items-center text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
                              {t("exams.startExam")}
                              <CaretRight className="h-4 w-4 ml-1" weight="regular" />
                            </div>
                          </SpotlightCard>
                        </Link>
                      );
                    })}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      )}
    </PageShell>
  );
}

export default function ExamsPageWrapper() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[60dvh]">
          <Spinner className="h-8 w-8 animate-spin text-emerald-500" />
        </div>
      }
    >
      <ExamsPage />
    </Suspense>
  );
}
