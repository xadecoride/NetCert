"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "./auth-context";
import { Spinner } from "@/components/ui/spinner";

export function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { isAuthenticated, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
      if (!loading && !isAuthenticated) {
        router.replace("/auth/login");
      }
    }, [loading, isAuthenticated, router]);

    if (loading) {
      return (
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner />
        </div>
      );
    }

    if (!isAuthenticated) {
      return (
        <div className="flex items-center justify-center min-h-[100dvh]">
          <Spinner />
        </div>
      );
    }

    return <Component {...props} />;
  };
}
