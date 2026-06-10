"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useTranslation } from "@/lib/i18n/context";
import {
  Network,
  ShieldCheck,
  ComputerTower,
  Cloud,
  ChartBar,
  BookOpen,
  Trophy,
} from "@phosphor-icons/react";

const tracks = [
  {
    name: "Enterprise Routing & Switching",
    vendor: "juniper" as const,
    slug: "junos-ent",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "Core enterprise networking with Junos OS",
    gradient: "from-emerald-500 to-emerald-600",
    icon: Network,
  },
  {
    name: "Service Provider",
    vendor: "juniper" as const,
    slug: "junos-sp",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "MPLS, BGP, and service provider technologies",
    gradient: "from-sky-500 to-cyan-600",
    icon: Network,
  },
  {
    name: "Security",
    vendor: "juniper" as const,
    slug: "junos-sec",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "SRX firewalls, IPsec VPNs, and security policies",
    gradient: "from-red-500 to-rose-600",
    icon: ShieldCheck,
  },
  {
    name: "Data Center",
    vendor: "juniper" as const,
    slug: "junos-dc",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "EVPN-VXLAN, QFX, and data center fabrics",
    gradient: "from-violet-500 to-purple-600",
    icon: ComputerTower,
  },
  {
    name: "DevOps & Automation",
    vendor: "juniper" as const,
    slug: "junos-aut",
    levels: ["JNCIA", "JNCIP", "JNCIE"],
    description: "PyEZ, Ansible, NETCONF, and automation",
    gradient: "from-amber-500 to-orange-600",
    icon: Cloud,
  },
  {
    name: "Cisco CCNA",
    vendor: "cisco" as const,
    slug: "cisco-ccna",
    levels: ["CCNA", "CCNP", "CCIE"],
    description: "Cisco certified network associate and beyond",
    gradient: "from-sky-500 to-blue-600",
    icon: Trophy,
  },
];

const features = [
  {
    icon: BookOpen,
    title: "Adaptive Testing",
    description: "AI-powered exam simulations that adapt to your skill level with spaced repetition.",
    stats: "1,200+ questions",
  },
  {
    icon: ChartBar,
    title: "Detailed Analytics",
    description: "Knowledge radar charts, weakness heatmaps, and predictive readiness scoring.",
    stats: "15+ metrics",
  },
  {
    icon: Trophy,
    title: "JNCIE/CCIE Labs",
    description: "Interactive 8-hour practical labs with Containerlab, auto-grading, and scoring sheets.",
    stats: "5 lab tracks",
  },
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
    transition: { type: "spring", stiffness: 100, damping: 20 },
  },
};

export default function LandingPage() {
  const { t } = useTranslation();

  return (
    <div className="min-h-[100dvh]">
      {/* ─── Hero: Asymmetric Split ─── */}
      <section className="relative overflow-hidden border-b border-zinc-200 dark:border-zinc-800">
        {/* Background mesh gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-zinc-50 dark:from-zinc-950 dark:via-zinc-950 dark:to-zinc-900" />
        <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-emerald-100/40 dark:from-emerald-900/10" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row lg:items-center min-h-[90dvh] py-20 lg:py-0">
            {/* Left: Content */}
            <motion.div
              initial={{ opacity: 0, x: -40 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
              className="lg:w-3/5 lg:pr-16 pt-12 lg:pt-0"
            >
              <Badge variant="default" className="mb-6">
                <Network className="h-3 w-3 mr-1.5" weight="fill" />
                {t("landing.badge")}
              </Badge>
              <h1 className="text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-bold tracking-tighter leading-[0.9] text-zinc-900 dark:text-white">
                {t("landing.title")}
                <span className="block mt-1 text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-emerald-700">
                  {t("landing.titleAccent")}
                </span>
              </h1>
              <p className="mt-6 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl leading-relaxed">
                {t("landing.subtitle")}
              </p>
              <div className="flex flex-col sm:flex-row gap-3 mt-10">
                <Link href="/auth/register">
                  <Button variant="primary" size="xl" className="w-full sm:w-auto text-base">
                    {t("landing.getStarted")}
                    <ArrowRightIcon className="ml-2" />
                  </Button>
                </Link>
                <Link href="/auth/login">
                  <Button variant="outline" size="xl" className="w-full sm:w-auto text-base">
                    {t("landing.signIn")}
                  </Button>
                </Link>
              </div>
              <div className="flex items-center gap-6 mt-10 text-xs text-zinc-400 dark:text-zinc-500">
                <span className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  {t("landing.freeForever")}
                </span>
                <span className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  {t("landing.noRegistration")}
                </span>
              </div>
            </motion.div>

            {/* Right: Visual */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="lg:w-2/5 mt-12 lg:mt-0 flex items-center justify-center"
            >
              <div className="relative w-full max-w-md aspect-square">
                {/* Decorative grid */}
                <div className="absolute inset-0 grid grid-cols-3 grid-rows-3 gap-3">
                  {[...Array(9)].map((_, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.3 + i * 0.05, type: "spring", stiffness: 100, damping: 20 }}
                      className="rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white/50 dark:bg-zinc-900/50 flex items-center justify-center"
                    >
                      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-emerald-600 opacity-40" />
                    </motion.div>
                  ))}
                </div>
                {/* Center hero element */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6, type: "spring", stiffness: 100, damping: 20 }}
                  className="absolute inset-[15%] rounded-3xl bg-gradient-to-br from-emerald-500 to-emerald-700 shadow-2xl flex items-center justify-center"
                >
                  <Network className="h-20 w-20 text-white" weight="fill" />
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ─── Tracks: Bento Grid ─── */}
      <section className="py-24 lg:py-32 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="mb-16"
        >
          <Badge variant="secondary" className="mb-4">{t("landing.tracks")}</Badge>
          <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-white">
            {t("landing.tracksTitle")}
          </h2>
          <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl">
            {t("landing.tracksSubtitle")}
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-50px" }}
          className="bento-grid"
        >
          {tracks.map((track) => {
            const Icon = track.icon;
            return (
              <motion.div key={track.slug} variants={itemVariants}>
                <Link href={`/exams?track=${track.slug}`}>
                  <div className="bento-card group cursor-pointer h-full flex flex-col">
                    <div className="flex items-start justify-between mb-4">
                      <div className={`p-3 rounded-xl bg-gradient-to-br ${track.gradient} text-white shadow-lg`}>
                        <Icon className="h-5 w-5" weight="fill" />
                      </div>
                      <Badge variant={track.vendor === "juniper" ? "juniper" : "cisco"}>
                        {track.vendor === "juniper" ? "Juniper" : "Cisco"}
                      </Badge>
                    </div>
                    <h3 className="font-semibold text-lg text-zinc-900 dark:text-zinc-100 group-hover:text-emerald-600 transition-colors">
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
                    <div className="flex items-center mt-4 text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
                      {t("landing.viewExams")} <CaretRightIcon className="ml-1" />
                    </div>
                  </div>
                </Link>
              </motion.div>
            );
          })}
        </motion.div>
      </section>

      {/* ─── Features: Asymmetric Layout ─── */}
      <section className="py-24 bg-zinc-50 dark:bg-zinc-900/50 border-y border-zinc-200 dark:border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="mb-16"
          >
          <Badge variant="secondary" className="mb-4">{t("landing.features")}</Badge>
          <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-white">
            {t("landing.featuresTitle")}
          </h2>
          <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl">
            {t("landing.featuresSubtitle")}
          </p>
          </motion.div>

          {/* Asymmetric grid: 2 + 1 layout (not 3-column cards) */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.1 }}
              className="lg:col-span-2"
            >
              <div className="bento-card h-full p-8 lg:p-10">
                <div className="flex flex-col sm:flex-row sm:items-start gap-6">
                  <div className="p-4 rounded-2xl bg-emerald-100 dark:bg-emerald-900/30 flex-shrink-0">
                    <BookOpen className="h-8 w-8 text-emerald-600 dark:text-emerald-400" weight="duotone" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                      {t("landing.adaptiveTesting")}
                    </h3>
                    <p className="mt-2 text-zinc-500 dark:text-zinc-400 max-w-lg leading-relaxed">
                      {t("landing.adaptiveTestingDesc")}
                    </p>
                    <div className="mt-6 flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400">
                      <div className="w-2 h-2 rounded-full bg-emerald-500" />
                      {t("landing.questionsCount")}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.2 }}
            >
              <div className="bento-card h-full p-8 lg:p-10">
                <div className="p-4 rounded-2xl bg-sky-100 dark:bg-sky-900/30 mb-5 inline-block">
                  <ChartBar className="h-8 w-8 text-sky-600 dark:text-sky-400" weight="duotone" />
                </div>
                <h3 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">                      {t("landing.detailedAnalytics")}
                    </h3>
                <p className="mt-2 text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  {t("landing.detailedAnalyticsDesc")}
                </p>
                <div className="mt-6 flex items-center gap-2 text-sm text-sky-600 dark:text-sky-400">
                  <div className="w-2 h-2 rounded-full bg-sky-500" />
                  {t("landing.metricsCount")}
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.3 }}
              className="lg:col-span-3"
            >
              <div className="bento-card h-full p-8 lg:p-10 flex flex-col lg:flex-row lg:items-center gap-8">
                <div className="p-4 rounded-2xl bg-amber-100 dark:bg-amber-900/30 flex-shrink-0 inline-block">
                  <Trophy className="h-8 w-8 text-amber-600 dark:text-amber-400" weight="duotone" />
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
                    {t("landing.labs")}
                  </h3>
                  <p className="mt-2 text-zinc-500 dark:text-zinc-400 max-w-2xl leading-relaxed">
                    {t("landing.labsDesc")}
                  </p>
                </div>
                <div className="flex items-center gap-2 text-sm text-amber-600 dark:text-amber-400 flex-shrink-0">
                  <div className="w-2 h-2 rounded-full bg-amber-500" />
                  {t("landing.labsCount")}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-600 to-emerald-800 p-12 lg:p-16 text-center text-white"
        >
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{ backgroundImage: 'radial-gradient(circle at 25% 50%, white 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
          </div>
          <div className="relative">
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter">{t("landing.ctaTitle")}</h2>
            <p className="mt-4 text-lg text-white/70 max-w-lg mx-auto">
              {t("landing.ctaSubtitle")}
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-3 mt-10">
              <Link href="/auth/register">
                <Button variant="secondary" size="xl" className="text-base bg-white text-emerald-800 hover:bg-zinc-100 shadow-xl">
                  {t("landing.getStarted")}
                </Button>
              </Link>
              <Link href="/exams">
                <Button variant="outline" size="xl" className="text-base border-white/20 text-white hover:bg-white/10">
                  {t("landing.browseExams")}
                </Button>
              </Link>
            </div>
          </div>
        </motion.div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="border-t border-zinc-200 dark:border-zinc-800 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-zinc-500 dark:text-zinc-400">
          <p>{t("landing.footer")}</p>
        </div>
      </footer>
    </div>
  );
}

/* Inline icon components to keep Phosphor imports clean */
function ArrowRightIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
    </svg>
  );
}

function CaretRightIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m9 18 6-6-6-6" />
    </svg>
  );
}
