import { Spinner } from "@/components/ui/spinner";

export default function LoadingPage() {
  return (
    <div className="min-h-[calc(100dvh-4rem)] flex items-center justify-center bg-zinc-50 dark:bg-zinc-950">
      <div className="flex flex-col items-center gap-4">
        <Spinner className="h-10 w-10 text-emerald-500" />
        <p className="text-sm text-zinc-400 dark:text-zinc-500">Loading...</p>
      </div>
    </div>
  );
}
