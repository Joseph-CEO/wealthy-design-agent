"use client";

import type { FormEvent } from "react";
import { useState } from "react";

const API_BASE = "https://api-production-8de3.up.railway.app/api/v1";

export default function PaymentPage() {
  const [projectId, setProjectId] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ type: "stripe" | "mpesa"; url?: string; message: string } | null>(null);
  const [phone, setPhone] = useState("");

  async function payStripe(e: FormEvent) {
    e.preventDefault();
    if (!projectId) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/payments/create-checkout-session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: parseInt(projectId),
          success_url: window.location.origin + "/payment/success",
          cancel_url: window.location.origin + "/payment/cancel",
        }),
      });
      if (!res.ok) {
        const err = await res.text();
        setResult({ type: "stripe", message: `Error: ${err}` });
        return;
      }
      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      } else {
        setResult({ type: "stripe", message: "No checkout URL returned" });
      }
    } catch (err: any) {
      setResult({ type: "stripe", message: `Error: ${err.message}` });
    } finally {
      setLoading(false);
    }
  }

  async function payMpesa(e: FormEvent) {
    e.preventDefault();
    if (!projectId || !phone) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/payments/mpesa-stk-push`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id: parseInt(projectId), phone_number: phone }),
      });
      if (!res.ok) {
        const err = await res.text();
        setResult({ type: "mpesa", message: `Error: ${err}` });
        return;
      }
      const data = await res.json();
      if (data.response_code === "0") {
        setResult({ type: "mpesa", message: "STK Push sent! Check your phone to complete payment." });
      } else {
        setResult({ type: "mpesa", message: `Payment failed: ${data.response_description || "Unknown error"}` });
      }
    } catch (err: any) {
      setResult({ type: "mpesa", message: `Error: ${err.message}` });
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="py-20">
      <div className="max-w-lg mx-auto px-4">
        <h1 className="text-3xl font-bold text-zinc-900 mb-2">Pay for Your Project</h1>
        <p className="text-zinc-500 mb-8">Enter your project ID to make a payment.</p>

        <div className="space-y-4 mb-6">
          <input
            type="number"
            placeholder="Project ID"
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 outline-none"
          />
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <form onSubmit={payStripe}>
            <button
              type="submit"
              disabled={loading || !projectId}
              className="w-full h-12 rounded-full bg-indigo-600 text-white font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
            >
              {loading ? "..." : "Pay with Card"}
            </button>
          </form>
          <div className="space-y-2">
            <input
              type="tel"
              placeholder="M-Pesa phone (e.g. 0712345678)"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-zinc-300 text-sm focus:border-amber-500 outline-none"
            />
            <form onSubmit={payMpesa}>
              <button
                type="submit"
                disabled={loading || !projectId || !phone}
                className="w-full h-10 rounded-full bg-green-600 text-white font-medium text-sm hover:bg-green-700 disabled:opacity-50 transition-colors"
              >
                {loading ? "..." : "Pay with M-Pesa"}
              </button>
            </form>
          </div>
        </div>

        {result && (
          <div className={`p-4 rounded-xl text-sm ${
            result.message.startsWith("Error") ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700"
          }`}>
            {result.message}
          </div>
        )}

        <p className="text-xs text-zinc-400 mt-8 text-center">
          Secured by Stripe and Safaricom M-Pesa.
        </p>
      </div>
    </section>
  );
}
