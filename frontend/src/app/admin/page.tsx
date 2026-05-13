"use client";

import type { FormEvent } from "react";
import { useState, useEffect, useCallback } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface AdminStats {
  leads: { total: number; new: number; qualified: number; converted: number };
  projects: { total: number; active: number; delivered: number };
  revenue: { total: number };
  portfolio_count: number;
  recent_scans: { id: number; scan_type: string; status: string; leads_found: number; message: string | null; started_at: string | null; completed_at: string | null }[];
}

interface PortfolioItem {
  id: number; title: string; description: string | null; category: string;
  image_urls: string[]; project_url: string | null; tags: string[]; featured: boolean;
}

interface Project {
  id: number; lead_id: number | null; title: string; description: string | null;
  status: string; quote_amount: number | null; currency: string; client_email: string | null;
}

interface Lead {
  id: number; source: string; title: string; client_name: string | null;
  client_email: string | null; score: number; status: string;
}

type Tab = "dashboard" | "portfolio" | "projects" | "leads" | "scans";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const token = sessionStorage.getItem("admin_token");
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers: { ...headers, ...options?.headers } });
  if (res.status === 401 || res.status === 403) throw new Error("auth_required");
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [portfolio, setPortfolio] = useState<PortfolioItem[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [scans, setScans] = useState<any[]>([]);
  const [authToken, setAuthToken] = useState("");
  const [showAuth, setShowAuth] = useState(false);
  const [authError, setAuthError] = useState("");
  const [loading, setLoading] = useState(false);
  const [editingPortfolio, setEditingPortfolio] = useState<Partial<PortfolioItem> | null>(null);
  const [editingProject, setEditingProject] = useState<Partial<Project> | null>(null);

  const checkAuth = useCallback(() => {
    const t = sessionStorage.getItem("admin_token");
    if (t) setAuthToken(t);
  }, []);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [s, p, pr, l] = await Promise.all([
        apiFetch<AdminStats>("/admin/stats").catch(() => { setShowAuth(true); setAuthError("Backend is waking up — try again in a moment."); return null; }),
        apiFetch<{ items: PortfolioItem[] }>("/portfolio?limit=200").then(r => r.items).catch(() => []),
        apiFetch<Project[]>("/projects").catch(() => []),
        apiFetch<{ leads: Lead[] }>("/leads?limit=200").then(r => r.leads).catch(() => []),
      ]);
      if (s) { setStats(s); setShowAuth(false); }
      setPortfolio(p);
      setProjects(pr);
      setLeads(l);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { checkAuth(); loadData(); }, [checkAuth, loadData]);

  useEffect(() => {
    if (tab === "scans") {
      apiFetch<{ logs: any[] }>("/admin/scan-logs?limit=100")
        .then(r => setScans(r.logs))
        .catch(() => {});
    }
  }, [tab]);

  async function handleAuth(e: FormEvent) {
    e.preventDefault();
    setAuthError("");
    sessionStorage.setItem("admin_token", authToken);
    setShowAuth(false);
    await loadData();
  }

  async function triggerSEOGeneration() {
    if (!confirm("Generate new SEO pages? This may create many pages.")) return;
    await apiFetch("/admin/generate-seo-pages", { method: "POST" });
    await loadData();
  }

  async function deletePortfolio(id: number) {
    if (!confirm("Delete this portfolio item?")) return;
    await apiFetch(`/portfolio/${id}`, { method: "DELETE" });
    await loadData();
  }

  async function savePortfolio(e: FormEvent) {
    e.preventDefault();
    if (!editingPortfolio) return;
    if (editingPortfolio.id) {
      await apiFetch(`/portfolio/${editingPortfolio.id}`, {
        method: "PUT", body: JSON.stringify(editingPortfolio),
      });
    } else {
      await apiFetch("/portfolio", {
        method: "POST", body: JSON.stringify(editingPortfolio),
      });
    }
    setEditingPortfolio(null);
    await loadData();
  }

  async function updateProjectStatus(id: number, status: string) {
    await apiFetch(`/projects/${id}`, { method: "PUT", body: JSON.stringify({ status }) });
    await loadData();
  }

  const StatCard = ({ label, value }: { label: string; value: string | number }) => (
    <div className="bg-white border border-zinc-200 rounded-xl p-5">
      <div className="text-2xl font-bold text-zinc-900">{value}</div>
      <div className="text-sm text-zinc-500 mt-1">{label}</div>
    </div>
  );

  if (showAuth) {
    return (
      <div className="max-w-sm mx-auto px-4 py-32">
        <h1 className="text-2xl font-bold text-zinc-900 mb-6">Admin Login</h1>
        <form onSubmit={handleAuth} className="space-y-4">
          <input
            value={authToken} onChange={(e) => setAuthToken(e.target.value)}
            placeholder="Admin Token" required
            className="w-full px-4 py-2.5 rounded-lg border border-zinc-300 focus:border-amber-500 outline-none"
          />
          <button type="submit" className="w-full h-12 rounded-full bg-zinc-900 text-white font-medium hover:bg-zinc-800">
            Login
          </button>
          {authError && <p className="text-red-500 text-sm text-center">{authError}</p>}
        </form>
      </div>
    );
  }

  const tabs: { key: Tab; label: string }[] = [
    { key: "dashboard", label: "Dashboard" },
    { key: "portfolio", label: "Portfolio" },
    { key: "projects", label: "Projects" },
    { key: "leads", label: "Leads" },
    { key: "scans", label: "Scan Logs" },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-zinc-900">Admin</h1>
        <button
          onClick={() => { sessionStorage.removeItem("admin_token"); setAuthToken(""); setShowAuth(true); }}
          className="text-sm text-zinc-500 hover:text-zinc-700 underline"
        >
          Logout
        </button>
      </div>

      <div className="flex gap-2 mb-8 flex-wrap">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              tab === t.key ? "bg-zinc-900 text-white" : "bg-zinc-100 text-zinc-600 hover:bg-zinc-200"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading && <p className="text-zinc-400 text-center py-12">Loading...</p>}

      {!loading && tab === "dashboard" && stats && (
        <div className="space-y-8">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <StatCard label="Total Leads" value={stats.leads.total} />
            <StatCard label="Qualified" value={stats.leads.qualified} />
            <StatCard label="Active Projects" value={stats.projects.active} />
            <StatCard label="Revenue" value={`$${stats.revenue.total}`} />
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <StatCard label="New Leads" value={stats.leads.new} />
            <StatCard label="Converted" value={stats.leads.converted} />
            <StatCard label="Delivered" value={stats.projects.delivered} />
            <StatCard label="Portfolio Items" value={stats.portfolio_count} />
          </div>
          {stats.recent_scans.length > 0 && (
            <div>
              <h2 className="text-lg font-semibold text-zinc-900 mb-3">Recent Scans</h2>
              <div className="space-y-2">
                {stats.recent_scans.map((s) => (
                  <div key={s.id} className="flex items-center justify-between bg-zinc-50 rounded-lg px-4 py-2 text-sm">
                    <span className="text-zinc-600">{s.scan_type}</span>
                    <span className={`font-medium ${s.status === "completed" ? "text-green-600" : s.status === "failed" ? "text-red-600" : "text-amber-600"}`}>
                      {s.status} ({s.leads_found} leads)
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {!loading && tab === "portfolio" && (
        <div>
          <button
            onClick={() => setEditingPortfolio({ title: "", category: "logo_design", image_urls: [], tags: [], featured: false })}
            className="mb-4 px-4 py-2 rounded-full bg-amber-500 text-white text-sm font-medium hover:bg-amber-600"
          >
            + New Item
          </button>
          {editingPortfolio && (
            <form onSubmit={savePortfolio} className="bg-zinc-50 rounded-xl p-6 mb-6 space-y-4 max-w-lg">
              <h3 className="font-semibold text-zinc-900">{editingPortfolio.id ? "Edit" : "New"} Portfolio Item</h3>
              <input placeholder="Title" required value={editingPortfolio.title || ""}
                onChange={(e) => setEditingPortfolio({ ...editingPortfolio, title: e.target.value })}
                className="w-full px-3 py-2 rounded-lg border border-zinc-300 text-sm outline-none" />
              <input placeholder="Description" value={editingPortfolio.description || ""}
                onChange={(e) => setEditingPortfolio({ ...editingPortfolio, description: e.target.value })}
                className="w-full px-3 py-2 rounded-lg border border-zinc-300 text-sm outline-none" />
              <select value={editingPortfolio.category || "logo_design"}
                onChange={(e) => setEditingPortfolio({ ...editingPortfolio, category: e.target.value })}
                className="w-full px-3 py-2 rounded-lg border border-zinc-300 text-sm outline-none bg-white">
                {["logo_design","branding","advertising_marketing","web_ui","website","ux_design","publication_editorial","book_layout","book_cover","packaging_design","environmental_experiential","signboard","information_data_viz","illustration_concept_art","environmental_graphics","flyer","poster","menu","banner"].map(c => (
                  <option key={c} value={c}>{c.replace("_", " ")}</option>
                ))}
              </select>
              <input placeholder="Image URLs (comma separated)" value={(editingPortfolio.image_urls || []).join(", ")}
                onChange={(e) => setEditingPortfolio({ ...editingPortfolio, image_urls: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                className="w-full px-3 py-2 rounded-lg border border-zinc-300 text-sm outline-none" />
              <input placeholder="Tags (comma separated)" value={(editingPortfolio.tags || []).join(", ")}
                onChange={(e) => setEditingPortfolio({ ...editingPortfolio, tags: e.target.value.split(",").map(s => s.trim()).filter(Boolean) })}
                className="w-full px-3 py-2 rounded-lg border border-zinc-300 text-sm outline-none" />
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" checked={editingPortfolio.featured || false}
                  onChange={(e) => setEditingPortfolio({ ...editingPortfolio, featured: e.target.checked })} />
                Featured
              </label>
              <div className="flex gap-2">
                <button type="submit" className="px-4 py-2 rounded-full bg-zinc-900 text-white text-sm font-medium hover:bg-zinc-800">
                  Save
                </button>
                <button type="button" onClick={() => setEditingPortfolio(null)} className="px-4 py-2 rounded-full bg-zinc-200 text-zinc-700 text-sm">
                  Cancel
                </button>
              </div>
            </form>
          )}
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-zinc-200 text-left text-zinc-500">
                  <th className="pb-3 pr-4">Title</th>
                  <th className="pb-3 pr-4">Category</th>
                  <th className="pb-3 pr-4">Featured</th>
                  <th className="pb-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.map((item) => (
                  <tr key={item.id} className="border-b border-zinc-100">
                    <td className="py-3 pr-4 font-medium text-zinc-900">{item.title}</td>
                    <td className="py-3 pr-4 text-zinc-500 capitalize">{item.category.replace("_", " ")}</td>
                    <td className="py-3 pr-4">{item.featured ? "Yes" : "No"}</td>
                    <td className="py-3 flex gap-2">
                      <button onClick={() => setEditingPortfolio(item)} className="text-amber-600 hover:text-amber-700 text-xs underline">Edit</button>
                      <button onClick={() => deletePortfolio(item.id)} className="text-red-500 hover:text-red-600 text-xs underline">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {!loading && tab === "projects" && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 text-left text-zinc-500">
                <th className="pb-3 pr-4">Title</th>
                <th className="pb-3 pr-4">Status</th>
                <th className="pb-3 pr-4">Quote</th>
                <th className="pb-3 pr-4">Client</th>
                <th className="pb-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p) => (
                <tr key={p.id} className="border-b border-zinc-100">
                  <td className="py-3 pr-4 font-medium text-zinc-900">{p.title}</td>
                  <td className="py-3 pr-4">
                    <select value={p.status}
                      onChange={(e) => updateProjectStatus(p.id, e.target.value)}
                      className="text-xs border border-zinc-300 rounded px-2 py-1 outline-none">
                      {["brief","negotiation","in_progress","review","delivered","paid","cancelled"].map(s => (
                        <option key={s} value={s}>{s.replace("_", " ")}</option>
                      ))}
                    </select>
                  </td>
                  <td className="py-3 pr-4 text-zinc-600">{p.quote_amount ? `${p.currency} ${p.quote_amount}` : "-"}</td>
                  <td className="py-3 pr-4 text-zinc-500">{p.client_email || "-"}</td>
                  <td className="py-3">
                    <button onClick={() => setEditingProject(p)} className="text-amber-600 hover:text-amber-700 text-xs underline">Edit</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && tab === "leads" && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 text-left text-zinc-500">
                <th className="pb-3 pr-4">Title</th>
                <th className="pb-3 pr-4">Source</th>
                <th className="pb-3 pr-4">Score</th>
                <th className="pb-3 pr-4">Status</th>
                <th className="pb-3">Client</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((l) => (
                <tr key={l.id} className="border-b border-zinc-100">
                  <td className="py-3 pr-4 font-medium text-zinc-900 max-w-xs truncate">{l.title}</td>
                  <td className="py-3 pr-4 text-zinc-500">{l.source}</td>
                  <td className="py-3 pr-4">
                    <span className={`font-medium ${l.score >= 70 ? "text-green-600" : l.score >= 40 ? "text-amber-600" : "text-zinc-400"}`}>
                      {l.score}
                    </span>
                  </td>
                  <td className="py-3 pr-4"><span className="capitalize">{l.status}</span></td>
                  <td className="py-3 text-zinc-500">{l.client_name || l.client_email || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && tab === "scans" && (
        <div>
          <button
            onClick={triggerSEOGeneration}
            className="mb-4 px-4 py-2 rounded-full bg-amber-500 text-white text-sm font-medium hover:bg-amber-600"
          >
            Generate SEO Pages
          </button>
          <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-200 text-left text-zinc-500">
                <th className="pb-3 pr-4">Type</th>
                <th className="pb-3 pr-4">Status</th>
                <th className="pb-3 pr-4">Leads Found</th>
                <th className="pb-3 pr-4">Message</th>
                <th className="pb-3">Started</th>
              </tr>
            </thead>
            <tbody>
              {scans.map((s) => (
                <tr key={s.id} className="border-b border-zinc-100">
                  <td className="py-3 pr-4 font-medium text-zinc-900">{s.scan_type}</td>
                  <td className="py-3 pr-4">
                    <span className={`font-medium ${s.status === "completed" ? "text-green-600" : s.status === "failed" ? "text-red-600" : "text-amber-600"}`}>
                      {s.status}
                    </span>
                  </td>
                  <td className="py-3 pr-4 text-zinc-600">{s.leads_found}</td>
                  <td className="py-3 pr-4 text-zinc-500 max-w-xs truncate">{s.message || "-"}</td>
                  <td className="py-3 text-zinc-400 text-xs">{s.started_at ? new Date(s.started_at).toLocaleString() : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        </div>
      )}
    </div>
  );
}
