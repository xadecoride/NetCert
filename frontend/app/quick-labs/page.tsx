"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function QuickLabsRedirectPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/labs");
  }, [router]);
  return null;
}
