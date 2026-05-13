import type { PortfolioItem } from "@/lib/api";

const placeholderImages: Record<string, string> = {
  logo_design: "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=600&h=400&fit=crop",
  branding: "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=600&h=400&fit=crop",
  advertising_marketing: "https://images.unsplash.com/photo-1557838923-2985c318be48?w=600&h=400&fit=crop",
  web_ui: "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=600&h=400&fit=crop",
  website: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop",
  ux_design: "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?w=600&h=400&fit=crop",
  publication_editorial: "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&h=400&fit=crop",
  book_cover: "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&h=400&fit=crop",
  book_layout: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop",
  packaging_design: "https://images.unsplash.com/photo-1544457070-4cd773b4d71e?w=600&h=400&fit=crop",
  environmental_experiential: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&h=400&fit=crop",
  signboard: "https://images.unsplash.com/photo-1576827232943-0fd8ebf1e782?w=600&h=400&fit=crop",
  information_data_viz: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop",
  illustration_concept_art: "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=600&h=400&fit=crop",
  environmental_graphics: "https://images.unsplash.com/photo-1559827291-baf8a0f80a5f?w=600&h=400&fit=crop",
  flyer: "https://images.unsplash.com/photo-1563986768609-322da13575f2?w=600&h=400&fit=crop",
  poster: "https://images.unsplash.com/photo-1580136579312-94651dfd596d?w=600&h=400&fit=crop",
  menu: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
  banner: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&h=400&fit=crop",
};

export function placeholder(category: string) {
  return placeholderImages[category] || "https://placehold.co/600x400/cccccc/333333?text=Design";
}

interface Props {
  items?: PortfolioItem[];
}

export default function PortfolioGrid({ items }: Props) {
  const display = items && items.length > 0 ? items : [];

  if (display.length === 0) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(placeholderImages).slice(0, 6).map(([cat, url]) => (
          <div key={cat} className="group relative overflow-hidden rounded-xl border border-zinc-200">
            <img
              src={url}
              alt={cat.replace("_", " ")}
              className="w-full h-64 object-cover transition-transform group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors flex items-center justify-center">
              <span className="text-white font-medium opacity-0 group-hover:opacity-100 transition-opacity capitalize">
                {cat.replace("_", " ")}
              </span>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {display.map((item) => (
        <div key={item.id} className="group relative overflow-hidden rounded-xl border border-zinc-200">
          <img
            src={item.image_urls?.[0] || placeholder(item.category)}
            alt={item.title}
            className="w-full h-64 object-cover transition-transform group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/60 transition-colors flex flex-col items-center justify-center p-4">
            <span className="text-white font-medium opacity-0 group-hover:opacity-100 transition-opacity text-center">
              {item.title}
            </span>
            <span className="text-zinc-300 text-xs opacity-0 group-hover:opacity-100 transition-opacity mt-1 capitalize">
              {item.category.replace("_", " ")}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
