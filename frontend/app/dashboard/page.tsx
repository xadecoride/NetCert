"use client";

import { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi, tracksApi, studyProgressApi, labsApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BentoCard } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { AnimatedCounter } from "@/components/motion/AnimatedCounter";
import {
  ChartBar,
  BookOpen,
  TrendUp,
  CheckCircle,
  Trophy,
  Lightning,
  Target,
  Network,
  CaretRight,
  XCircle,
  Warning,
  Book,
  ArrowClockwise,
  Exam,
  Flask,
} from "@phosphor-icons/react";
import { staggerContainer, fadeInUp } from "@/lib/motion";

const guideTracks: Record<string, string> = {
  "junos-cli": "junos-ent",
  "ospf": "junos-ent",
  "bgp": "junos-ent",
  "isis": "junos-ent",
  "mpls": "junos-ent",
  "vlan": "junos-ent",
  "multicast": "junos-ent",
  "firewall-filters": "junos-sec",
  "ipsec-vpn": "junos-sec",
  "evpn-vxlan": "junos-dc",
  "vrf": "junos-sp",
  "bgp-lu": "junos-sp",
};

function formatDate(locale: string, iso: string) {
  return new Date(iso).toLocaleDateString(locale === "ru" ? "ru-RU" : "en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function DashboardSkeleton() {
  return (
    <PageShell>
      <div className="mb-8 md:mb-10">
        <Skeleton className="h-5 w-24 rounded-full mb-3" />
        <Skeleton className="h-10 md:h-14 w-3/4 max-w-lg mb-2" />
        <Skeleton className="h-5 w-1/2 max-w-md" />
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-28 w-full rounded-2xl" />
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <Skeleton className="h-80 w-full rounded-2xl" />
          <Skeleton className="h-72 w-full rounded-2xl" />
        </div>
        <div className="space-y-6">
          <Skeleton className="h-56 w-full rounded-2xl" />
          <Skeleton className="h-56 w-full rounded-2xl" />
          <Skeleton className="h-48 w-full rounded-2xl" />
        </div>
      </div>
    </PageShell>
  );
}

export default function DashboardPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const { t, locale } = useTranslation();
  const router = useRouter();

  const [history, setHistory] = useState<any[]>([]);
  const [tracks, setTracks] = useState<any[]>([]);
  const [completedGuides, setCompletedGuides] = useState<Set<string>>(new Set());
  const [labSessions, setLabSessions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    const [h, tr, p, labs] = await Promise.all([
      attemptsApi.history().catch(() => []),
      tracksApi.list().catch(() => []),
      studyProgressApi.getProgress().catch(() => []),
      labsApi.getActive().catch(() => []),
    ]);
    setHistory(h || []);
    setTracks(tr || []);
    setCompletedGuides(new Set((p || []).map((item: any) => item.guide_id)));
    setLabSessions(labs || []);
    setLoading(false);
  };

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    if (isAuthenticated) {
      loadData();
    }
  }, [isAuthenticated, authLoading, router]);

  const trackStudyStats = useMemo(() => {
    const stats: Record<string, { total: number; completed: number }> = {};
    for (const [guideId, trackSlug] of Object.entries(guideTracks)) {
      if (!stats[trackSlug]) stats[trackSlug] = { total: 0, completed: 0 };
      stats[trackSlug].total++;
      if (completedGuides.has(guideId)) stats[trackSlug].completed++;
    }
    return stats;
  }, [completedGuides]);

  if (authLoading || loading) {
    return <DashboardSkeleton />;
  }

  const totalAttempts = history.length;
  const passedAttempts = history.filter((a) => a.score && a.score >= 70).length;
  const avgScore =
    totalAttempts > 0
      ? Math.round(history.reduce((s, a) => s + (a.score || 0), 0) / totalAttempts)
      : 0;
  const completedLabs = labSessions.filter((l) => l.status === "completed" || l.status === "graded").length;

  const chartData = history
    .slice(0, 7)
    .map((a, i) => ({
      name: `T${i + 1}`,
      score: Math.round(a.score || 0),
      date: formatDate(locale, a.started_at),
    }))
    .reverse();

  return (
    <PageShell className="min-h-[100dvh]">
      <PageHeader
        badge={<Badge variant="secondary">{t("dashboard.badge")}</Badge>}
        title={
          <>
            {t("dashboard.welcomeBack")},{" "}
            <span className="text-emerald-500">
              {user?.display_name?.split(" ")[0] || t("dashboard.engineer")}
            </span>
          </>
        }
        subtitle={t("dashboard.subtitle")}
        className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4"
      >
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={loadData}>
            <ArrowClockwise className="h-4 w-4 mr-2" weight="regular" />
            Refresh
          </Button>
        </div>
      </PageHeader>

      {/* Stats row */}
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
      >
        {[
          {
            icon: Lightning,
            label: t("dashboard.streakLabel"),
            value: user?.streak_days || 0,
            suffix: "d",
            color: "text-amber-500",
            bg: "bg-amber-100 dark:bg-amber-900/20",
          },
          {
            icon: BookOpen,
            label: t("dashboard.examsTaken"),
            value: totalAttempts,
            suffix: "",
            color: "text-emerald-500",
            bg: "bg-emerald-100 dark:bg-emerald-900/20",
          },
          {
            icon: TrendUp,
            label: t("dashboard.avgScore"),
            value: avgScore,
            suffix: "%",
            color: "text-zinc-900 dark:text-white",
            bg: "bg-zinc-100 dark:bg-zinc-800",
          },
          {
            icon: Flask,
            label: "Completed Labs",
            value: completedLabs,
            suffix: "",
            color: "text-sky-500",
            bg: "bg-sky-100 dark:bg-sky-900/20",
          },
        ].map((stat) => {
          const Icon = stat.icon;
          return (
            <motion.div key={stat.label} variants={fadeInUp}>
              <BentoCard className="h-full">
                <div className="flex items-center gap-3">
                  <div className={`p-2.5 rounded-xl ${stat.bg}`}>
                    <Icon className={`h-5 w-5 ${stat.color}`} weight="fill" />
                  </div>
                  <div>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400">{stat.label}</p>
                    <p className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-white">
                      <AnimatedCounter value={stat.value} suffix={stat.suffix} />
                    </p>
                  </div>
                </div>
              </BentoCard>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Main content — asymmetric grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left column */}
        <div className="lg:col-span-8 space-y-8">
          {/* Chart */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.1 }}
          >
            <BentoCard>
              <div className="flex items-center gap-2 mb-6">
                <ChartBar className="h-5 w-5 text-emerald-500" weight="fill" />
                <h2 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
                  Last 7 Exam Scores
                </h2>
              </div>
              {chartData.length > 0 ? (
                <div className="h-56 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} margin={{ top: 8, right: 8, bottom: 8, left: -8 }}>
                      <XAxis
                        dataKey="name"
                        tick={{ fill: "currentColor", fontSize: 12 }}
                        stroke="currentColor"
                        className="text-zinc-400"
                      />
                      <YAxis
                        domain={[0, 100]}
                        tick={{ fill: "currentColor", fontSize: 12 }}
                        stroke="currentColor"
                        className="text-zinc-400"
                      />
                      <Tooltip
                        cursor={{ fill: "rgba(16,185,129,0.06)" }}
                        contentStyle={{
                          background: "rgba(24,24,27,0.9)",
                          border: "1px solid rgba(63,63,70,0.5)",
                          borderRadius: "0.75rem",
                          color: "#fff",
                        }}
                        formatter={(value: number) => [`${value}%`, "Score"]}
                        labelFormatter={(_, payload: any) =>
                          payload?.[0]?.payload?.date || ""
                        }
                      />
                      <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                        {chartData.map((entry, index) => (
                          <Cell
                            key={`cell-${index}`}
                            fill={entry.score >= 70 ? "#10b981" : "#ef4444"}
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="h-56 flex flex-col items-center justify-center text-zinc-400 dark:text-zinc-500">
                  <ChartBar className="h-12 w-12 mb-3 opacity-40" weight="light" />
                  <p className="text-sm">No scores to chart yet.</p>
                </div>
              )}
            </BentoCard>
          </motion.div>

          {/* Recent attempts */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.2 }}
          >
            <BentoCard>
              <div className="flex items-center gap-2 mb-6">
                <Exam className="h-5 w-5 text-emerald-500" weight="fill" />
                <h2 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
                  {t("dashboard.recentAttempts")}
                </h2>
              </div>
              {history.length === 0 ? (
                <div className="text-center py-10 text-zinc-400 dark:text-zinc-500">
                  <BookOpen className="h-12 w-12 mx-auto mb-3 opacity-40" weight="light" />
                  <p className="text-sm mb-4">{t("dashboard.noAttempts")}</p>
                  <Link href="/exams">
                    <Button variant="outline" size="sm">
                      {t("dashboard.startFirstExam")}
                    </Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-2">
                  {history.slice(0, 5).map((attempt) => (
                    <Link
                      key={attempt.id}
                      href={`/review/${attempt.id}`}
                      className="flex items-center justify-between p-3 rounded-xl hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors group"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        {attempt.score && attempt.score >= 70 ? (
                          <CheckCircle className="h-5 w-5 text-emerald-500 shrink-0" weight="fill" />
                        ) : attempt.score ? (
                          <XCircle className="h-5 w-5 text-red-500 shrink-0" weight="fill" />
                        ) : (
                          <Warning className="h-5 w-5 text-amber-500 shrink-0" weight="fill" />
                        )}
                        <div className="min-w-0">
                          <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100 truncate">
                            {attempt.exam_id?.substring(0, 8)}...
                          </p>
                          <p className="text-xs text-zinc-500 dark:text-zinc-400">
                            {formatDate(locale, attempt.started_at)} ·{" "}
                            {attempt.questions_answered}/{attempt.questions_total}{" "}
                            {t("dashboard.answered")}
                          </p>
                        </div>
                      </div>
                      {attempt.score !== null && (
                        <span
                          className={`text-sm font-semibold font-mono shrink-0 ${
                            attempt.score >= 70 ? "text-emerald-500" : "text-red-500"
                          }`}
                        >
                          {Math.round(attempt.score)}%
                        </span>
                      )}
                    </Link>
                  ))}
                </div>
              )}
            </BentoCard>
          </motion.div>
        </div>

        {/* Right column */}
        <div className="lg:col-span-4 space-y-8">
          {/* Track progress */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.25 }}
          >
            <BentoCard>
              <div className="flex items-center gap-2 mb-1">
                <Network className="h-5 w-5 text-emerald-500" weight="fill" />
                <h2 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
                  {t("dashboard.certTracks")}
                </h2>
              </div>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-6">
                {t("dashboard.studyProgressDesc")}
              </p>
              {tracks.length === 0 ? (
                <div className="text-center py-6 text-zinc-400 dark:text-zinc-500">
                  <Network className="h-10 w-10 mx-auto mb-2 opacity-40" weight="light" />
                  <p className="text-xs">{t("dashboard.noTracks")}</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {tracks.map((track) => {
                    const stats = trackStudyStats[track.slug];
                    const pct =
                      stats && stats.total > 0
                        ? Math.round((stats.completed / stats.total) * 100)
                        : 0;
                    return (
                      <div key={track.slug} className="space-y-1.5">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-sm text-zinc-700 dark:text-zinc-300 truncate">
                            {track.name}
                          </span>
                          <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 shrink-0">
                            {stats ? `${stats.completed}/${stats.total}` : "0/0"}
                          </span>
                        </div>
                        <div className="w-full h-2 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                          <motion.div
                            className="h-full rounded-full bg-emerald-500"
                            initial={{ width: 0 }}
                            animate={{ width: `${pct}%` }}
                            transition={{ duration: 0.8, ease: "easeOut" }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </BentoCard>
          </motion.div>

          {/* Quick links */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.3 }}
          >
            <BentoCard>
              <div className="flex items-center gap-2 mb-6">
                <Target className="h-5 w-5 text-emerald-500" weight="fill" />
                <h2 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
                  {t("dashboard.quickActions")}
                </h2>
              </div>
              <div className="space-y-2">
                <Link href="/exams">
                  <Button variant="primary" size="sm" className="w-full justify-start">
                    <BookOpen className="h-4 w-4 mr-2" weight="regular" />
                    {t("dashboard.startPractice")}
                  </Button>
                </Link>
                <Link href="/exams?track=junos-ent">
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Network className="h-4 w-4 mr-2" weight="regular" />
                    {t("dashboard.juniaTrack")}
                  </Button>
                </Link>
                <Link href="/exams?track=cisco-ccna">
                  <Button variant="outline" size="sm" className="w-full justify-start">
                    <Trophy className="h-4 w-4 mr-2" weight="regular" />
                    {t("dashboard.ccnaTrack")}
                  </Button>
                </Link>
              </div>
            </BentoCard>
          </motion.div>

          {/* Achievements */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.35 }}
          >
            <BentoCard>
              <div className="flex items-center gap-2 mb-6">
                <Trophy className="h-5 w-5 text-emerald-500" weight="fill" />
                <h2 className="text-lg font-semibold tracking-tight text-zinc-900 dark:text-white">
                  {t("dashboard.achievements")}
                </h2>
              </div>
              <div className="space-y-2">
                {[
                  { name: t("dashboard.firstExam"), icon: BookOpen, done: totalAttempts > 0 },
                  {
                    name: t("dashboard.perfectScore"),
                    icon: Trophy,
                    done: history.some((a) => a.score === 100),
                  },
                  {
                    name: t("dashboard.studyStreak"),
                    icon: Lightning,
                    done: (user?.streak_days || 0) >= 7,
                  },
                  {
                    name: t("dashboard.jackOfAll"),
                    icon: Network,
                    done: new Set(history.map((a) => a.exam_id)).size >= 3,
                  },
                ].map((ach) => {
                  const Icon = ach.icon;
                  return (
                    <div
                      key={ach.name}
                      className={`flex items-center gap-3 p-2 rounded-xl transition-opacity ${
                        ach.done ? "opacity-100" : "opacity-40"
                      }`}
                    >
                      <Icon
                        className={`h-4 w-4 ${ach.done ? "text-emerald-500" : "text-zinc-400"}`}
                        weight={ach.done ? "fill" : "regular"}
                      />
                      <span className="text-sm text-zinc-700 dark:text-zinc-300">{ach.name}</span>
                    </div>
                  );
                })}
              </div>
            </BentoCard>
          </motion.div>
        </div>
      </div>
    </PageShell>
  );
}
