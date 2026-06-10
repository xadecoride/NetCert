"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { tracksApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
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
  Funnel,
} from "@phosphor-icons/react";

const trackIcons: Record<string, any> = {
  "junos-ent": Network,
  "junos-sp": Network,
  "junos-sec": ShieldCheck,
  "junos-dc": ComputerTower,
  "junos-aut": Cloud,
  "cisco-ccna": Trophy,
};

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.06 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 100, damping: 20 },
  },
};

export default function ExamsPageWrapper() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    }>
      <ExamsPage />
    </Suspense>
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
  const [loading, setLoading] = useState(true);
  const [activeTrack, setActiveTrack] = useState<string | null>(selectedTrack);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    loadTracks();
  }, [isAuthenticated, authLoading, router]);

  const loadTracks = async () => {
    try {
      const t = await tracksApi.list();
      setTracks(t || []);
      const examMap: Record<string, any[]> = {};
      for (const track of t || []) {
        try {
          const e = await tracksApi.getExams(track.slug);
          examMap[track.slug] = e || [];
        } catch {
          examMap[track.slug] = [];
        }
      }
      setExams(examMap);
    } catch (err) {
      console.error("Failed to load tracks:", err);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    );
  }

  const displayTracks = activeTrack
    ? tracks.filter((t) => t.slug === activeTrack)
    : tracks;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-10">
        <div>
          <Badge variant="secondary" className="mb-3">{t("exams.badge")}</Badge>
          <h1 className="text-4xl font-bold tracking-tighter text-zinc-900 dark:text-white">
            {t("exams.title")}
          </h1>
          <p className="mt-1 text-zinc-500 dark:text-zinc-400">
            {t("exams.subtitle")}
          </p>
        </div>
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap items-center gap-2 mb-8">
        <Funnel className="h-4 w-4 text-zinc-400" weight="regular" />
        {tracks.map((track) => (
          <button
            key={track.slug}
            onClick={() => setActiveTrack(activeTrack === track.slug ? null : track.slug)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
              activeTrack === track.slug
                ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
            }`}
          >
            {track.name}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="flex items-center justify-center min-h-[40dvh]">
          <Spinner />
        </div>
      ) : (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-10"
        >
          {displayTracks.map((track) => {
            const Icon = trackIcons[track.slug] || BookOpen;
            const trackExams = exams[track.slug] || [];
            const isJuniper = track.vendor === "juniper";

            return (
              <motion.div key={track.slug} variants={itemVariants}>
                {/* Track header */}
                <div className="flex items-center gap-4 mb-5">
                  <div className={`p-2.5 rounded-xl ${isJuniper ? "bg-emerald-100 dark:bg-emerald-900/20" : "bg-sky-100 dark:bg-sky-900/20"}`}>
                    <Icon className={`h-5 w-5 ${isJuniper ? "text-emerald-600 dark:text-emerald-400" : "text-sky-600 dark:text-sky-400"}`} weight="fill" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h2 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                        {track.name}
                      </h2>
                      <Badge variant={track.vendor === "juniper" ? "juniper" : "cisco"} className="shrink-0">
                        {track.vendor === "juniper" ? "Juniper" : "Cisco"}
                      </Badge>
                    </div>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">{track.description}</p>
                  </div>
                </div>

                {/* Exams grid — asymmetric 2/3 layout */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {trackExams.map((exam: any, idx: number) => (
                    <Link key={exam.id} href={`/exam/${exam.id}`}>
                      <motion.div
                        whileHover={{ y: -2 }}
                        transition={{ type: "spring", stiffness: 200, damping: 20 }}
                        className="bento-card group cursor-pointer h-full"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <Badge variant="outline" className="font-mono text-xs">{exam.code}</Badge>
                          <Badge variant="secondary" className="text-xs">{exam.level}</Badge>
                        </div>
                        <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-emerald-600 transition-colors">
                          {exam.name}
                        </h3>
                        <div className="flex items-center gap-4 mt-4 text-sm text-zinc-500 dark:text-zinc-400">
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
                        <div className="flex items-center mt-4 text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
                          {t("exams.startExam")} <CaretRight className="h-4 w-4 ml-1" weight="regular" />
                        </div>
                      </motion.div>
                    </Link>
                  ))}
                  {trackExams.length === 0 && (
                    <div className="col-span-full text-center py-12 text-zinc-400 dark:text-zinc-500">
                      <BookOpen className="h-12 w-12 mx-auto mb-3 opacity-40" weight="light" />
                      <p className="text-sm">{t("exams.noExams")}</p>
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      )}
    </div>
  );
}


