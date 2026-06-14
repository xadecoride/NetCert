"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { NetworkTopology } from "@/components/landing/network-topology";
import {
  UserPlus,
  Eye,
  EyeSlash,
  ArrowRight,
  Check,
} from "@phosphor-icons/react";

export default function RegisterPage() {
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const { register } = useAuth();
  const { t } = useTranslation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError(t("auth.passwordTooShort"));
      return;
    }

    if (!acceptTerms) {
      setError(t("auth.termsError"));
      return;
    }

    setLoading(true);
    try {
      await register(email, password, displayName);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[100dvh] flex flex-col lg:flex-row">
      {/* Left: Branding & kinetic topology */}
      <div className="relative hidden lg:flex lg:w-1/2 flex-col justify-between overflow-hidden bg-zinc-50 dark:bg-zinc-950 border-r border-zinc-200 dark:border-zinc-800">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-zinc-50 dark:from-zinc-950 dark:via-zinc-950 dark:to-zinc-900" />
        <div className="absolute inset-0 opacity-[0.03] bg-[url('data:image/svg+xml,%3Csvg%20viewBox%3D%220%200%20256%20256%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cfilter%20id%3D%22noise%22%3E%3CfeTurbulence%20type%3D%22fractalNoise%22%20baseFrequency%3D%220.85%22%20numOctaves%3D%224%22%20stitchTiles%3D%22stitch%22%2F%3E%3C%2Ffilter%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20filter%3D%22url%28%23noise%29%22%2F%3E%3C%2Fsvg%3E')]" />

        <div className="relative z-10 p-12">
          <Link href="/" className="inline-flex items-center gap-2.5 text-2xl font-bold tracking-tight text-zinc-900 dark:text-white">
            <div className="w-9 h-9 rounded-xl bg-emerald-500 flex items-center justify-center">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2L2 7l10 5 10-5-10-5z" />
                <path d="M2 17l10 5 10-5" />
                <path d="M2 12l10 5 10-5" />
              </svg>
            </div>
            NetCert
          </Link>
        </div>

        <div className="relative z-10 flex-1 flex items-center justify-center p-12">
          <div className="w-full max-w-md aspect-square">
            <NetworkTopology className="w-full h-full" />
          </div>
        </div>

        <div className="relative z-10 p-12">
          <blockquote className="text-lg font-medium text-zinc-700 dark:text-zinc-300 max-w-sm">
            &ldquo;Join thousands of engineers mastering Junos and IOS-XR with hands-on labs and adaptive practice exams.&rdquo;
          </blockquote>
          <p className="mt-3 text-sm text-zinc-500 dark:text-zinc-400">Free forever. No credit card required.</p>
        </div>
      </div>

      {/* Right: Glass register form */}
      <div className="flex-1 flex items-center justify-center px-4 py-12 bg-white dark:bg-zinc-950">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="w-full max-w-md"
        >
          {/* Mobile logo */}
          <div className="lg:hidden text-center mb-8">
            <Link href="/" className="inline-flex items-center gap-2.5 text-2xl font-bold tracking-tight text-zinc-900 dark:text-white">
              <div className="w-9 h-9 rounded-xl bg-emerald-500 flex items-center justify-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" />
                  <path d="M2 17l10 5 10-5" />
                  <path d="M2 12l10 5 10-5" />
                </svg>
              </div>
              NetCert
            </Link>
          </div>

          <div className="glass-card p-8">
            <div className="text-center mb-6">
              <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                {t("auth.createAccountTitle")}
              </h1>
              <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                {t("auth.registerSubtitle")}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-sm text-red-600 dark:text-red-400"
                >
                  {error}
                </motion.div>
              )}

              <Input
                type="text"
                label={t("auth.fullName")}
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder={t("auth.fullNamePlaceholder")}
                required
                minLength={2}
              />

              <Input
                type="email"
                label={t("auth.email")}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={t("auth.emailPlaceholder")}
                required
              />

              <Input
                type={showPassword ? "text" : "password"}
                label={t("auth.password")}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={t("auth.passwordMin")}
                required
                minLength={8}
                rightElement={(
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeSlash className="h-4 w-4" weight="regular" /> : <Eye className="h-4 w-4" weight="regular" />}
                  </button>
                )}
              />

              <label className="flex items-start gap-3 cursor-pointer group">
                <div className="relative flex items-center">
                  <input
                    type="checkbox"
                    checked={acceptTerms}
                    onChange={(e) => setAcceptTerms(e.target.checked)}
                    className="peer h-5 w-5 rounded-md border border-zinc-300 dark:border-zinc-700 bg-white/70 dark:bg-zinc-900/70 text-emerald-500 focus-visible:ring-2 focus-visible:ring-emerald-500/50 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-zinc-950 transition-all"
                  />
                  <Check className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-3.5 w-3.5 text-white opacity-0 peer-checked:opacity-100 pointer-events-none" weight="bold" />
                </div>
                <span className="text-sm text-zinc-600 dark:text-zinc-400 leading-snug group-hover:text-zinc-700 dark:group-hover:text-zinc-300 transition-colors">
                  {t("auth.acceptTerms")}
                </span>
              </label>

              <Button type="submit" variant="primary" size="lg" className="w-full group" loading={loading}>
                <UserPlus className="h-4 w-4" weight="regular" />
                {t("auth.createAccount")}
                <ArrowRight className="h-4 w-4 ml-auto transition-transform group-hover:translate-x-1" />
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              <span className="text-zinc-500 dark:text-zinc-400">{t("auth.haveAccount")}</span>{" "}
              <Link href="/auth/login" className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 font-medium transition-colors">
                {t("auth.signInLink")}
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
