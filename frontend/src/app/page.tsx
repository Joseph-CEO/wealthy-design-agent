import Hero from "@/components/Hero";
import ServicesGrid from "@/components/ServicesGrid";
import Testimonials from "@/components/Testimonials";
import CTABanner from "@/components/CTABanner";
import PortfolioGrid from "@/components/PortfolioGrid";

export default function Home() {
  return (
    <>
      <Hero />
      <ServicesGrid />
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-900">
              Recent Work
            </h2>
            <p className="mt-4 text-zinc-600">
              A selection of projects I&apos;ve delivered for clients worldwide.
            </p>
          </div>
          <PortfolioGrid />
        </div>
      </section>
      <Testimonials />
      <CTABanner />
    </>
  );
}
