export default function Footer() {
  return (
    <footer className="bg-zinc-900 text-zinc-400 mt-auto">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
          <div>
            <h3 className="text-white font-semibold mb-3">Designer.</h3>
            <p className="text-sm">
              Nairobi-based graphic designer specializing in logos, branding, book design,
              packaging, and web design. Available worldwide.
            </p>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-3">Services</h3>
            <ul className="text-sm space-y-1">
              <li>Logo Design</li>
              <li>Brand Identity</li>
              <li>Advertising &amp; Marketing</li>
              <li>Web Design &amp; UI</li>
              <li>UX Design</li>
              <li>Publication &amp; Editorial</li>
              <li>Packaging Design</li>
              <li>Environmental &amp; Experiential</li>
              <li>Data Visualization</li>
              <li>Illustration &amp; Concept Art</li>
            </ul>
          </div>
          <div>
            <h3 className="text-white font-semibold mb-3">Contact</h3>
            <ul className="text-sm space-y-1">
              <li>Nairobi, Kenya</li>
              <li>hello@designer.ke</li>
              <li>+254 700 000 000</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-zinc-800 mt-8 pt-8 text-center text-xs">
          &copy; {new Date().getFullYear()} Designer. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
