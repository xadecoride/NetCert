"use client";

import { useState, useEffect, Suspense } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { tracksApi, labsApi } from "@/lib/api";
import { Spinner } from "@/components/ui/spinner";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  ComputerTower,
  Clock,
  Network,
  ShieldCheck,
  Cloud,
  Trophy,
  CaretRight,
  Funnel,
  Flask,
  BookOpen,
  Play,
} from "@phosphor-icons/react";

const trackIcons: Record<string, any> = {
  "junos-ent": Network,
  "junos-sp": Network,
  "junos-sec": ShieldCheck,
  "junos-dc": ComputerTower,
  "junos-aut": Cloud,
  "cisco": Trophy,
};

const technologyLabels: Record<string, string> = {
  "junos-cli": "JunOS CLI",
  "ospf": "OSPF",
  "bgp": "BGP",
  "isis": "IS-IS",
  "mpls": "MPLS",
  "evpn": "EVPN",
  "vxlan": "VXLAN",
  "ipsec": "IPsec",
  "srx-policies": "SRX Policies",
  "pyez": "PyEZ",
  "ansible": "Ansible",
};

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

export default function LabsPageWrapper() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    }>
      <LabsPage />
    </Suspense>
  );
}

function LabsPage() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { t } = useTranslation();
  const router = useRouter();

  const [tracks, setTracks] = useState<any[]>([]);
  const [labsByTrack, setLabsByTrack] = useState<Record<string, any[]>>({});
  const [loading, setLoading] = useState(true);
  const [activeTrack, setActiveTrack] = useState<string | null>(null);
  const [activeLevel, setActiveLevel] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
      return;
    }
    loadData();
  }, [isAuthenticated, authLoading, router]);

  const loadData = async () => {
    try {
      const t = await tracksApi.list();
      setTracks(t || []);

      const labsMap: Record<string, any[]> = {};
      for (const track of t || []) {
        try {
          const labs = await labsApi.list(track.id);
          labsMap[track.slug] = labs || [];
        } catch {
          labsMap[track.slug] = [];
        }
      }
      setLabsByTrack(labsMap);
    } catch (err) {
      console.error("Failed to load labs:", err);
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

  // Get all labs across all tracks for filtering
  const allLabs = Object.values(labsByTrack).flat();
  const levels = [...new Set(allLabs.map((l: any) => l.level).filter(Boolean))];

  const filteredLabsByTrack = (() => {
    if (!activeTrack && !activeLevel) return labsByTrack;
    const result: Record<string, any[]> = {};
    for (const [slug, labs] of Object.entries(labsByTrack)) {
      let filtered = labs;
      if (activeTrack && slug !== activeTrack) {
        if (Object.keys(labsByTrack).filter(s => s === activeTrack).length > 0) {
          if (slug !== activeTrack) continue;
        }
      }
      if (activeLevel) {
        filtered = filtered.filter((l: any) => l.level === activeLevel);
      }
      if (filtered.length > 0 || slug === activeTrack) {
        result[slug] = filtered;
      }
    }
    if (activeTrack) {
      const keys = Object.keys(result);
      for (const key of keys) {
        if (key !== activeTrack) delete result[key];
      }
    }
    return result;
  })();

  const getLevelBadgeVariant = (level: string) => {
    switch (level) {
      case "JNCIA": return "success";
      case "JNCIP": return "warning";
      case "JNCIP": return "warning";
      case "JNCIE": return "danger";
      default: return "outline";
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-10">
        <div>
          <Badge variant="secondary" className="mb-3">{t("labs.badge") || "Labs"}</Badge>
          <h1 className="text-4xl font-bold tracking-tighter text-zinc-900 dark:text-white">
            {t("labs.title") || "Lab Exercises"}
          </h1>
          <p className="mt-1 text-zinc-500 dark:text-zinc-400">
            {t("labs.subtitle") || "Hands-on practice with virtual Juniper devices. Deploy real network topologies and verify configurations."}
          </p>
        </div>
      </div>

      {/* Filters */}
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
        <div className="w-px h-5 bg-zinc-300 dark:bg-zinc-600 mx-1" />
        {levels.map((level) => (
          <button
            key={level}
            onClick={() => setActiveLevel(activeLevel === level ? null : level)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
              activeLevel === level
                ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
                : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
            }`}
          >
            {level}
          </button>
        ))}
        {(activeTrack || activeLevel) && (
          <button
            onClick={() => { setActiveTrack(null); setActiveLevel(null); }}
            className="px-3 py-1.5 rounded-lg text-xs font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            Clear
          </button>
        )}
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
          {Object.entries(filteredLabsByTrack).map(([slug, labs]) => {
            const track = tracks.find((t) => t.slug === slug);
            if (!track || labs.length === 0) return null;
            const Icon = trackIcons[slug] || ComputerTower;
            const isJuniper = track.vendor === "juniper";

            return (
              <motion.div key={slug} variants={itemVariants}>
                {/* Track header */}
                <div className="flex items-center gap-4 mb-5">
                  <div className={`p-2.5 rounded-xl ${isJuniper ? "bg-emerald-100 dark:bg-emerald-900/20" : "bg-sky-100 dark:bg-sky-900/20"}`}>
                    <Icon className={`h-5 w-5 ${isJuniper ? "text-emerald-600 dark:text-emerald-400" : "text-sky-600 dark:text-sky-400"}`} weight="fill" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h2 className="text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">{track.name}</h2>
                      <Badge variant={track.vendor === "juniper" ? "juniper" : "cisco"} className="shrink-0">
                        {track.vendor === "juniper" ? "Juniper" : "Cisco"}
                      </Badge>
                    </div>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">
                      {labs.length} {(t("labs.available") || "available")}
                    </p>
                  </div>
                </div>

                {/* Labs grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {labs.map((lab: any) => (
                    <Link key={lab.id} href={`/lab/${lab.id}`}>
                      <motion.div
                        whileHover={{ y: -2 }}
                        transition={{ type: "spring", stiffness: 200, damping: 20 }}
                        className="bento-card group cursor-pointer h-full flex flex-col"
                      >
                        {/* Header badges */}
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex gap-1.5 flex-wrap">
                            <Badge
                              variant={getLevelBadgeVariant(lab.level)}
                              className="text-xs"
                            >
                              {lab.level}
                            </Badge>
                            <Badge variant="outline" className="text-xs font-mono">
                              {technologyLabels[lab.technology] || lab.technology}
                            </Badge>
                          </div>
                          {lab.is_troubleshooting && (
                            <Badge variant="danger" className="text-xs shrink-0">
                              Troubleshoot
                            </Badge>
                          )}
                        </div>

                        {/* Title & description */}
                        <h3 className="font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-emerald-600 transition-colors mb-1">
                          {lab.title}
                        </h3>
                        <p className="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2 flex-1">
                          {lab.description || "Interactive lab with virtual network devices."}
                        </p>

                        {/* Footer metadata */}
                        <div className="flex items-center gap-3 mt-4 pt-3 border-t border-zinc-200 dark:border-zinc-800 text-sm text-zinc-500 dark:text-zinc-400">
                          <span className="flex items-center gap-1.5">
                            <Flask className="h-3.5 w-3.5" weight="regular" />
                            {lab.max_score || "—"} pts
                          </span>
                          <span className="flex items-center gap-1.5">
                            <Clock className="h-3.5 w-3.5" weight="regular" />
                            {lab.duration_minutes}m
                          </span>
                        </div>

                        {/* Start link */}
                        <div className="flex items-center mt-3 text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
                          <Play className="h-3.5 w-3.5 mr-1.5" weight="fill" />
                          {(t("labs.start") || "Start Lab")} <CaretRight className="h-4 w-4 ml-1" weight="regular" />
                        </div>
                      </motion.div>
                    </Link>
                  ))}
                </div>
              </motion.div>
            );
          })}

          {/* Empty state */}
          {Object.keys(filteredLabsByTrack).length === 0 && (
            <div className="text-center py-16">
              <ComputerTower className="h-16 w-16 mx-auto mb-4 text-zinc-300 dark:text-zinc-600" weight="light" />
              <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                {(t("labs.noLabs") || "No labs available")}
              </h2>
              <p className="text-zinc-500 dark:text-zinc-400 mb-6">
                {(t("labs.noLabsDesc") || "Labs are being prepared for this track.")}
              </p>
              <Button variant="outline" onClick={() => { setActiveTrack(null); setActiveLevel(null); }}>
                {(t("labs.viewAll") || "View all labs")}
              </Button>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}


