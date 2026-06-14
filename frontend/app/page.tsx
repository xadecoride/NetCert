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
  Users,
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

const stats = [
  { value: 9150, suffix: "+", labelKey: "statsQuestions", icon: BookOpen },
  { value: 10, suffix: "+", labelKey: "statsLabs", icon: ComputerTower },
  { value: 5, suffix: "", labelKey: "statsTracks", icon: Network },
  { value: 1200, suffix: "+", labelKey: "statsUsers", icon: Users },
];

const certifications = [
  "JNCIA-Junos",
  "JNCIP-ENT",
  "JNCIE-ENT",
  "CCNA",
  "CCNP",
  "CCIE",
  "JNCIA-Cloud",
  "JNCIP-SP",
  "JNCIE-SP",
  "CCNP Enterprise",
  "CCIE Enterprise",
  "JNCIP-SEC",
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
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-zinc-50 dark:from-zinc-950 dark:via-zinc-950 dark:to-zinc-900" />
        <div className="absolute top-0 right-0 w-full lg:w-1/2 h-full bg-gradient-to-l from-emerald-100/40 dark:from-emerald-900/10" />

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
              <h1 className="text-5xl sm:text-6xl lg:text-7xl xl:text-8xl font-bold tracking-tighter leading-[0.9] text-zinc-900 dark:text-white">
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
                <div className="absolute inset-0 rounded-[2rem] bg-gradient-to-br from-emerald-100/50 to-zinc-100/50 dark:from-emerald-900/10 dark:to-zinc-900/30 border border-zinc-200 dark:border-zinc-800" />
                <NetworkTopology className="relative p-6 lg:p-8" />
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
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-white">
              {t("landing.featuresTitle")}
            </h2>
            <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400 max-w-xl">
              {t("landing.featuresSubtitle")}
            </p>
          </SectionReveal>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              const colorMap: Record<string, { bg: string; text: string; dot: string }> = {
                emerald: { bg: "bg-emerald-100 dark:bg-emerald-900/30", text: "text-emerald-600 dark:text-emerald-400", dot: "bg-emerald-500" },
                sky: { bg: "bg-sky-100 dark:bg-sky-900/30", text: "text-sky-600 dark:text-sky-400", dot: "bg-sky-500" },
                amber: { bg: "bg-amber-100 dark:bg-amber-900/30", text: "text-amber-600 dark:text-amber-400", dot: "bg-amber-500" },
              };
              const c = colorMap[feature.color];
              return (
                <motion.div
                  key={feature.titleKey}
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-50px" }}
                  transition={{ ...springTransition, delay: index * 0.1 }}
                >
                  <BentoCard className="h-full flex flex-col">
                    <div className={`p-4 rounded-2xl ${c.bg} w-fit mb-5`}>
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
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-white">
              {t("landing.statsTitle")}
            </h2>
            <p className="mt-3 text-lg text-zinc-500 dark:text-zinc-400">
              {t("landing.statsSubtitle")}
            </p>
          </SectionReveal>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.labelKey}
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ ...springTransition, delay: index * 0.1 }}
                  className="bento-card"
                >
                  <Icon className="h-6 w-6 text-emerald-500 mb-4" weight="duotone" />
                  <div className="text-4xl lg:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-white">
                    <AnimatedCounter value={stat.value} suffix={stat.suffix} />
                  </div>
                  <div className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                    {t(`landing.${stat.labelKey}` as any)}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ─── Tracks: Zig-Zag 2-col ─── */}
      <section className="py-24 lg:py-32 bg-zinc-50 dark:bg-zinc-950">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <SectionReveal className="mb-16">
            <Badge variant="secondary" className="mb-4">{t("landing.tracks")}</Badge>
            <h2 className="text-4xl sm:text-5xl font-bold tracking-tighter text-zinc-900 dark:text-white">
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
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            {tracks.map((track, index) => {
              const Icon = track.icon;
              const isOffset = index % 2 === 1;
              return (
                <motion.div
                  key={track.slug}
                  variants={itemVariants}
                  className={isOffset ? "lg:mt-12" : ""}
                >
                  <Link href={`/exams?track=${track.slug}`}>
                    <BentoCard className="group cursor-pointer h-full flex flex-col hover:-translate-y-1 transition-transform duration-300">
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
                        {t("landing.viewExams")} <CaretRight className="ml-1 h-4 w-4" />
                      </div>
                    </BentoCard>
                  </Link>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section className="py-24 lg:py-32 border-t border-zinc-200 dark:border-zinc-800">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-emerald-600 to-emerald-800 p-12 lg:p-16 text-center text-white"
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
        </div>
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
