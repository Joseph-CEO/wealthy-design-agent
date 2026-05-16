const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface Lead {
  id: number;
  source: string;
  title: string;
  description: string | null;
  client_name: string | null;
  client_email: string | null;
  budget_min: number | null;
  budget_max: number | null;
  currency: string | null;
  location: string | null;
  service_type: string | null;
  score: number;
  status: string;
  created_at: string | null;
  updated_at: string | null;
}

export interface PortfolioItem {
  id: number;
  title: string;
  description: string | null;
  category: string;
  image_urls: string[];
  project_url: string | null;
  tags: string[];
  featured: boolean;
  created_at: string | null;
}

export interface Project {
  id: number;
  lead_id: number | null;
  title: string;
  description: string | null;
  status: string;
  quote_amount: number | null;
  currency: string;
  client_email: string | null;
  started_at: string | null;
  deadline: string | null;
  delivered_at: string | null;
}

export interface Payment {
  id: number;
  project_id: number;
  amount: number;
  currency: string;
  gateway: string;
  gateway_payment_id: string | null;
  status: string;
  client_email: string | null;
  receipt_url: string | null;
  paid_at: string | null;
}

export interface ScanLog {
  id: number;
  scan_type: string;
  status: string;
  leads_found: number;
  message: string | null;
  started_at: string | null;
  completed_at: string | null;
}

export interface AdminStats {
  leads: { total: number; new: number; qualified: number; converted: number };
  projects: { total: number; active: number; delivered: number };
  revenue: { total: number };
  portfolio_count: number;
  recent_scans: ScanLog[];
}

export interface LeadsResponse {
  total: number;
  limit: number;
  offset: number;
  leads: Lead[];
}

export interface PortfolioResponse {
  total: number;
  limit: number;
  offset: number;
  items: PortfolioItem[];
}

export interface ScanLogsResponse {
  total: number;
  limit: number;
  offset: number;
  logs: ScanLog[];
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API ${res.status}: ${body || res.statusText}`);
  }
  return res.json();
}

export interface SEOPage {
  id: number;
  slug: string;
  service_type: string;
  county: string;
  industry: string | null;
  title: string;
  meta_description: string;
  h1: string;
  body_html: string | null;
  portfolio_examples: string[];
  pricing_html: string | null;
  cta_text: string | null;
  score: number;
  published: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface SEOPagesResponse {
  total: number;
  limit: number;
  offset: number;
  pages: SEOPage[];
}

export interface SEOServicesResponse {
  services: { type: string; page_count: number }[];
}

export interface SEOCountiesResponse {
  counties: { name: string; page_count: number }[];
}

export const api = {
  // Health
  health: () => request<{ status: string }>("/health"),

  // Leads
  getLeads: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return request<LeadsResponse>(`/leads${qs}`);
  },
  getLead: (id: number) => request<Lead>(`/leads/${id}`),
  deleteLead: (id: number) => request<{ status: string; id: number }>(`/leads/${id}`, { method: "DELETE" }),
  qualifyLead: (id: number) =>
    request<{ id: number; score: number; status: string }>(`/leads/${id}/qualify`, { method: "POST" }),
  contactLead: (id: number) =>
    request<{ status: string; id: number; email?: object }>(`/leads/${id}/contact`, { method: "POST" }),
  triggerScan: () => request<{ status: string; summary: object }>("/leads/scan", { method: "POST" }),
  qualifyAll: () => request<{ qualified: number; results: object[] }>("/leads/qualify-all", { method: "POST" }),
  outreachQualified: () => request<{ total: number; results: object[] }>("/leads/outreach-qualified", { method: "POST" }),
  outreachFollowup: () => request<{ total: number; results: object[] }>("/leads/outreach-followup", { method: "POST" }),

  // Portfolio
  getPortfolio: (category?: string) => {
    const qs = category ? `?category=${category}` : "";
    return request<PortfolioResponse>(`/portfolio${qs}`);
  },
  createPortfolioItem: (data: Partial<PortfolioItem>) =>
    request<PortfolioItem>("/portfolio", { method: "POST", body: JSON.stringify(data) }),
  updatePortfolioItem: (id: number, data: Partial<PortfolioItem>) =>
    request<PortfolioItem>(`/portfolio/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deletePortfolioItem: (id: number) =>
    request<{ status: string; id: number }>(`/portfolio/${id}`, { method: "DELETE" }),

  // Projects
  getProjects: () => request<Project[]>("/projects"),
  getProject: (id: number) => request<Project>(`/projects/${id}`),
  createProject: (data: Partial<Project>) =>
    request<Project>("/projects", { method: "POST", body: JSON.stringify(data) }),
  updateProject: (id: number, data: Partial<Project>) =>
    request<Project>(`/projects/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  // Payments
  createPesapalOrder: (data: { project_id: number; client_first_name?: string; client_last_name?: string; client_phone?: string }) =>
    request<{ order_tracking_id: string; redirect_url: string }>("/payments/create-pesapal-order", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  mpesaStkPush: (data: { project_id: number; phone_number: string; amount?: number }) =>
    request<{ merchant_request_id?: string; checkout_request_id?: string; response_code?: string }>(
      "/payments/mpesa-stk-push",
      { method: "POST", body: JSON.stringify(data) },
    ),

  // Chat
  sendMessage: (message: string, sessionId?: string) =>
    request<{ response: string; session_id: string }>("/chat", {
      method: "POST",
      body: JSON.stringify({ message, session_id: sessionId }),
    }),

  // Contact
  submitContact: (data: { name: string; email: string; service_type: string; budget: string; description: string }) =>
    request<{ status: string; message: string }>("/contact", { method: "POST", body: JSON.stringify(data) }),

  // SEO
  getSEOPages: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return request<SEOPagesResponse>(`/seo/pages${qs}`);
  },
  getSEOPage: (slug: string) => request<SEOPage>(`/seo/pages/${slug}`),
  getSEOServices: () => request<SEOServicesResponse>("/seo/services"),
  getSEOCounties: () => request<SEOCountiesResponse>("/seo/counties"),
  generateSEOPages: () =>
    request<{ status: string; total_combinations: number; created: number; batch_size: number }>(
      "/admin/generate-seo-pages", { method: "POST" }
    ),

  // Admin
  getAdminStats: (token?: string) => {
    const headers: Record<string, string> = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;
    return request<AdminStats>("/admin/stats", { headers });
  },
  getScanLogs: (limit = 50, offset = 0) =>
    request<ScanLogsResponse>(`/admin/scan-logs?limit=${limit}&offset=${offset}`),
};
