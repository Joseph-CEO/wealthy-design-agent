"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface SEOPageData {
  id: number;
  slug: string;
  service_type: string;
  county: string;
  industry: string;
  title: string;
  meta_description: string;
  h1: string;
  body_html: string;
  portfolio_examples: string[];
  pricing_html: string;
  cta_text: string;
  published: boolean;
  created_at: string | null;
}

export default function SEOIndividualPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [page, setPage] = useState<SEOPageData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/seo/pages/${slug}`)
      .then(r => r.json())
      .then(data => setPage(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [slug]);

  const formatService = (s: string) =>
    s.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");

  if (loading) {
    return <div className="py-32 text-center text-zinc-400">Loading...</div>;
  }

  if (!page) {
    return (
      <div className="py-32 text-center">
        <h1 className="text-2xl font-bold text-zinc-900 mb-4">Page Not Found</h1>
        <Link href="/seo" className="text-amber-600 hover:text-amber-700">Browse SEO Pages</Link>
      </div>
    );
  }

  return (
    <article className="py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link href="/seo" className="text-sm text-amber-600 hover:text-amber-700 mb-6 inline-block">
          &larr; Browse All Services
        </Link>

        <h1 className="text-3xl sm:text-4xl font-bold text-zinc-900 mb-4">{page.h1}</h1>
        <p className="text-lg text-zinc-600 mb-8">{page.meta_description}</p>

        <div className="flex gap-2 mb-8 flex-wrap">
          <Link href={`/seo/service/${page.service_type}`}
            className="text-xs bg-amber-50 px-3 py-1.5 rounded-full text-amber-700 hover:bg-amber-100">
            {formatService(page.service_type)}
          </Link>
          <Link href={`/seo/county/${page.county.toLowerCase().replace(/\s+/g, "-")}`}
            className="text-xs bg-zinc-100 px-3 py-1.5 rounded-full text-zinc-600 hover:bg-zinc-200">
            {page.county}
          </Link>
          {page.industry && (
            <span className="text-xs bg-zinc-100 px-3 py-1.5 rounded-full text-zinc-600">
              {page.industry}
            </span>
          )}
        </div>

        {page.portfolio_examples.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-bold text-zinc-900 mb-4">Portfolio Examples</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {page.portfolio_examples.map((url, i) => (
                <img key={i} src={url} alt="Portfolio example" className="rounded-xl border border-zinc-200" />
              ))}
            </div>
          </div>
        )}

        <div
          className="prose prose-zinc max-w-none mb-8"
          dangerouslySetInnerHTML={{ __html: page.body_html }}
        />

        <div
          className="bg-zinc-50 rounded-xl p-6 mb-8"
          dangerouslySetInnerHTML={{ __html: page.pricing_html }}
        />

        <div className="text-center">
          <Link
            href="/contact"
            className="inline-flex h-14 items-center justify-center rounded-full bg-zinc-900 px-10 text-white font-medium hover:bg-zinc-800 transition-colors"
          >
            {page.cta_text}
          </Link>
        </div>
      </div>
    </article>
  );
}
