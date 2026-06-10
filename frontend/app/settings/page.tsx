"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { useTranslation } from "@/lib/i18n/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
import {
  User,
  Bell,
  Shield,
  Globe,
  SignOut,
  CaretRight,
  FloppyDisk,
} from "@phosphor-icons/react";

export default function SettingsPage() {
  const { user, isAuthenticated, loading: authLoading, logout, updateProfile, updatePreferences } = useAuth();
  const { t, locale, setLocale } = useTranslation();
  const router = useRouter();

  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);
  const [langSaved, setLangSaved] = useState(false);
  const [displayName, setDisplayName] = useState("");
  const [selectedLang, setSelectedLang] = useState<string>(locale);

  const [notifExamReminders, setNotifExamReminders] = useState(true);
  const [notifWeeklyReport, setNotifWeeklyReport] = useState(true);
  const [notifNewQuestions, setNotifNewQuestions] = useState(false);
  const [notifMarketing, setNotifMarketing] = useState(false);

  const initialized = useRef(false);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (user && !initialized.current) {
      initialized.current = true;
      setDisplayName(user.display_name || "");
      setSelectedLang(user.preferences?.language || locale);
      setNotifExamReminders(user.preferences?.notifications?.exam_reminders ?? true);
      setNotifWeeklyReport(user.preferences?.notifications?.weekly_report ?? true);
      setNotifNewQuestions(user.preferences?.notifications?.new_questions ?? false);
      setNotifMarketing(user.preferences?.notifications?.marketing ?? false);
    }
  }, [user, locale]);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60dvh]">
        <Spinner />
      </div>
    );
  }

  const handleSaveProfile = async () => {
    setSaving(true);
    try {
      await updateProfile({ display_name: displayName });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      console.error("Failed to save profile:", err);
    } finally {
      setSaving(false);
    }
  };

  const handleLanguageChange = async (newLang: string) => {
    setSelectedLang(newLang);
    await setLocale(newLang as "en" | "ru");
    setLangSaved(true);
    setTimeout(() => setLangSaved(false), 2000);
  };

  const handleSaveNotifications = async () => {
    setSaving(true);
    try {
      await updatePreferences({
        language: selectedLang,
        notifications: {
          exam_reminders: notifExamReminders,
          weekly_report: notifWeeklyReport,
          new_questions: notifNewQuestions,
          marketing: notifMarketing,
        },
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (err) {
      console.error("Failed to save notifications:", err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Badge variant="secondary" className="mb-3">{t("settings.badge")}</Badge>
      <h1 className="text-3xl sm:text-4xl font-bold tracking-tighter text-zinc-900 dark:text-white mb-8">
        {t("settings.title")}
      </h1>

      <div className="space-y-6">
        {/* Profile */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5 text-emerald-600" weight="fill" />
              {t("settings.profile")}
            </CardTitle>
            <CardDescription>{t("settings.profileDesc")}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4 p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 border border-zinc-200 dark:border-zinc-800">
              <div className="w-12 h-12 rounded-full bg-emerald-100 dark:bg-emerald-900/20 flex items-center justify-center flex-shrink-0">
                <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                  {user?.display_name?.charAt(0) || "U"}
                </span>
              </div>
              <div>
                <p className="font-medium text-zinc-900 dark:text-white">{user?.display_name || "User"}</p>
                <p className="text-sm text-zinc-500">{user?.email || "user@example.com"}</p>
              </div>
              <Badge variant="outline" className="ml-auto shrink-0">
                {user?.role || "student"}
              </Badge>
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">{t("settings.displayName")}</label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
              />
            </div>
            <Button onClick={handleSaveProfile} variant="primary" disabled={saving} className="flex items-center gap-2">
              <FloppyDisk className="h-4 w-4" weight="regular" />
              {saved ? t("settings.saved") : t("settings.saveChanges")}
            </Button>
          </CardContent>
        </Card>

        {/* Language */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5 text-emerald-600" weight="fill" />
              {t("settings.language")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <select
              value={selectedLang}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
            >
              <option value="en">English</option>
              <option value="ru">Русский</option>
            </select>
            {langSaved && (
              <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">{t("settings.saved")}</p>
            )}
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5 text-emerald-600" weight="fill" />
              {t("settings.notifications")}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: "settings.examReminders", checked: notifExamReminders, setter: setNotifExamReminders },
              { label: "settings.weeklyReport", checked: notifWeeklyReport, setter: setNotifWeeklyReport },
              { label: "settings.newQuestions", checked: notifNewQuestions, setter: setNotifNewQuestions },
              { label: "settings.marketing", checked: notifMarketing, setter: setNotifMarketing },
            ].map((notif) => (
              <div key={notif.label} className="flex items-center justify-between py-1">
                <span className="text-sm text-zinc-700 dark:text-zinc-300">{t(notif.label as any)}</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={notif.checked}
                    onChange={(e) => notif.setter(e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-9 h-5 bg-zinc-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-emerald-300 dark:peer-focus:ring-emerald-800 rounded-full peer dark:bg-zinc-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-zinc-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-zinc-600 peer-checked:bg-emerald-500" />
                </label>
              </div>
            ))}
            <Button onClick={handleSaveNotifications} variant="secondary" size="sm" disabled={saving}>
              <FloppyDisk className="h-4 w-4 mr-2" weight="regular" />
              {t("settings.saveChanges")}
            </Button>
          </CardContent>
        </Card>

        {/* Sign Out */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-emerald-600" weight="fill" />
              {t("settings.accountActions")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Button variant="outline" className="w-full justify-between group" onClick={logout}>
              <span className="flex items-center gap-2">
                <SignOut className="h-4 w-4" weight="regular" />
                {t("settings.signOut")}
              </span>
              <CaretRight className="h-4 w-4 text-zinc-400 group-hover:text-zinc-600 transition-colors" weight="regular" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
