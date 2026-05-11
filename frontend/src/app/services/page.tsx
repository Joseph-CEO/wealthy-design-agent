import CTABanner from "@/components/CTABanner";

const serviceDetails = [
  {
    title: "Logo Design",
    desc: "Custom, memorable logos that capture your brand essence. Includes multiple concepts, color variations, vector files, and style guide.",
    price: "From $300",
    features: ["3 initial concepts", "Unlimited revisions", "Vector files (AI, EPS, SVG)", "Color palette", "Logo usage guide"],
  },
  {
    title: "Brand Identity",
    desc: "Complete visual identity systems including logo, color palette, typography, brand guidelines, and application mockups.",
    price: "From $800",
    features: ["Logo + variations", "Color system", "Typography selection", "Brand guidelines PDF", "Business card design", "Social media kit"],
  },
  {
    title: "Advertising & Marketing Design",
    desc: "Promotional design across all channels — print ads, outdoor ads, digital ads, social media campaigns, email marketing templates, and motion ads.",
    price: "From $250",
    features: ["Print ad design", "Digital ad formats", "Social media campaign assets", "Email marketing templates", "Event marketing materials", "Video/motion ad design", "POS displays"],
  },
  {
    title: "Web Design & UI",
    desc: "Visual design of websites and digital interfaces. Portfolio sites, business sites, landing pages, and app interface screens.",
    price: "From $600",
    features: ["Custom website design", "Mobile responsive", "App interface screens", "Landing pages", "CMS integration", "SEO basics"],
  },
  {
    title: "UX Design",
    desc: "User experience design focused on usability, flow, and conversion. Research-backed design that delights users.",
    price: "From $400",
    features: ["Wireframes", "Interactive prototypes", "User journey maps", "Personas", "Usability testing reports", "Information architecture"],
  },
  {
    title: "Publication & Editorial Design",
    desc: "Professional layout and design for long-form print and digital publications. Magazines, books, annual reports, catalogues, and more.",
    price: "From $500",
    features: ["Cover design (front + back + spine)", "Interior layout", "Print-ready PDF", "eBook formatting", "Magazine layout", "Annual report design", "Newsletter templates"],
  },
  {
    title: "Packaging Design",
    desc: "Shelf-ready packaging that tells your brand story. Product labels, boxes, bags, and custom packaging solutions.",
    price: "From $400",
    features: ["Product label design", "Box/packaging structure", "Print-ready artwork", "Mockup renders", "Die-cut template", "Unboxing experience"],
  },
  {
    title: "Environmental & Experiential Design",
    desc: "Graphics integrated into physical spaces. Signage, wayfinding systems, exhibition graphics, office branding, and event stage backdrops.",
    price: "From $350",
    features: ["Signage & wayfinding design", "Exhibition graphics", "Office branding", "Retail graphics", "Event stage backdrops", "Installation-ready files"],
  },
  {
    title: "Information & Data Visualization",
    desc: "Clear visual communication of complex data. Infographics, dashboards, data reports, and educational diagrams.",
    price: "From $250",
    features: ["Infographic design", "Dashboard layouts", "Data report visualization", "Educational diagrams", "Interactive viz concepts"],
  },
  {
    title: "Illustration & Concept Art",
    desc: "Custom artwork for storytelling, branding, or visualization. Editorial illustrations, vector art, poster art, and custom graphics.",
    price: "From $200",
    features: ["Editorial illustrations", "Vector art", "Poster art", "Custom graphics", "Brand mascot design", "Source files included"],
  },
  {
    title: "Environmental Graphics",
    desc: "Large-scale graphics for public or branded spaces. Wall murals, large-format branding, public installations, and branded architectural elements.",
    price: "From $500",
    features: ["Wall mural design", "Large-format branding", "Public installation art", "Branded architectural elements", "Installation specifications"],
  },
  {
    title: "Signboards & Banners",
    desc: "Eye-catching signage for storefronts, events, trade shows, and outdoor advertising. Various sizes and materials.",
    price: "From $200",
    features: ["Custom size specifications", "Multiple format exports", "Print-ready files", "Weather-resistant design", "Illuminated sign options"],
  },
  {
    title: "Flyers & Posters",
    desc: "Attention-grabbing promotional materials for events, products, services, and campaigns. Print and digital formats.",
    price: "From $150",
    features: ["Front/back design", "Print-ready CMYK", "Digital optimized version", "Social media resizing", "Source files included"],
  },
  {
    title: "Menu Design",
    desc: "Well-organized, appetizing menu designs for restaurants, cafes, bars, and food trucks. Easy to update.",
    price: "From $250",
    features: ["Custom layout per page", "Food photography integration", "Print-ready PDF", "Digital menu version", "Easy-edit template"],
  },
];

export default function ServicesPage() {
  return (
    <>
      <section className="py-20 bg-gradient-to-br from-zinc-50 via-white to-amber-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-zinc-900">
              Services &amp; Pricing
            </h1>
            <p className="mt-4 text-zinc-600 max-w-2xl mx-auto">
              Every project is unique. Below are starting prices — final quotes depend on scope,
              complexity, and timeline. All projects include unlimited revisions until you&apos;re
              completely satisfied.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {serviceDetails.map((s) => (
              <div
                key={s.title}
                className="p-8 rounded-xl border border-zinc-200 hover:border-amber-200 transition-all"
              >
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-xl font-bold text-zinc-900">{s.title}</h2>
                  <span className="text-amber-600 font-semibold whitespace-nowrap ml-4">{s.price}</span>
                </div>
                <p className="text-zinc-600 text-sm mb-4">{s.desc}</p>
                <ul className="space-y-2">
                  {s.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm text-zinc-500">
                      <span className="text-amber-500">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
      <CTABanner />
    </>
  );
}
