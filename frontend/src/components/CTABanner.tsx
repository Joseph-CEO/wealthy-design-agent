import Link from "next/link";

export default function CTABanner() {
  return (
    <section className="py-20 bg-zinc-900">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-white">
          Ready to bring your vision to life?
        </h2>
        <p className="mt-4 text-zinc-400 text-lg">
          Let&apos;s discuss your project. Free consultation, no obligation.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          <Link
            href="/contact"
            className="inline-flex h-12 items-center justify-center rounded-full bg-white px-8 text-sm font-medium text-zinc-900 hover:bg-zinc-100 transition-colors"
          >
            Get a Free Quote
          </Link>
          <Link
            href="/portfolio"
            className="inline-flex h-12 items-center justify-center rounded-full border border-zinc-600 px-8 text-sm font-medium text-zinc-300 hover:border-zinc-500 transition-colors"
          >
            View Portfolio
          </Link>
        </div>
      </div>
    </section>
  );
}
