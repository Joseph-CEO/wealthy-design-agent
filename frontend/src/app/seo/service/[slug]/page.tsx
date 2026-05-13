"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

const API_BASE = "https://api-production-8de3.up.railway.app/api/v1";

interface SEOPageItem {
  id: number;
  slug: string;
  service_type: string;
  county: string;
  industry: string;
  title: string;
  meta_description: string;
  h1: string;
  published: boolean;
  created_at: string | null;
}

export default function SEOServicePage() {
  const params = useParams();
  const slug = params.slug as string;
  const [pages, setPages] = useState<SEOPageItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/seo/pages?service_type=${slug}&limit=200`)
      .then(r => r.json())
      .then(data => setPages(data.pages || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [slug]);

  const formatName = (s: string) =>
    s.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");

  if (loading) {
    return <div className="py-32 text-center text-zinc-400">Loading...</div>;
  }

  return (
    <section className="py-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link href="/seo" className="text-sm text-amber-600 hover:text-amber-700 mb-6 inline-block">
          &larr; Back to SEO Pages
        </Link>
        <h1 className="text-3xl sm:text-4xl font-bold text-zinc-900 mb-2">
          {formatName(slug)}
        </h1>
        <p className="text-zinc-600 mb-8">{pages.length} location pages</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {pages.map((page) => (
            <Link
              key={page.id}
              href={`/seo/page/${page.slug}`}
              className="p-5 rounded-xl border border-zinc-200 hover:border-amber-200 hover:shadow-sm transition-all"
            >
              <h2 className="font-semibold text-zinc-900 mb-2">{page.title}</h2>
              <p className="text-sm text-zinc-500 line-clamp-2">{page.meta_description}</p>
              <div className="flex gap-2 mt-3">
                <span className="text-xs bg-zinc-100 px-2 py-1 rounded-full text-zinc-600">{page.county}</span>
                {page.industry && (
                  <span className="text-xs bg-amber-50 px-2 py-1 rounded-full text-amber-700">{page.industry}</span>
                )}
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
