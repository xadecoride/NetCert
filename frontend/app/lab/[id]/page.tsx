"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect } from "react";

export default function LabLegacyRedirectPage() {
  const params = useParams();
  const router = useRouter();
  const labId = params.id as string;

  useEffect(() => {
    if (labId) {
      router.replace(`/labs/${labId}`);
    }
  }, [labId, router]);

  return null;
}
