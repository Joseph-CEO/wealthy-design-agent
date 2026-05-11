import ContactForm from "@/components/ContactForm";

export default function ContactPage() {
  return (
    <section className="py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-zinc-900">
            Start Your Project
          </h1>
          <p className="mt-4 text-zinc-600 max-w-xl mx-auto">
            Tell me about your project and I&apos;ll get back to you within 24 hours
            with a personalized quote and timeline.
          </p>
        </div>
        <ContactForm />
        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 text-center text-sm text-zinc-500">
          <div>
            <div className="font-semibold text-zinc-900 mb-1">Email</div>
            hello@designer.ke
          </div>
          <div>
            <div className="font-semibold text-zinc-900 mb-1">Response Time</div>
            Within 24 hours
          </div>
          <div>
            <div className="font-semibold text-zinc-900 mb-1">Payments</div>
            Visa, Mastercard, M-Pesa, PayPal
          </div>
        </div>
      </div>
    </section>
  );
}
