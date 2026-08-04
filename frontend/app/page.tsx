"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { BentoCard } from "@/components/ui/card";
import { SectionReveal } from "@/components/motion/SectionReveal";
import { KineticMarquee } from "@/components/motion/KineticMarquee";
import { AnimatedCounter } from "@/components/motion/AnimatedCounter";
import { NetworkTopology } from "@/components/landing/network-topology";
import { HeroTopology } from "@/components/landing/HeroTopology";
import { useTranslation } from "@/lib/i18n/context";
import { springTransition } from "@/lib/motion";
import {
  Network,
  ShieldCheck,
  ComputerTower,
  Cloud,
  ChartBar,
  BookOpen,
  Trophy,
  ArrowRight,
  CaretRight,
  CheckCircle,
  Sparkle,
} from "@phosphor-icons/react";

// Available tracks correspond to the four exams that actually have content
// in the bank (per AGENTS.md / CLAUDE.md §10): CCNA 200-301, JNCIA-Junos,
// JNCIP-ENT, JNCIP-SP. The other Juniper tracks are roadmap placeholders.
const tracks = [
  {
    name: "Enterprise Routing & Switching",
    vendor: "juniper" as const,
    slug: "junos-ent",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "Core enterprise networking with Junos OS",
    gradient: "from-emerald-500 to-emerald-600",
    icon: Network,
    available: true,
  },
  {
    name: "Service Provider",
    vendor: "juniper" as const,
    slug: "junos-sp",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "MPLS, BGP, and service provider technologies",
    gradient: "from-sky-500 to-cyan-600",
    icon: Network,
    available: true,
  },
  {
    name: "Security",
    vendor: "juniper" as const,
    slug: "junos-sec",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "SRX firewalls, IPsec VPNs, and security policies",
    gradient: "from-red-500 to-rose-600",
    icon: ShieldCheck,
    available: false,
  },
  {
    name: "Data Center",
    vendor: "juniper" as const,
    slug: "junos-dc",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "EVPN-VXLAN, QFX, and data center fabrics",
    gradient: "from-violet-500 to-purple-600",
    icon: ComputerTower,
    available: false,
  },
  {
    name: "DevOps & Automation",
    vendor: "juniper" as const,
    slug: "junos-aut",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "PyEZ, Ansible, NETCONF, and automation",
    gradient: "from-amber-500 to-orange-600",
    icon: Cloud,
    available: false,
  },
  {
    name: "Cisco CCNA",
    vendor: "cisco" as const,
    slug: "cisco-ccna",
    levels: ["CCNA", "CCNP", "CCIE"],
    description: "Cisco certified network associate and beyond",
    gradient: "from-sky-500 to-blue-600",
    icon: Trophy,
    available: true,
  },
];

const features = [
  {
    icon: BookOpen,
    titleKey: "adaptiveTesting",
    descKey: "adaptiveTestingDesc",
    value: 9150,
    suffix: "+",
    statKey: "statsQuestions",
    color: "emerald",
  },
  {
    icon: ChartBar,
    titleKey: "detailedAnalytics",
    descKey: "detailedAnalyticsDesc",
    value: 15,
    suffix: "+",
    statKey: "statsMetrics",
    color: "sky",
  },
  {
    icon: Trophy,
    titleKey: "labs",
    descKey: "labsDesc",
    value: 10,
    suffix: "+",
    statKey: "statsLabs",
    color: "amber",
  },
];

// Numeric stats use AnimatedCounter; the free/self-hosted cell is a static badge.
const stats = [
  { value: 9150, suffix: "+", labelKey: "statsQuestions", icon: BookOpen },
  { value: 10, suffix: "+", labelKey: "statsLabs", icon: ComputerTower },
  { value: 6, suffix: "", labelKey: "statsTracks", icon: Network },
  { static: true, labelKey: "statsSelfHosted", icon: CheckCircle },
];

const certifications = [
  "JNCIA-Junos",
  "JNCIS-ENT",
  "JNCIP-ENT",
  "JNCIE-ENT",
  "CCNA 2.0",
  "CCNP",
  "CCIE",
  "JNCIA-Cloud",
  "JNCIS-SP",
  "JNCIP-SP",
  "JNCIE-SP",
  "CCNP Enterprise",
  "CCIE Enterprise",
  "JNCIS-SEC",
  "JNCIP-SEC",
  "JNCIS-DC",
  "JNCIS-AUT",
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: springTransition,
  },
};

export default function LandingPage() {
  const { t } = useTranslation();

  return (
    <div className="min-h-[100dvh]">
      {/* ─── Hero ─── */}
      <section className="relative overflow-hidden border-b border-zinc-200 dark:border-zinc-800">
        {/* Base gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-zinc-50 dark:from-zinc-950 dark:via-zinc-950 dark:to-zinc-900" />
        
        {/* Mesh gradients — 3 large blobs for depth */}
        <div className="absolute -top-40 -right-40 w-[500px] h-[500px] rounded-full bg-emerald-400/10 blur-3xl dark:bg-emerald-500/10" />
        <div className="absolute -bottom-60 -left-60 w-[400px] h-[400px] rounded-full bg-cyan-400/10 blur-3xl dark:bg-cyan-500/10" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-emerald-300/5 blur-3xl dark:bg-emerald-600/5" />
        
        {/* Subtle vignette */}
        <div className="absolute inset-0 bg-gradient-to-t from-zinc-950/10 to-transparent dark:from-zinc-900/20 pointer-events-none" />
        
        {/* Noise overlay */}
                <div 
                  className="absolute inset-0 opacity-[0.015] pointer-events-none" 
                  style={{ 
                    backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")' 
                  }} 
                />
        
        <div className="relative max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row lg:items-center min-h-[calc(100dvh-4rem)] py-20 lg:py-0 gap-12 lg:gap-8">
            {/* Left: Content */}
            <motion.div
              initial={{ opacity: 0, x: -40 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className="w-full lg:w-[55%] lg:pr-12 pt-12 lg:pt-0"
            >
              <Badge variant="default" pulse className="mb-6">
                <Network className="h-3 w-3" weight="fill" />
                {t("landing.badge")}
              </Badge>
              <h1 className="font-[var(--font-family-display)] text-display-xl font-bold tracking-tighter leading-[0.95] text-zinc-900 dark:text-zinc-100">
                {t("landing.title")}
                <span className="block mt-1 text-emerald-600 dark:text-emerald-400">
                  {t("landing.titleAccent")}
                </span>
              </h1>
              <p className="mt-6 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl leading-relaxed">
                {t("landing.subtitle")}
              </p>
              <div className="flex flex-col sm:flex-row gap-3 mt-10">
                <Link href="/auth/register">
                  <Button variant="primary" size="xl" className="w-full sm:w-auto text-base group">
                    {t("landing.getStarted")}
                    <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" weight="bold" />
                  </Button>
                </Link>
                <Link href="/auth/login">
                  <Button variant="outline" size="xl" className="w-full sm:w-auto text-base">
                    {t("landing.signIn")}
                  </Button>
                </Link>
              </div>
              <div className="flex flex-wrap items-center gap-6 mt-10 text-xs text-zinc-400 dark:text-zinc-500">
                <span className="flex items-center gap-1.5">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                  </span>
                  {t("landing.freeForever")}
                </span>
                <span className="flex items-center gap-1.5">
                  <CheckCircle className="h-4 w-4 text-emerald-500" weight="fill" />
                  {t("landing.noRegistration")}
                </span>
                <span className="flex items-center gap-1.5">
                  <Sparkle className="h-4 w-4 text-cyan-500" weight="fill" />
                  AGPL-3.0
                </span>
              </div>
            </motion.div>

            {/* Right: Topology */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="w-full lg:w-[45%] flex items-center justify-center"
            >
              <div className="relative w-full max-w-lg aspect-square">
                <div className="absolute inset-0 rounded-[2rem] bg-gradient-to-br from-emerald-100/50 to-zinc-100/50 dark:from-emerald-900/10 dark:to-zinc-900/30 border border-zinc-200 dark:border-zinc-800 shadow-[var(--shadow-glow-emerald-soft)]" />
                <HeroTopology className="relative p-6 lg:p-8" />
                {/* floating stat chips overlay */}
                <motion.div
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8, duration: 0.6 }}
                  className="absolute -bottom-4 -left-4 hidden sm:flex items-center gap-2 rounded-2xl border border-zinc-200 bg-white/80 px-3 py-2 text-xs font-medium text-zinc-700 shadow-[var(--shadow-sm)] backdrop-blur-xl dark:border-zinc-800 dark:bg-zinc-900/80 dark:text-zinc-200"
                >
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                  </span>
                  Live topology
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ─── Certification Marquee ─── */}
      <KineticMarquee
        items={certifications}
        speed={35}
        className="bg-zinc-50 dark:bg-zinc-950"
      />

      {/* ─── Features: Bento Grid ─── */}
      <section className="py-24 lg:py-32 bg-zinc-50 dark:bg-zinc-950 border-b border-zinc-200 dark:border-zinc-800">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <SectionReveal className="mb-16">
            <Badge variant="secondary" className="mb-4">{t("landing.features")}</Badge>
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
              {t("landing.featuresTitle")}
            </h2>
            <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl">
              {t("landing.featuresSubtitle")}
            </p>
          </SectionReveal>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              const colorMap: Record<string, { bg: string; text: string; dot: string; glow: string }> = {
                emerald: { bg: "bg-emerald-100 dark:bg-emerald-900/30", text: "text-emerald-600 dark:text-emerald-400", dot: "bg-emerald-500", glow: "shadow-[0_0_40px_-12px_rgba(16,185,129,0.45)]" },
                sky: { bg: "bg-sky-100 dark:bg-sky-900/30", text: "text-sky-600 dark:text-sky-400", dot: "bg-sky-500", glow: "shadow-[0_0_40px_-12px_rgba(14,165,233,0.45)]" },
                amber: { bg: "bg-amber-100 dark:bg-amber-900/30", text: "text-amber-600 dark:text-amber-400", dot: "bg-amber-500", glow: "shadow-[0_0_40px_-12px_rgba(245,158,11,0.45)]" },
              };
              const c = colorMap[feature.color];
              return (
                <motion.div
                  key={feature.titleKey}
                  className="group relative"
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-50px" }}
                  transition={{ ...springTransition, delay: index * 0.1 }}
                >
                  {/* Accent border that animates on hover */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                  
                  <BentoCard className="relative h-full flex flex-col z-10 group-hover:-translate-y-1 transition-transform duration-300">
                    <div className={`p-4 rounded-2xl ${c.bg} ${c.glow} w-fit mb-5 transition-transform duration-300 group-hover:scale-110`}>
                      <Icon className={`h-8 w-8 ${c.text}`} weight="duotone" />
                    </div>
                    <h3 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                      {t(`landing.${feature.titleKey}` as any)}
                    </h3>
                    <p className="mt-2 text-zinc-500 dark:text-zinc-400 leading-relaxed flex-1">
                      {t(`landing.${feature.descKey}` as any)}
                    </p>
                    <div className="mt-6 flex items-center gap-3">
                      <motion.div
                        className={`h-2 w-2 rounded-full ${c.dot}`}
                        animate={{ scale: [1, 1.4, 1], opacity: [0.6, 1, 0.6] }}
                        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                      />
                      <span className={`text-sm font-medium ${c.text}`}>
                        <AnimatedCounter value={feature.value} suffix={feature.suffix} /> {t(`landing.${feature.statKey}` as any).toLowerCase()}
                      </span>
                    </div>
                  </BentoCard>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ─── Stats ─── */}
      <section className="py-24 lg:py-32 border-b border-zinc-200 dark:border-zinc-800">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <SectionReveal className="mb-16 max-w-xl">
            <Badge variant="secondary" className="mb-4">{t("landing.statsTitle")}</Badge>
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
              {t("landing.statsTitle")}
            </h2>
            <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400">
              {t("landing.statsSubtitle")}
            </p>
          </SectionReveal>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            {/* Hero stat — Questions (spans 2 cols) */}
            <motion.div
              key="statsQuestions"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ ...springTransition, delay: 0 }}
              className="lg:col-span-2 bento-card relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/10 to-cyan-500/10" />
              <div className="relative p-6 lg:p-8">
                <BookOpen className="h-6 w-6 text-emerald-500 mb-4" weight="duotone" />
                <div className="text-6xl lg:text-7xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
                  <AnimatedCounter value={9150} suffix="+" />
                </div>
                <div className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                  {t("landing.statsQuestions")}
                </div>
              </div>
            </motion.div>
            
            {/* Remaining stats */}
            {stats.slice(1).map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.labelKey}
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ ...springTransition, delay: (index + 1) * 0.1 }}
                  className="bento-card"
                >
                  <Icon className="h-6 w-6 text-emerald-500 mb-4" weight="duotone" />
                  <div className="text-4xl lg:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
                    {(stat as any).static ? (
                      <span className="inline-flex items-center gap-2 text-3xl lg:text-4xl">
                        Free
                        <span className="text-base font-medium text-zinc-400 dark:text-zinc-500">/ {t(`landing.${stat.labelKey}` as any)}</span>
                      </span>
                    ) : (
                      <AnimatedCounter value={(stat as any).value} suffix={(stat as any).suffix} />
                    )}
                  </div>
                  {!(stat as any).static && (
                    <div className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                      {t(`landing.${stat.labelKey}` as any)}
                    </div>
                  )}
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ─── Tracks: Masonry Grid ─── */}
      <section className="py-24 lg:py-32 bg-zinc-50 dark:bg-zinc-950">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <SectionReveal className="mb-16">
            <Badge variant="secondary" className="mb-4">{t("landing.tracks")}</Badge>
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-zinc-100">
              {t("landing.tracksTitle")}
            </h2>
            <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl">
              {t("landing.tracksSubtitle")}
            </p>
          </SectionReveal>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {tracks.map((track, index) => {
              const Icon = track.icon;
              return (
                <motion.div
                  key={track.slug}
                  variants={itemVariants}
                  className={track.available ? "lg:row-span-2" : ""}
                >
                  {track.available ? (
                    <Link href={`/exams?track=${track.slug}`}>
                      <BentoCard className="group cursor-pointer h-full flex flex-col hover:-translate-y-1 transition-transform duration-300">
                        <TrackCardInner track={track} Icon={Icon} t={t} />
                      </BentoCard>
                    </Link>
                  ) : (
                    <BentoCard className="group h-full flex flex-col opacity-60">
                      <TrackCardInner track={track} Icon={Icon} t={t} />
                    </BentoCard>
                  )}
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section className="py-24 lg:py-32 border-t border-zinc-200 dark:border-zinc-800 relative">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-20 -right-20 w-[400px] h-[400px] rounded-full bg-emerald-500/15 blur-3xl" />
          <div className="absolute -bottom-20 -left-20 w-[300px] h-[300px] rounded-full bg-cyan-500/15 blur-3xl" />
        </div>
        
        <motion.div
          className="relative z-10 max-w-3xl mx-auto px-6 text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
        >
          <Badge variant="secondary" className="mb-5 mx-auto bg-white/10 text-white border border-white/20">
            <Sparkle className="h-3 w-3" weight="fill" /> AGPL-3.0 · Open Source
          </Badge>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tighter text-white">
            {t("landing.ctaTitle")}
          </h2>
          <p className="mt-5 text-lg text-white/70 max-w-xl mx-auto">
            {t("landing.ctaSubtitle")}
          </p>
          <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/auth/register">
              <Button variant="secondary" size="xl" className="w-full sm:w-auto bg-white text-emerald-800 hover:bg-zinc-100 shadow-[0_0_40px_rgba(255,255,255,0.15)]">
                {t("landing.getStarted")}
              </Button>
            </Link>
            <Link href="/exams">
              <Button variant="outline" size="xl" className="w-full sm:w-auto border-white/30 text-white hover:bg-white/10">
                {t("landing.browseExams")}
              </Button>
            </Link>
          </div>
        </motion.div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="border-t border-zinc-200 dark:border-zinc-800 py-8">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-zinc-500 dark:text-zinc-400">
          <p>{t("landing.footer")}</p>
        </div>
      </footer>
    </div>
  );
}

// ─── helpers ────────────────────────────────────────────────
type Track = (typeof tracks)[number];

function TrackCardInner({
  track,
  Icon,
  t,
}: {
  track: Track;
  Icon: Track["icon"];
  // The real i18n `t` is a union-of-keys function (strongly typed); we pass it
  // through `as any` at the call site just like the rest of this page already
  // does for computed keys (`t(`landing.${...}` as any)`). Plumbing the full
  // union here would duplicate the i18n type, which is not worth it for one helper.
  t: (key: any) => string;
}) {
  return (
    <>
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-xl bg-gradient-to-br ${track.gradient} text-white shadow-lg`}>
          <Icon className="h-5 w-5" weight="fill" />
        </div>
        <div className="flex items-center gap-1.5">
          <Badge variant={track.vendor === "juniper" ? "juniper" : "cisco"}>
            {track.vendor === "juniper" ? "Juniper" : "Cisco"}
          </Badge>
          {track.available ? (
            <Badge variant="success" className="gap-1">
              <span className="relative flex h-1.5 w-1.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75" />
                <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500" />
              </span>
              {t("landing.trackAvailable")}
            </Badge>
          ) : (
            <Badge variant="outline" className="text-zinc-400 dark:text-zinc-500">
              {t("landing.trackRoadmap")}
            </Badge>
          )}
        </div>
      </div>
      <h3
        className={`font-semibold text-lg text-zinc-900 dark:text-zinc-100 ${
          track.available ? "group-hover:text-emerald-600 transition-colors" : ""
        }`}
      >
        {track.name}
      </h3>
      <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400 flex-1">
        {track.description}
      </p>
      <div className="flex flex-wrap gap-1.5 mt-4">
        {track.levels.map((level) => (
          <Badge key={level} variant="outline" className="text-xs">
            {level}
          </Badge>
        ))}
      </div>
      {track.available && (
        <div className="flex items-center mt-4 text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
          {t("landing.viewExams")} <CaretRight className="ml-1 h-4 w-4" />
        </div>
      )}
    </>
  );
}
