"use client";
import { useState } from "react";

const testimonials = [
  {
    quote: "Exceptional work on our brand identity. The logo and packaging design exceeded our expectations.",
    author: "Sarah Wanjiku",
    role: "Founder, Organic Foods Kenya",
  },
  {
    quote: "The book cover design was perfect — captured the essence of my novel beautifully.",
    author: "James Ochieng",
    role: "Author",
  },
  {
    quote: "Professional, responsive, and incredibly creative. Our website looks amazing.",
    author: "Grace Mwangi",
    role: "CEO, Mwangi Tech Solutions",
  },
];

export default function Testimonials() {
  const [index, setIndex] = useState(0);
  const t = testimonials[index];

  return (
    <section className="py-20 bg-zinc-50">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-900 mb-12">
          What Clients Say
        </h2>
        <blockquote className="text-xl text-zinc-700 italic leading-relaxed">
          &ldquo;{t.quote}&rdquo;
        </blockquote>
        <div className="mt-6">
          <p className="font-semibold text-zinc-900">{t.author}</p>
          <p className="text-sm text-zinc-500">{t.role}</p>
        </div>
        <div className="mt-8 flex justify-center gap-3">
          {testimonials.map((_, i) => (
            <button
              key={i}
              onClick={() => setIndex(i)}
              className={`w-2.5 h-2.5 rounded-full transition-colors ${
                i === index ? "bg-zinc-900" : "bg-zinc-300"
              }`}
              aria-label={`Testimonial ${i + 1}`}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
