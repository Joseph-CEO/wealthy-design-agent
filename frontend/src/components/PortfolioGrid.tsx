import type { PortfolioItem } from "@/lib/api";

const placeholderImages: Record<string, string> = {
  logo_design: "https://placehold.co/600x400/1a1a1a/ffffff?text=Logo+Design",
  branding: "https://placehold.co/600x400/2d2d2d/ffffff?text=Brand+Identity",
  advertising_marketing: "https://placehold.co/600x400/3d3d3d/ffffff?text=Advertising",
  web_ui: "https://placehold.co/600x400/4d4d4d/ffffff?text=Web+Design+UI",
  website: "https://placehold.co/600x400/bdbdbd/ffffff?text=Website",
  ux_design: "https://placehold.co/600x400/5d5d5d/ffffff?text=UX+Design",
  publication_editorial: "https://placehold.co/600x400/6d6d6d/ffffff?text=Publication",
  book_cover: "https://placehold.co/600x400/3d3d3d/ffffff?text=Book+Cover",
  book_layout: "https://placehold.co/600x400/4d4d4d/ffffff?text=Book+Layout",
  packaging_design: "https://placehold.co/600x400/5d5d5d/ffffff?text=Packaging",
  environmental_experiential: "https://placehold.co/600x400/7d7d7d/ffffff?text=Experiential",
  signboard: "https://placehold.co/600x400/6d6d6d/ffffff?text=Signboard",
  information_data_viz: "https://placehold.co/600x400/8d8d8d/ffffff?text=Data+Viz",
  illustration_concept_art: "https://placehold.co/600x400/9d9d9d/ffffff?text=Illustration",
  environmental_graphics: "https://placehold.co/600x400/adadad/ffffff?text=Environmental",
  flyer: "https://placehold.co/600x400/7d7d7d/ffffff?text=Flyer",
  poster: "https://placehold.co/600x400/8d8d8d/ffffff?text=Poster",
  menu: "https://placehold.co/600x400/9d9d9d/ffffff?text=Menu",
  banner: "https://placehold.co/600x400/adadad/ffffff?text=Banner",
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
