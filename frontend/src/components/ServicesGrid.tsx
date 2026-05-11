import Link from "next/link";

const services = [
  { title: "Logo Design", desc: "Memorable logos that capture your brand essence.", icon: "✦" },
  { title: "Brand Identity", desc: "Complete visual systems — colors, typography, guidelines.", icon: "◆" },
  { title: "Advertising & Marketing", desc: "Print, digital & social media campaign assets.", icon: "▣" },
  { title: "Web Design & UI", desc: "Clean websites and app interfaces that convert.", icon: "◎" },
  { title: "UX Design", desc: "Wireframes, prototypes, user journeys & usability.", icon: "⬡" },
  { title: "Publication & Editorial", desc: "Magazines, books, reports & catalogues.", icon: "📖" },
  { title: "Packaging Design", desc: "Shelf-ready packaging that tells your story.", icon: "📦" },
  { title: "Environmental & Experiential", desc: "Signage, wayfinding, retail & event graphics.", icon: "◈" },
  { title: "Data Visualization", desc: "Infographics, dashboards & visualized reports.", icon: "⬟" },
  { title: "Illustration & Concept Art", desc: "Custom artwork for storytelling and branding.", icon: "✎" },
  { title: "Environmental Graphics", desc: "Wall murals, large-format & public installations.", icon: "▥" },
];

export default function ServicesGrid() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-900">
            What I Do
          </h2>
          <p className="mt-4 text-zinc-600 max-w-xl mx-auto">
            Every project starts with understanding your vision. Here&apos;s how I can bring it to life.
          </p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {services.map((s) => (
            <div
              key={s.title}
              className="p-6 rounded-xl border border-zinc-100 hover:border-amber-200 hover:shadow-md transition-all"
            >
              <span className="text-2xl">{s.icon}</span>
              <h3 className="mt-3 font-semibold text-zinc-900">{s.title}</h3>
              <p className="mt-2 text-sm text-zinc-500">{s.desc}</p>
            </div>
          ))}
        </div>
        <div className="text-center mt-12">
          <Link
            href="/services"
            className="inline-flex h-12 items-center justify-center rounded-full border border-zinc-300 px-8 text-sm font-medium text-zinc-700 hover:border-zinc-400 transition-colors"
          >
            View All Services &amp; Pricing
          </Link>
        </div>
      </div>
    </section>
  );
}
