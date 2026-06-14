"use client";

import { Toaster as SonnerToaster, toast as sonnerToast } from "sonner";

export const Toaster = () => (
  <SonnerToaster
    position="bottom-right"
    toastOptions={{
      className:
        "bg-white/90 dark:bg-zinc-900/90 backdrop-blur-xl border border-zinc-200 dark:border-zinc-800 text-zinc-900 dark:text-zinc-100 shadow-diffuse-lg rounded-xl",
    }}
  />
);

export const toast = sonnerToast;
