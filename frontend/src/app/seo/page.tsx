"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface ServiceInfo {
  type: string;
  page_count: number;
}

interface CountyInfo {
  name: string;
  page_count: number;
}

export default function SEOPage() {
  const [services, setServices] = useState<ServiceInfo[]>([]);
  const [counties, setCounties] = useState<CountyInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/seo/services`).then(r => r.json()),
      fetch(`${API_BASE}/seo/counties`).then(r => r.json()),
    ]).then(([s, c]) => {
      setServices(s.services || []);
      setCounties(c.counties || []);
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const formatService = (type: string) =>
    type.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");

  if (loading) {
    return (
      <div className="py-32 text-center text-zinc-400">
        Loading...
      </div>
    );
  }

  return (
    <section className="py-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-zinc-900">
            Design Services Across Kenya
          </h1>
          <p className="mt-4 text-zinc-600 max-w-2xl mx-auto">
            Professional graphic design services tailored for businesses in every county.
            Browse by service type or location.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-2xl font-bold text-zinc-900 mb-6">Services</h2>
            <div className="space-y-3">
              {services.map((s) => (
                <Link
                  key={s.type}
                  href={`/seo/service/${s.type}`}
                  className="flex items-center justify-between p-4 rounded-xl border border-zinc-200 hover:border-amber-200 hover:shadow-sm transition-all"
                >
                  <span className="font-medium text-zinc-900">{formatService(s.type)}</span>
                  <span className="text-sm text-zinc-400">{s.page_count} pages</span>
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-zinc-900 mb-6">Counties</h2>
            <div className="space-y-3">
              {counties.map((c) => (
                <Link
                  key={c.name}
                  href={`/seo/county/${c.name.toLowerCase().replace(/\s+/g, "-")}`}
                  className="flex items-center justify-between p-4 rounded-xl border border-zinc-200 hover:border-amber-200 hover:shadow-sm transition-all"
                >
                  <span className="font-medium text-zinc-900">{c.name}</span>
                  <span className="text-sm text-zinc-400">{c.page_count} pages</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
