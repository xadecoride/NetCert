"use client";

import { useParams } from "next/navigation";
import { Suspense } from "react";
import { Spinner } from "@phosphor-icons/react";
import { withAuth } from "@/lib/with-auth";
import { LabWorkspace } from "@/components/lab/LabWorkspace";

function LabWorkspacePageContent() {
  const params = useParams();
  const submissionId = params.submissionId as string;
  return <LabWorkspace submissionId={submissionId} />;
}

function LabWorkspacePage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center min-h-[100dvh] bg-zinc-50 dark:bg-zinc-950">
          <Spinner className="h-8 w-8 text-emerald-500 animate-spin" weight="bold" />
        </div>
      }
    >
      <LabWorkspacePageContent />
    </Suspense>
  );
}

export default withAuth(LabWorkspacePage);
