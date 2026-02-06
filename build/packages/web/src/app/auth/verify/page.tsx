"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuthStore } from "@/stores/auth-store";

function VerifyContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<"verifying" | "error">("verifying");
  const [error, setError] = useState("");
  const { setAuth } = useAuthStore();

  useEffect(() => {
    const token = searchParams.get("token");
    if (!token) {
      setStatus("error");
      setError("No token provided");
      return;
    }

    const verify = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/verify/${token}`
        );

        if (res.ok) {
          const data = await res.json();
          setAuth(data.access_token, data.refresh_token, data.user);
          router.replace("/dashboard");
        } else {
          const data = await res.json();
          setStatus("error");
          setError(data.detail || "Invalid or expired link");
        }
      } catch {
        setStatus("error");
        setError("Unable to verify. Please try again.");
      }
    };

    verify();
  }, [searchParams, router, setAuth]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-muted">
      <div className="text-center">
        {status === "verifying" && (
          <>
            <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-body text-[rgb(var(--color-text-secondary))]">
              Verifying your login link...
            </p>
          </>
        )}

        {status === "error" && (
          <>
            <div className="text-4xl mb-4">😕</div>
            <h2 className="text-h3 mb-2">Link expired or invalid</h2>
            <p className="text-body text-[rgb(var(--color-text-secondary))] mb-4">
              {error}
            </p>
            <a
              href="/auth/login"
              className="inline-block px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-white font-medium transition-colors"
            >
              Request a new link
            </a>
          </>
        )}
      </div>
    </div>
  );
}

export default function VerifyPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-surface-muted">
          <div className="text-center">
            <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full mx-auto mb-4" />
            <p className="text-body text-[rgb(var(--color-text-secondary))]">
              Verifying your login link...
            </p>
          </div>
        </div>
      }
    >
      <VerifyContent />
    </Suspense>
  );
}
