import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ChatBot from "@/components/ChatBot";

export const metadata: Metadata = {
  title: "Designer — Graphic Design Portfolio | Nairobi",
  description:
    "Nairobi-based graphic designer specializing in logo design, book layouts & covers, branding, packaging, signboards, flyers, posters, menus, banners, and websites. Available for projects worldwide.",
  keywords: [
    "graphic designer", "Nairobi", "logo design", "branding",
    "book cover design", "packaging design", "website design",
    "Kenyan designer", "freelance graphic designer",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-white text-zinc-900 font-sans">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
        <ChatBot />
      </body>
    </html>
  );
}
