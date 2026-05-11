"use client";

import Link from "next/link";

export default function PaymentCancel() {
  return (
    <section className="py-20 text-center">
      <div className="max-w-md mx-auto px-4">
        <div className="text-5xl mb-4">✕</div>
        <h1 className="text-3xl font-bold text-zinc-900 mb-2">Payment Cancelled</h1>
        <p className="text-zinc-500 mb-8">
          Your payment was not completed. You can try again whenever you&apos;re ready.
        </p>
        <Link
          href="/payment"
          className="inline-block h-12 px-8 rounded-full bg-zinc-900 text-white font-medium leading-12 hover:bg-zinc-800"
        >
          Try Again
        </Link>
      </div>
    </section>
  );
}
