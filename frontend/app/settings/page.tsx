"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useTheme } from "next-themes";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { PageShell, PageHeader } from "@/components/layout/page-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { CardHeader, CardTitle, CardDescription, CardContent, GlassCard } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { SectionReveal } from "@/components/motion/SectionReveal";
import { springSnappy } from "@/lib/motion";
import {
  User,
  Bell,
  Shield,
  Globe,
  SignOut,
  Sun,
  Moon,
  Desktop,
  Trash,
  FloppyDisk,
  Check,
  Warning,
  X,
  Lock,
} from "@phosphor-icons/react";

const springQuick = { type: "spring", stiffness: 400, damping: 25 };

function Alert({ type, message, onDismiss }: { type: "success" | "error"; message: string; onDismiss?: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={springQuick}
      className={`flex items-start gap-2 rounded-xl px-4 py-3 text-sm ${
        type === "success"
          ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300"
          : "bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-300"
      }`}
    >
      {type === "success" ? (
        <Check className="h-4 w-4 mt-0.5 shrink-0" weight="bold" />
      ) : (
        <Warning className="h-4 w-4 mt-0.5 shrink-0" weight="fill" />
      )}
      <span className="flex-1">{message}</span>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="shrink-0 rounded-lg p-1 hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
          aria-label="Dismiss"
        >
          <X className="h-3.5 w-3.5" />
        </button>
      )}
    </motion.div>
  );
}

function Toggle({
  label,
  description,
  checked,
  onChange,
}: {
  label: string;
  description?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}) {
  return (
    <label className="flex items-center justify-between gap-4 py-2 cursor-pointer group">
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{label}</p>
        {description && <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{description}</p>}
      </div>
      <div className="relative inline-flex items-center shrink-0">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
          className="sr-only peer"
        />
        <div
          className={`
            w-11 h-6 rounded-full transition-colors duration-200
            bg-zinc-200 peer-checked:bg-emerald-500
            dark:bg-zinc-700 dark:peer-checked:bg-emerald-500
          `}
        />
        <div
          className={`
            absolute top-1 left-1 h-4 w-4 rounded-full bg-white shadow-sm
            transition-transform duration-200
            peer-checked:translate-x-5
          `}
        />
      </div>
    </label>
  );
}

function ThemeButton({
  active,
  onClick,
  icon: Icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ElementType;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        flex flex-1 items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium
        transition-all duration-200
        ${
          active
            ? "bg-emerald-500 text-white shadow-[0_1px_3px_rgba(16,185,129,0.2)]"
            : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
        }
      `}
    >
      <Icon className="h-4 w-4" weight={active ? "fill" : "regular"} />
      {label}
    </button>
  );
}

function LangButton({
  active,
  onClick,
  label,
  native,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
  native: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        flex flex-1 items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium
        transition-all duration-200
        ${
          active
            ? "bg-emerald-500 text-white shadow-[0_1px_3px_rgba(16,185,129,0.2)]"
            : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
        }
      `}
    >
      <span className="uppercase font-bold text-xs">{label}</span>
      <span className="text-zinc-400 dark:text-zinc-500">|</span>
      <span>{native}</span>
    </button>
  );
}

function SettingsSkeleton() {
  return (
    <div className="space-y-6">
      <div className="glass-card p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-14 w-14 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-5 w-48" />
            <Skeleton className="h-4 w-32" />
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <Skeleton className="h-14 w-full rounded-xl" />
          <Skeleton className="h-14 w-full rounded-xl" />
        </div>
      </div>
      <div className="glass-card p-6 space-y-4">
        <Skeleton className="h-6 w-32" />
        <div className="grid gap-4 sm:grid-cols-3">
          <Skeleton className="h-12 w-full rounded-xl" />
          <Skeleton className="h-12 w-full rounded-xl" />
          <Skeleton className="h-12 w-full rounded-xl" />
        </div>
      </div>
      <div className="glass-card p-6 space-y-4">
        <Skeleton className="h-6 w-40" />
        <div className="grid gap-4 sm:grid-cols-2">
          <Skeleton className="h-12 w-full rounded-xl" />
          <Skeleton className="h-12 w-full rounded-xl" />
        </div>
        <div className="space-y-3 pt-2">
          <Skeleton className="h-10 w-full rounded-xl" />
          <Skeleton className="h-10 w-full rounded-xl" />
          <Skeleton className="h-10 w-full rounded-xl" />
        </div>
      </div>
      <div className="glass-card p-6 space-y-4">
        <Skeleton className="h-6 w-36" />
        <Skeleton className="h-10 w-full rounded-xl" />
        <Skeleton className="h-10 w-full rounded-xl" />
      </div>
    </div>
  );
}

export default function SettingsPage() {
  const { user, isAuthenticated, loading: authLoading, logout, updateProfile, updatePreferences } = useAuth();
  const { t, locale, setLocale } = useTranslation();
  const { theme, setTheme } = useTheme();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const initialized = useRef(false);

  // Profile
  const [displayName, setDisplayName] = useState("");
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState<string | null>(null);
  const [profileError, setProfileError] = useState<string | null>(null);

  // Password
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);

  // Preferences
  const [selectedTheme, setSelectedTheme] = useState<"light" | "dark" | "system">("system");
  const [selectedLang, setSelectedLang] = useState<"en" | "ru">("en");
  const [notifExamReminders, setNotifExamReminders] = useState(true);
  const [notifWeeklyReport, setNotifWeeklyReport] = useState(true);
  const [notifNewQuestions, setNotifNewQuestions] = useState(false);
  const [notifMarketing, setNotifMarketing] = useState(false);
  const [prefsLoading, setPrefsLoading] = useState(false);
  const [prefsSuccess, setPrefsSuccess] = useState<string | null>(null);
  const [prefsError, setPrefsError] = useState<string | null>(null);

  // Account
  const [deleteError, setDeleteError] = useState<string | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (user && !initialized.current) {
      initialized.current = true;
      setDisplayName(user.display_name || "");
      setSelectedLang((user.preferences?.language as "en" | "ru") || locale);
      setSelectedTheme((user.preferences?.theme as "light" | "dark" | "system") || (theme as "light" | "dark" | "system") || "system");
      setNotifExamReminders(user.preferences?.notifications?.exam_reminders ?? true);
      setNotifWeeklyReport(user.preferences?.notifications?.weekly_report ?? true);
      setNotifNewQuestions(user.preferences?.notifications?.new_questions ?? false);
      setNotifMarketing(user.preferences?.notifications?.marketing ?? false);
    }
  }, [user, locale, theme]);

  const clearMessages = () => {
    setProfileSuccess(null);
    setProfileError(null);
    setPasswordSuccess(null);
    setPasswordError(null);
    setPrefsSuccess(null);
    setPrefsError(null);
    setDeleteError(null);
  };

  const handleSaveProfile = async () => {
    clearMessages();
    setProfileLoading(true);
    try {
      await updateProfile({ display_name: displayName });
      setProfileSuccess("Profile updated successfully");
    } catch (err: any) {
      setProfileError(err?.message || "Failed to update profile");
    } finally {
      setProfileLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    clearMessages();
    setPasswordError(null);
    setPasswordSuccess(null);

    if (!currentPassword) {
      setPasswordError("Current password is required");
      return;
    }
    if (newPassword.length < 8) {
      setPasswordError("New password must be at least 8 characters");
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    setPasswordLoading(true);
    // Backend password-change endpoint is not implemented yet
    setTimeout(() => {
      setPasswordLoading(false);
      setPasswordSuccess("Password change request received. Backend endpoint not yet implemented.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    }, 600);
  };

  const handleThemeChange = (value: "light" | "dark" | "system") => {
    setSelectedTheme(value);
    setTheme(value);
  };

  const handleLanguageChange = (value: "en" | "ru") => {
    setSelectedLang(value);
    setLocale(value);
  };

  const handleSavePreferences = async () => {
    clearMessages();
    setPrefsLoading(true);
    try {
      setTheme(selectedTheme);
      await setLocale(selectedLang);
      await updatePreferences({
        language: selectedLang,
        theme: selectedTheme,
        notifications: {
          exam_reminders: notifExamReminders,
          weekly_report: notifWeeklyReport,
          new_questions: notifNewQuestions,
          marketing: notifMarketing,
        },
      });
      setPrefsSuccess("Preferences saved");
    } catch (err: any) {
      setPrefsError(err?.message || "Failed to save preferences");
    } finally {
      setPrefsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  const handleDeleteAccount = () => {
    clearMessages();
    setDeleteError("Account deletion is not available yet.");
  };

  if (authLoading || !mounted) {
    return (
      <PageShell>
        <PageHeader
          badge={<Badge variant="secondary">{t("settings.badge")}</Badge>}
          title={t("settings.title")}
          subtitle="Manage your profile, preferences, and account security."
        />
        <SettingsSkeleton />
      </PageShell>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <PageShell>
      <PageHeader
        badge={<Badge variant="secondary">{t("settings.badge")}</Badge>}
        title={t("settings.title")}
        subtitle="Manage your profile, preferences, and account security."
      />

      <div className="space-y-6 max-w-3xl">
        {/* Profile */}
        <SectionReveal>
          <GlassCard>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5 text-emerald-500" weight="fill" />
                {t("settings.profile")}
              </CardTitle>
              <CardDescription>{t("settings.profileDesc")}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-zinc-50/80 border border-zinc-200 dark:bg-zinc-800/50 dark:border-zinc-800">
                <div className="h-14 w-14 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center flex-shrink-0">
                  <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                    {user?.display_name?.charAt(0) || "U"}
                  </span>
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-semibold text-zinc-900 dark:text-white truncate">
                    {user?.display_name || "User"}
                  </p>
                  <p className="text-sm text-zinc-500 truncate">{user?.email || "user@example.com"}</p>
                </div>
                <Badge variant="outline" className="shrink-0 capitalize">
                  {user?.role || "student"}
                </Badge>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <Input
                  label={t("settings.displayName")}
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="Your display name"
                />
                <Input
                  label={t("settings.email")}
                  type="email"
                  value={user?.email || ""}
                  disabled
                  helper="Email cannot be changed here."
                />
              </div>

              <AnimatePresence mode="wait">
                {profileSuccess && (
                  <Alert type="success" message={profileSuccess} onDismiss={() => setProfileSuccess(null)} />
                )}
                {profileError && (
                  <Alert type="error" message={profileError} onDismiss={() => setProfileError(null)} />
                )}
              </AnimatePresence>

              <div className="flex justify-end">
                <Button
                  onClick={handleSaveProfile}
                  disabled={profileLoading}
                  loading={profileLoading}
                  className="w-full sm:w-auto"
                >
                  <FloppyDisk className="h-4 w-4" />
                  {t("settings.saveChanges")}
                </Button>
              </div>
            </CardContent>
          </GlassCard>
        </SectionReveal>

        {/* Password */}
        <SectionReveal delay={0.05}>
          <GlassCard>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lock className="h-5 w-5 text-emerald-500" weight="fill" />
                Change Password
              </CardTitle>
              <CardDescription>Update your password to keep your account secure.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleChangePassword} className="space-y-4">
                <Input
                  label="Current Password"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Enter current password"
                  autoComplete="current-password"
                />
                <div className="grid gap-4 sm:grid-cols-2">
                  <Input
                    label="New Password"
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="At least 8 characters"
                    autoComplete="new-password"
                  />
                  <Input
                    label="Confirm New Password"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter new password"
                    autoComplete="new-password"
                    error={
                      confirmPassword && newPassword !== confirmPassword
                        ? "Passwords do not match"
                        : undefined
                    }
                  />
                </div>

                <AnimatePresence mode="wait">
                  {passwordSuccess && (
                    <Alert type="success" message={passwordSuccess} onDismiss={() => setPasswordSuccess(null)} />
                  )}
                  {passwordError && (
                    <Alert type="error" message={passwordError} onDismiss={() => setPasswordError(null)} />
                  )}
                </AnimatePresence>

                <div className="flex justify-end">
                  <Button
                    type="submit"
                    variant="secondary"
                    disabled={passwordLoading}
                    loading={passwordLoading}
                    className="w-full sm:w-auto"
                  >
                    <Lock className="h-4 w-4" />
                    Change Password
                  </Button>
                </div>
              </form>
            </CardContent>
          </GlassCard>
        </SectionReveal>

        {/* Preferences */}
        <SectionReveal delay={0.1}>
          <GlassCard>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-emerald-500" weight="fill" />
                Preferences
              </CardTitle>
              <CardDescription>Choose how NetCert looks and notifies you.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Theme */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex items-center gap-2">
                  <Sun className="h-4 w-4" />
                  Theme
                </label>
                <div className="grid grid-cols-3 gap-2">
                  <ThemeButton
                    active={selectedTheme === "light"}
                    onClick={() => handleThemeChange("light")}
                    icon={Sun}
                    label="Light"
                  />
                  <ThemeButton
                    active={selectedTheme === "dark"}
                    onClick={() => handleThemeChange("dark")}
                    icon={Moon}
                    label="Dark"
                  />
                  <ThemeButton
                    active={selectedTheme === "system"}
                    onClick={() => handleThemeChange("system")}
                    icon={Desktop}
                    label="System"
                  />
                </div>
              </div>

              {/* Language */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300 flex items-center gap-2">
                  <Globe className="h-4 w-4" />
                  Language
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <LangButton
                    active={selectedLang === "en"}
                    onClick={() => handleLanguageChange("en")}
                    label="EN"
                    native="English"
                  />
                  <LangButton
                    active={selectedLang === "ru"}
                    onClick={() => handleLanguageChange("ru")}
                    label="RU"
                    native="Русский"
                  />
                </div>
              </div>

              {/* Notifications */}
              <div className="space-y-1 pt-2 border-t border-zinc-200 dark:border-zinc-800">
                <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2 flex items-center gap-2">
                  <Bell className="h-4 w-4" />
                  Notifications
                </p>
                <Toggle
                  label="Exam reminders"
                  description="Get notified before scheduled exams."
                  checked={notifExamReminders}
                  onChange={setNotifExamReminders}
                />
                <Toggle
                  label="Weekly progress report"
                  description="A summary of your weekly study activity."
                  checked={notifWeeklyReport}
                  onChange={setNotifWeeklyReport}
                />
                <Toggle
                  label="New questions available"
                  description="Be the first to know when new questions are added."
                  checked={notifNewQuestions}
                  onChange={setNotifNewQuestions}
                />
                <Toggle
                  label="Marketing emails"
                  description="Receive updates about features and offers."
                  checked={notifMarketing}
                  onChange={setNotifMarketing}
                />
              </div>

              <AnimatePresence mode="wait">
                {prefsSuccess && (
                  <Alert type="success" message={prefsSuccess} onDismiss={() => setPrefsSuccess(null)} />
                )}
                {prefsError && (
                  <Alert type="error" message={prefsError} onDismiss={() => setPrefsError(null)} />
                )}
              </AnimatePresence>

              <div className="flex justify-end">
                <Button
                  onClick={handleSavePreferences}
                  disabled={prefsLoading}
                  loading={prefsLoading}
                  className="w-full sm:w-auto"
                >
                  <FloppyDisk className="h-4 w-4" />
                  {t("settings.saveChanges")}
                </Button>
              </div>
            </CardContent>
          </GlassCard>
        </SectionReveal>

        {/* Account actions */}
        <SectionReveal delay={0.15}>
          <GlassCard>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5 text-emerald-500" weight="fill" />
                {t("settings.accountActions")}
              </CardTitle>
              <CardDescription>Session and account management.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button
                variant="outline"
                onClick={handleLogout}
                className="w-full justify-between group"
              >
                <span className="flex items-center gap-2">
                  <SignOut className="h-4 w-4" />
                  {t("settings.signOut")}
                </span>
                <motion.span
                  className="text-zinc-400 group-hover:text-zinc-600 dark:group-hover:text-zinc-300 transition-colors"
                  whileHover={{ x: 2 }}
                  transition={springSnappy}
                >
                  →
                </motion.span>
              </Button>

              <div className="pt-2 border-t border-zinc-200 dark:border-zinc-800">
                <Button
                  variant="danger"
                  onClick={handleDeleteAccount}
                  className="w-full justify-between group"
                >
                  <span className="flex items-center gap-2">
                    <Trash className="h-4 w-4" />
                    Delete Account
                  </span>
                </Button>
                <p className="mt-2 text-xs text-zinc-500 dark:text-zinc-400">
                  This will permanently remove your account and all associated data.
                </p>
              </div>

              <AnimatePresence mode="wait">
                {deleteError && (
                  <Alert type="error" message={deleteError} onDismiss={() => setDeleteError(null)} />
                )}
              </AnimatePresence>
            </CardContent>
          </GlassCard>
        </SectionReveal>
      </div>
    </PageShell>
  );
}
