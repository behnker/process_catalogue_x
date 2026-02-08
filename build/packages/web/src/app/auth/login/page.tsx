"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth-store";

type LoginState = "email" | "sent" | "error";

const isDev = process.env.NODE_ENV === "development";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [state, setState] = useState<LoginState>("email");
  const [isLoading, setIsLoading] = useState(false);
  const [devLoading, setDevLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleDevLogin = async () => {
    setDevLoading(true);
    setError("");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/dev-login`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        }
      );

      if (res.ok) {
        const data = await res.json();
        setAuth(data.access_token, data.refresh_token, data.user);
        router.push("/dashboard");
      } else {
        const data = await res.json();
        setError(data.detail || "Dev login failed");
        setState("error");
      }
    } catch {
      setError("API not running. Start the backend with: cd build/packages/api && uvicorn src.main:app --reload");
      setState("error");
    } finally {
      setDevLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/magic-link`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        }
      );

      if (res.ok) {
        setState("sent");
      } else {
        const data = await res.json();
        setError(data.detail || "Something went wrong");
        setState("error");
      }
    } catch {
      setError("Unable to connect. Please check your connection.");
      setState("error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[rgb(var(--color-background))] p-4">
      {/* Subtle background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:20px_20px] opacity-40 dark:opacity-5" />

      <div className="relative w-full max-w-md">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-brand-500 text-white text-2xl font-bold mb-4">
            PC
          </div>
          <h1 className="text-h2 text-[rgb(var(--color-text))]">
            Process Catalogue
          </h1>
        </div>

        {/* Card */}
        <div className="bg-white dark:bg-[rgb(var(--color-surface))] rounded-xl shadow-lg border border-[rgb(var(--color-border))] p-8">
          {state === "email" && (
            <>
              <h2 className="text-h3 text-[rgb(var(--color-text))] mb-1">Sign in</h2>
              <p className="text-[rgb(var(--color-text-secondary))] text-body mb-6">
                Enter your work email address
              </p>

              <form onSubmit={handleSubmit}>
                <label htmlFor="email" className="block text-body-sm font-medium text-[rgb(var(--color-text))] mb-1.5">
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  required
                  autoFocus
                  className="w-full px-3 py-2.5 rounded-lg border border-[rgb(var(--color-border))] bg-white dark:bg-[rgb(var(--color-background))] text-body text-[rgb(var(--color-text))] focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-colors"
                />

                {error && (
                  <p className="mt-2 text-caption text-red-600">{error}</p>
                )}

                <button
                  type="submit"
                  disabled={isLoading || !email}
                  className="w-full mt-4 px-4 py-2.5 rounded-lg bg-brand-500 hover:bg-brand-600 text-white font-semibold text-body transition-colors disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2"
                >
                  {isLoading ? "Sending..." : "Send Login Link →"}
                </button>
              </form>

              <p className="mt-4 text-center text-caption text-[rgb(var(--color-text-secondary))]">
                We'll email you a link to sign in.
                <br />
                No password needed.
              </p>

              {isDev && (
                <div className="mt-6 pt-6 border-t border-[rgb(var(--color-border))]">
                  <p className="text-center text-caption text-[rgb(var(--color-text-secondary))] mb-3">
                    Development Mode
                  </p>
                  <button
                    type="button"
                    onClick={handleDevLogin}
                    disabled={devLoading}
                    className="w-full px-4 py-2.5 rounded-lg bg-gray-800 hover:bg-gray-900 text-white font-semibold text-body transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {devLoading ? "Logging in..." : "Dev Login (Admin)"}
                  </button>
                </div>
              )}
            </>
          )}

          {state === "sent" && (
            <div className="text-center">
              <div className="text-4xl mb-4">✉️</div>
              <h2 className="text-h3 text-[rgb(var(--color-text))] mb-2">Check your email</h2>
              <p className="text-[rgb(var(--color-text-secondary))] text-body mb-1">
                We sent a login link to
              </p>
              <p className="font-semibold text-body text-[rgb(var(--color-text))] mb-4">{email}</p>
              <p className="text-caption text-[rgb(var(--color-text-secondary))] mb-6">
                The link expires in 15 minutes.
              </p>

              <button
                onClick={() => {
                  setState("email");
                  handleSubmit(new Event("submit") as unknown as React.FormEvent);
                }}
                className="text-brand-600 hover:text-brand-700 font-medium text-body-sm"
              >
                Resend Link
              </button>

              <div className="mt-4">
                <button
                  onClick={() => {
                    setState("email");
                    setEmail("");
                  }}
                  className="text-[rgb(var(--color-text-secondary))] hover:text-[rgb(var(--color-text))] text-caption"
                >
                  Wrong email? Try again
                </button>
              </div>
            </div>
          )}

          {state === "error" && (
            <div className="text-center">
              <div className="text-4xl mb-4">😕</div>
              <h2 className="text-h3 text-[rgb(var(--color-text))] mb-2">Something went wrong</h2>
              <p className="text-[rgb(var(--color-text-secondary))] text-body mb-4">
                {error}
              </p>
              <button
                onClick={() => setState("email")}
                className="px-4 py-2 rounded-lg bg-brand-500 hover:bg-brand-600 text-white font-medium text-body transition-colors"
              >
                Try again
              </button>
            </div>
          )}
        </div>

        {/* Version */}
        <p className="text-center mt-6 text-caption text-[rgb(var(--color-text-secondary))]">
          v{process.env.NEXT_PUBLIC_APP_VERSION || "0.1.0"}
        </p>
      </div>
    </div>
  );
}
