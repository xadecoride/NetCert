"use client";

import { useState, useEffect, useMemo } from "react"; 
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { attemptsApi, tracksApi, studyProgressApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
import {
  ChartBar,
  BookOpen,
  TrendUp,
  Clock,
  Trophy,
  Lightning,
  Target,
  Network,
  CaretRight,
  CheckCircle,
  XCircle,
  Warning,
  SignOut,
  Book,
} from "@phosphor-icons/react";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
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

export default function DashboardPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const { t, locale } = useTranslation();
  const router = useRouter();
  const [history, setHistory] = useState<any[]>([]);
  const [tracks, setTracks] = useState<any[]>([]);
  const [completedGuides, setCompletedGuides] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    if (isAuthenticated) {
      Promise.all([
        attemptsApi.history().catch(() => []),
        tracksApi.list().catch(() => []),
        studyProgressApi.getProgress().catch(() => []),
      ]).then(([h, t, p]) => {
        setHistory(h || []);
        setTracks(t || []);
        setCompletedGuides(new Set((p || []).map((item: any) => item.guide_id)));
        setLoading(false);
      });
    }
  }, [isAuthenticated, authLoading, router]);

  // Guide → track mapping for study progress
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

  // Per-track study progress stats (moved BEFORE early return to satisfy Rules of Hooks)
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
    return (
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    );
  }

  const totalAttempts = history.length;
  const passedAttempts = history.filter((a) => a.score && a.score >= 70).length;
  const avgScore =
    totalAttempts > 0
      ? Math.round(history.reduce((s, a) => s + (a.score || 0), 0) / totalAttempts)
      : 0;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8"
      >
        <div>
          <Badge variant="secondary" className="mb-3">{t("dashboard.badge")}</Badge>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tighter text-zinc-900 dark:text-white">
            {t("dashboard.welcomeBack")}, {user?.display_name?.split(" ")[0] || t("dashboard.engineer")}
          </h1>
          <p className="mt-1 text-zinc-500 dark:text-zinc-400">
            {t("dashboard.subtitle")}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-100 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 text-sm font-medium">
            <Lightning className="h-4 w-4" weight="fill" />
            {user?.total_xp || 0} {t("dashboard.xpLabel")}
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-100 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 text-sm font-medium">
            <Trophy className="h-4 w-4" weight="fill" />
            {t("dashboard.streakLabel")}: {user?.streak_days || 0}d
          </div>
        </div>
      </motion.div>

      {/* Stats */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
      >
        {[
          { icon: BookOpen, label: t("dashboard.examsTaken"), value: totalAttempts, color: "bg-sky-100 dark:bg-sky-900/20 text-sky-600 dark:text-sky-400" },
          { icon: CheckCircle, label: t("dashboard.passed"), value: passedAttempts, color: "bg-emerald-100 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400" },
          { icon: TrendUp, label: t("dashboard.avgScore"), value: `${avgScore}%`, color: "bg-violet-100 dark:bg-violet-900/20 text-violet-600 dark:text-violet-400" },
          { icon: Target, label: t("dashboard.readiness"), value: totalAttempts > 0 ? `${Math.min(100, avgScore + 10)}%` : t("dashboard.notAvailable"), color: "bg-amber-100 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400" },
        ].map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div key={stat.label} variants={itemVariants}>
              <div className="bento-card">
                <div className="flex items-center gap-3">
                  <div className={`p-2.5 rounded-lg ${stat.color}`}>
                    <Icon className="h-5 w-5" weight="fill" />
                  </div>
                  <div>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400">{stat.label}</p>
                    <p className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-white">
                      {typeof stat.value === "number" ? stat.value : stat.value}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Main content — asymmetric grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left column — 2/3 width */}
        <div className="lg:col-span-2 space-y-6">
          {/* Tracks progress */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 100, damping: 20 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Network className="h-5 w-5 text-emerald-600" weight="fill" />
                  {t("dashboard.certTracks")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {tracks.length === 0 ? (
                    <div className="text-center py-10 text-zinc-400 dark:text-zinc-500">
                      <Network className="h-12 w-12 mx-auto mb-3 opacity-40" weight="light" />
                      <p className="text-sm">{t("dashboard.noTracks")}</p>
                    </div>
                  ) : (
                    tracks.map((track, i) => (
                      <Link
                        key={track.slug}
                        href={`/exams?track=${track.slug}`}
                        className="flex items-center justify-between p-4 rounded-xl border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-all duration-200 group"
                      >
                        <div className="flex items-center gap-3">
                          <Badge variant={track.vendor === "juniper" ? "juniper" : "cisco"} className="shrink-0">
                            {track.vendor === "juniper" ? "Juniper" : "Cisco"}
                          </Badge>
                          <div>
                            <p className="font-medium text-sm text-zinc-900 dark:text-zinc-100">{track.name}</p>
                            <p className="text-xs text-zinc-500 dark:text-zinc-400">{track.description}</p>
                          </div>
                        </div>
                        <CaretRight className="h-4 w-4 text-zinc-400 group-hover:text-emerald-500 transition-colors" weight="regular" />
                      </Link>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent attempts */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, type: "spring", stiffness: 100, damping: 20 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-emerald-600" weight="fill" />
                  {t("dashboard.recentAttempts")}
                </CardTitle>
              </CardHeader>
              <CardContent>
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
                  <div className="space-y-1">
                    {history.slice(0, 5).map((attempt) => (
                      <Link
                        key={attempt.id}
                        href={`/review/${attempt.id}`}
                        className="flex items-center justify-between p-3 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors group"
                      >
                        <div className="flex items-center gap-3">
                          {attempt.score && attempt.score >= 70 ? (
                            <CheckCircle className="h-5 w-5 text-emerald-500" weight="fill" />
                          ) : attempt.score ? (
                            <XCircle className="h-5 w-5 text-red-500" weight="fill" />
                          ) : (
                            <Warning className="h-5 w-5 text-amber-500" weight="fill" />
                          )}
                          <div>
                            <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">
                              {attempt.exam_id?.substring(0, 8)}...
                            </p>
                            <p className="text-xs text-zinc-500 dark:text-zinc-400">
                              {new Date(attempt.started_at).toLocaleDateString(locale === "ru" ? "ru-RU" : "en-US", { month: "short", day: "numeric", year: "numeric" })} &middot;{" "}
                              {attempt.questions_answered}/{attempt.questions_total} {t("dashboard.answered")}
                            </p>
                          </div>
                        </div>
                        {attempt.score !== null && (
                          <span className={`text-sm font-semibold font-mono ${
                            attempt.score >= 70 ? "text-emerald-500" : "text-red-500"
                          }`}>
                            {Math.round(attempt.score)}%
                          </span>
                        )}
                      </Link>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Right column — 1/3 width */}
        <div className="space-y-6">
          {/* Quick actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25, type: "spring", stiffness: 100, damping: 20 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-sm">
                  <Lightning className="h-4 w-4 text-amber-500" weight="fill" />
                  {t("dashboard.quickActions")}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
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
              </CardContent>
            </Card>
          </motion.div>

          {/* Study Progress */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35, type: "spring", stiffness: 100, damping: 20 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-sm">
                  <Book className="h-4 w-4 text-emerald-600" weight="fill" />
                  {t("dashboard.studyProgress")}
                </CardTitle>
                <CardDescription className="text-xs">
                  {t("dashboard.studyProgressDesc")}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {tracks.length === 0 ? (
                  <div className="text-center py-6 text-zinc-400 dark:text-zinc-500">
                    <Book className="h-10 w-10 mx-auto mb-2 opacity-40" weight="light" />
                    <p className="text-xs">{t("dashboard.noGuides")}</p>
                  </div>
                ) : (
                  tracks.map((track) => {
                    const stats = trackStudyStats[track.slug];
                    if (!stats) return null;
                    const pct = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;
                    return (
                      <div key={track.slug} className="space-y-1">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-xs text-zinc-700 dark:text-zinc-300 truncate">
                            {track.name}
                          </span>
                          <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 shrink-0">
                            {stats.completed}/{stats.total}
                          </span>
                        </div>
                        <div className="w-full h-1.5 bg-zinc-200 dark:bg-zinc-800 rounded-full overflow-hidden">
                          <motion.div
                            className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-400"
                            initial={{ width: 0 }}
                            animate={{ width: `${pct}%` }}
                            transition={{ duration: 0.8, ease: "easeOut" }}
                          />
                        </div>
                      </div>
                    );
                  })
                )}
                <Link
                  href="/study"
                  className="block mt-4 text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 transition-colors"
                >
                  {t("dashboard.viewAllGuides")} →
                </Link>
              </CardContent>
            </Card>
          </motion.div>

          {/* Achievements */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, type: "spring", stiffness: 100, damping: 20 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-sm">
                  <Trophy className="h-4 w-4 text-emerald-600" weight="fill" />
                  {t("dashboard.achievements")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {[
                    { name: t("dashboard.firstExam"), icon: BookOpen, done: totalAttempts > 0 },
                    { name: t("dashboard.perfectScore"), icon: Trophy, done: history.some((a) => a.score === 100) },
                    { name: t("dashboard.studyStreak"), icon: Lightning, done: (user?.streak_days || 0) >= 7 },
                    { name: t("dashboard.jackOfAll"), icon: Network, done: new Set(history.map((a) => a.exam_id)).size >= 3 },
                  ].map((ach) => {
                    const Icon = ach.icon;
                    return (
                      <div
                        key={ach.name}
                        className={`flex items-center gap-3 p-2 rounded-lg transition-opacity ${
                          ach.done ? "opacity-100" : "opacity-30"
                        }`}
                      >
                        <Icon className={`h-4 w-4 ${ach.done ? "text-emerald-500" : "text-zinc-400"}`} weight={ach.done ? "fill" : "regular"} />
                        <span className="text-sm text-zinc-700 dark:text-zinc-300">{ach.name}</span>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

