"use client";
import { useState, FormEvent } from "react";

const serviceOptions = [
  "Logo Design",
  "Book Layout",
  "Book Cover",
  "Branding",
  "Packaging Design",
  "Signboard",
  "Flyer",
  "Poster",
  "Menu",
  "Banner",
  "Website",
  "Other",
];

const budgetOptions = [
  "Under $100",
  "$100 - $300",
  "$300 - $500",
  "$500 - $1,000",
  "$1,000 - $2,500",
  "$2,500+",
];

export default function ContactForm() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    service_type: "",
    budget: "",
    description: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/leads/contact`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        }
      );
      if (res.ok) {
        setSubmitted(true);
        setForm({ name: "", email: "", service_type: "", budget: "", description: "" });
      } else {
        const text = await res.text().catch(() => "");
        setError(text || `Server error (${res.status})`);
      }
    } catch (err) {
      setError("Network error — please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="text-center py-16">
        <div className="text-4xl mb-4">✓</div>
        <h3 className="text-xl font-semibold text-zinc-900">Thank You!</h3>
        <p className="text-zinc-600 mt-2">
          I&apos;ll review your project and get back to you within 24 hours.
        </p>
        <button
          onClick={() => setSubmitted(false)}
          className="mt-6 text-sm text-amber-600 hover:text-amber-700 underline"
        >
          Submit another request
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-xl mx-auto">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-zinc-700 mb-1">
          Your Name *
        </label>
        <input
          id="name"
          required
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors"
          placeholder="John Doe"
        />
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-zinc-700 mb-1">
          Email Address *
        </label>
        <input
          id="email"
          type="email"
          required
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors"
          placeholder="john@example.com"
        />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label htmlFor="service" className="block text-sm font-medium text-zinc-700 mb-1">
            Service Needed *
          </label>
          <select
            id="service"
            required
            value={form.service_type}
            onChange={(e) => setForm({ ...form, service_type: e.target.value })}
            className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors bg-white"
          >
            <option value="">Select a service</option>
            {serviceOptions.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="budget" className="block text-sm font-medium text-zinc-700 mb-1">
            Budget Range
          </label>
          <select
            id="budget"
            value={form.budget}
            onChange={(e) => setForm({ ...form, budget: e.target.value })}
            className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors bg-white"
          >
            <option value="">Select budget</option>
            {budgetOptions.map((b) => (
              <option key={b} value={b}>
                {b}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-zinc-700 mb-1">
          Project Description *
        </label>
        <textarea
          id="description"
          required
          rows={5}
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors resize-y"
          placeholder="Tell me about your project, goals, timeline, and any specific requirements..."
        />
      </div>
      <button
        type="submit"
        disabled={loading}
        className="w-full h-12 rounded-full bg-zinc-900 text-white font-medium hover:bg-zinc-800 disabled:opacity-50 transition-colors"
      >
        {loading ? "Sending..." : "Send Request"}
      </button>
      {error && <p className="text-red-500 text-sm text-center">{error}</p>}
    </form>
  );
}
