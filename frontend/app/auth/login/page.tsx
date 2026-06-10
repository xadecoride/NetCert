"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { Spinner } from "@/components/ui/spinner";
import { Button } from "@/components/ui/button";
import {
  SignIn,
  Eye,
  EyeSlash,
  Bug,
} from "@phosphor-icons/react";

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

  return (
    <div className="min-h-[100dvh] flex items-center justify-center px-4 py-12 bg-zinc-50 dark:bg-zinc-950">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
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

        {/* Card */}
        <div className="glass-card p-8">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
              {t("auth.welcomeBack")}
            </h1>
            <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
              {t("auth.signInSubtitle")}
            </p>
          </div>

          {/* Dev Login */}
          <div className="p-3 rounded-xl border border-amber-300/30 bg-amber-50/50 dark:bg-amber-900/10 dark:border-amber-700/30 mb-6">
            <p className="text-xs text-amber-600 dark:text-amber-400 mb-2 font-medium">
              {t("auth.devMode")}
            </p>
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="w-full border-amber-300/50 text-amber-600 hover:bg-amber-100 dark:border-amber-700/30 dark:text-amber-400 dark:hover:bg-amber-900/20"
              onClick={async () => {
                setLoading(true);
                try {
                  await devLogin(email || undefined);
                  router.push("/dashboard");
                } catch (err: any) {
                  setError(err.message || "Dev login failed");
                } finally {
                  setLoading(false);
                }
              }}
              disabled={loading}
            >
              <Bug className="h-4 w-4 mr-2" weight="regular" />
              {t("auth.devLogin")}
            </Button>
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

            <div className="space-y-1.5">
              <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {t("auth.email")}
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-zinc-300 bg-white text-zinc-900 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
                placeholder={t("auth.emailPlaceholder")}
                required
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {t("auth.password")}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 pr-10 rounded-xl border border-zinc-300 bg-white text-zinc-900 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
                  placeholder={t("auth.passwordPlaceholder")}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                >
                  {showPassword ? <EyeSlash className="h-4 w-4" weight="regular" /> : <Eye className="h-4 w-4" weight="regular" />}
                </button>
              </div>
            </div>

            <Button type="submit" variant="primary" size="lg" className="w-full" disabled={loading}>
              {loading ? (
                <span className="flex items-center gap-2">
                  <Spinner size="sm" />
                  {t("auth.signingIn")}
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <SignIn className="h-4 w-4" weight="regular" />
                  {t("auth.signInButton")}
                </span>
              )}
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
  );
}


