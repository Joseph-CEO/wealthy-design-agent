"use client";
import { useState, FormEvent } from "react";

export default function ClientPortalPage() {
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [view, setView] = useState<"login" | "project">("login");

  if (view === "project") {
    return (
      <section className="py-20">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-3xl font-bold text-zinc-900">Your Project</h1>
            <p className="text-zinc-500 mt-2">Track the status of your design project.</p>
          </div>
          <div className="border border-zinc-200 rounded-xl p-8 space-y-6">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Status</span>
              <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-sm font-medium">
                In Progress
              </span>
            </div>
            <div className="border-t border-zinc-100 pt-4">
              <div className="space-y-4">
                {["Brief Received", "Design Phase", "Review", "Revisions", "Final Delivery"].map(
                  (step, i) => (
                    <div key={step} className="flex items-center gap-3">
                      <div
                        className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                          i <= 1
                            ? "bg-zinc-900 text-white"
                            : "bg-zinc-200 text-zinc-400"
                        }`}
                      >
                        {i + 1}
                      </div>
                      <span
                        className={`text-sm ${
                          i <= 1 ? "text-zinc-900 font-medium" : "text-zinc-400"
                        }`}
                      >
                        {step}
                      </span>
                    </div>
                  )
                )}
              </div>
            </div>
            <button
              onClick={() => setView("login")}
              className="text-sm text-amber-600 hover:text-amber-700 underline"
            >
              Back to login
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-20">
      <div className="max-w-md mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-zinc-900">Client Portal</h1>
          <p className="text-zinc-500 mt-2">
            Enter your email and project code to track your project.
          </p>
        </div>
        <form
          onSubmit={(e: FormEvent) => {
            e.preventDefault();
            setView("project");
          }}
          className="space-y-4"
        >
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-zinc-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label htmlFor="token" className="block text-sm font-medium text-zinc-700 mb-1">
              Project Code
            </label>
            <input
              id="token"
              required
              value={token}
              onChange={(e) => setToken(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none"
              placeholder="e.g. PROJ-001"
            />
          </div>
          <button
            type="submit"
            className="w-full h-12 rounded-full bg-zinc-900 text-white font-medium hover:bg-zinc-800 transition-colors"
          >
            Track Project
          </button>
        </form>
      </div>
    </section>
  );
}
