"use client";
import Link from "next/link";
import { useState } from "react";

const links = [
  { href: "/", label: "Home" },
  { href: "/services", label: "Services" },
  { href: "/portfolio", label: "Portfolio" },
  { href: "/seo", label: "Locations" },
  { href: "/chat", label: "Chat" },
  { href: "/payment", label: "Pay" },
  { href: "/contact", label: "Get a Quote" },
];

const adminLink = { href: "/admin", label: "Admin" };

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-zinc-100">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link href="/" className="flex flex-col">
            <span className="text-xl font-bold tracking-tight text-zinc-900">
              Wealthbox<span className="text-amber-500">.</span>
            </span>
            <span className="text-[10px] text-zinc-400 tracking-wider -mt-1">
              by Seven Integrated
            </span>
          </Link>
          <div className="hidden sm:flex gap-8">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors"
              >
                {l.label}
              </Link>
            ))}
            <Link
              href={adminLink.href}
              className="text-sm font-medium text-zinc-400 hover:text-zinc-900 transition-colors"
            >
              {adminLink.label}
            </Link>
          </div>
          <button
            className="sm:hidden p-2"
            onClick={() => setOpen(!open)}
            aria-label="Menu"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {open ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
        {open && (
          <div className="sm:hidden pb-4 space-y-2">
            {[...links, adminLink].map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className="block py-2 text-sm font-medium text-zinc-600 hover:text-zinc-900"
                onClick={() => setOpen(false)}
              >
                {l.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
