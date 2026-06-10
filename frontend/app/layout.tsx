import type { Metadata } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import { AuthProvider } from "@/lib/auth-context";
import { I18nProvider } from "@/lib/i18n/context";
import { Header } from "@/components/layout/header";
import "./globals.css";

export const metadata: Metadata = {
  title: "NetCert — Certification Preparation Platform",
  description:
    "Free platform for Juniper (JNCIA–JNCIE) and Cisco (CCNA–CCIE) certification preparation with adaptive testing, detailed analytics, and interactive labs.",
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable}`} suppressHydrationWarning>
      <body className="min-h-[100dvh] antialiased">
        <AuthProvider>
          <I18nProvider>
            <Header />
            <main className="min-h-[calc(100dvh-4rem)]">{children}</main>
          </I18nProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
