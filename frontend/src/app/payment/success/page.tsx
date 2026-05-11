"use client";

import Link from "next/link";

export default function PaymentSuccess() {
  return (
    <section className="py-20 text-center">
      <div className="max-w-md mx-auto px-4">
        <div className="text-5xl mb-4">✓</div>
        <h1 className="text-3xl font-bold text-zinc-900 mb-2">Payment Successful!</h1>
        <p className="text-zinc-500 mb-8">
          Thank you for your payment. The designer will begin work on your project shortly.
        </p>
        <Link
          href="/"
          className="inline-block h-12 px-8 rounded-full bg-zinc-900 text-white font-medium leading-12 hover:bg-zinc-800"
        >
          Back to Home
        </Link>
      </div>
    </section>
  );
}
