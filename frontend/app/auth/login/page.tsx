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
  SignIn,
  Eye,
  EyeSlash,
  Bug,
  ArrowRight,
} from "@phosphor-icons/react";

const isDev = process.env.NODE_ENV === "development";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const { login, devLogin } = useAuth();
  const { t } = useTranslation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  const handleDevLogin = async () => {
    setError("");
    setLoading(true);
    try {
      await devLogin(email || undefined);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Dev login failed");
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
            &ldquo;The most realistic certification preparation platform for Juniper and Cisco exams.&rdquo;
          </blockquote>
          <p className="mt-3 text-sm text-zinc-500 dark:text-zinc-400">Built for network engineers, by network engineers.</p>
        </div>
      </div>

      {/* Right: Glass login form */}
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
                {t("auth.welcomeBack")}
              </h1>
              <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                {t("auth.signInSubtitle")}
              </p>
            </div>

            {isDev && (
              <div className="p-3 rounded-xl border border-amber-300/30 bg-amber-50/50 dark:bg-amber-900/10 dark:border-amber-700/30 mb-6">
                <p className="text-xs text-amber-600 dark:text-amber-400 mb-2 font-medium">
                  {t("auth.devMode")}
                </p>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className="w-full border-amber-300/50 text-amber-600 hover:bg-amber-100 dark:border-amber-700/30 dark:text-amber-400 dark:hover:bg-amber-900/20"
                  onClick={handleDevLogin}
                  loading={loading}
                >
                  <Bug className="h-4 w-4 mr-2" weight="regular" />
                  {t("auth.devLogin")}
                </Button>
              </div>
            )}

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
                placeholder={t("auth.passwordPlaceholder")}
                required
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

              <Button type="submit" variant="primary" size="lg" className="w-full group" loading={loading}>
                <SignIn className="h-4 w-4" weight="regular" />
                {t("auth.signInButton")}
                <ArrowRight className="h-4 w-4 ml-auto transition-transform group-hover:translate-x-1" />
              </Button>
            </form>

            <div className="mt-6 text-center text-sm">
              <span className="text-zinc-500 dark:text-zinc-400">{t("auth.noAccount")}</span>{" "}
              <Link href="/auth/register" className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 font-medium transition-colors">
                {t("auth.createOne")}
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
