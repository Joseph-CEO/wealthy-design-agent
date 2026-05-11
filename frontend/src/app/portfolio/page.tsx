"use client";
import { useState } from "react";
import PortfolioGrid from "@/components/PortfolioGrid";

const categories = [
  { value: "", label: "All" },
  { value: "logo_design", label: "Logos" },
  { value: "branding", label: "Branding" },
  { value: "advertising_marketing", label: "Advertising" },
  { value: "web_ui", label: "Web & UI" },
  { value: "ux_design", label: "UX Design" },
  { value: "publication_editorial", label: "Publications" },
  { value: "book_cover", label: "Book Covers" },
  { value: "book_layout", label: "Book Layouts" },
  { value: "packaging_design", label: "Packaging" },
  { value: "environmental_experiential", label: "Experiential" },
  { value: "signboard", label: "Signboards" },
  { value: "information_data_viz", label: "Data Viz" },
  { value: "illustration_concept_art", label: "Illustration" },
  { value: "environmental_graphics", label: "Env. Graphics" },
  { value: "flyer", label: "Flyers" },
  { value: "poster", label: "Posters" },
  { value: "menu", label: "Menus" },
  { value: "banner", label: "Banners" },
  { value: "website", label: "Websites" },
];

export default function PortfolioPage() {
  const [category, setCategory] = useState("");

  return (
    <section className="py-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-zinc-900">
            Portfolio
          </h1>
          <p className="mt-4 text-zinc-600 max-w-xl mx-auto">
            A showcase of projects I&apos;ve delivered for clients around the world.
            <br />
            <span className="text-sm text-zinc-400">
              (Placeholder images shown — real portfolio coming soon)
            </span>
          </p>
        </div>
        <div className="flex flex-wrap justify-center gap-2 mb-12">
          {categories.map((c) => (
            <button
              key={c.value}
              onClick={() => setCategory(c.value)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                category === c.value
                  ? "bg-zinc-900 text-white"
                  : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>
        <PortfolioGrid />
      </div>
    </section>
  );
}
