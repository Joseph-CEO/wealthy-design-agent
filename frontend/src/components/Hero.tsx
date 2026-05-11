import Link from "next/link";

export default function Hero() {
  return (
    <section className="bg-gradient-to-br from-zinc-50 via-white to-amber-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
        <div className="max-w-3xl">
          <p className="text-amber-600 font-medium text-sm tracking-widest uppercase mb-4">
            Nairobi-Based Graphic Designer
          </p>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-zinc-900 leading-tight">
            I create visual identities
            <br />
            that make an impact.
          </h1>
          <p className="mt-6 text-lg text-zinc-600 max-w-xl">
            Logo design, book layouts &amp; covers, branding, packaging, signboards,
            flyers, posters, menus, banners, and websites — crafted for clients worldwide.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href="/contact"
              className="inline-flex h-12 items-center justify-center rounded-full bg-zinc-900 px-8 text-sm font-medium text-white hover:bg-zinc-800 transition-colors"
            >
              Start Your Project
            </Link>
            <Link
              href="/portfolio"
              className="inline-flex h-12 items-center justify-center rounded-full border border-zinc-300 px-8 text-sm font-medium text-zinc-700 hover:border-zinc-400 transition-colors"
            >
              View Portfolio
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
