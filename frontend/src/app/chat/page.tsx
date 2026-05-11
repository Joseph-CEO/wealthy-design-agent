"use client";

import type { FormEvent } from "react";
import { useState, useRef, useEffect, useCallback } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function getSessionId(): string {
  let sid = sessionStorage.getItem("chat_session_id");
  if (!sid) {
    sid = crypto.randomUUID();
    sessionStorage.setItem("chat_session_id", sid);
  }
  return sid;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const scroll = useCallback(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(scroll, [messages, scroll]);

  async function handleSend(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, session_id: getSessionId() }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't reach the server. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-12 sm:py-20">
      <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-900 mb-2">
        Chat with the Designer
      </h1>
      <p className="text-zinc-600 mb-8">
        Ask about services, pricing, portfolio, or start a new project.
      </p>

      <div className="bg-white border border-zinc-200 rounded-2xl flex flex-col h-[60vh] min-h-[400px]">
        <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-zinc-400 mt-12 space-y-2">
              <p>Hi there! I'm the designer's virtual assistant.</p>
              <p>Ask me anything about our services and pricing.</p>
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm sm:text-base ${
                  m.role === "user"
                    ? "bg-amber-500 text-white"
                    : "bg-zinc-100 text-zinc-800"
                }`}
              >
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-zinc-100 rounded-2xl px-4 py-3 text-zinc-400">Typing...</div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <form onSubmit={handleSend} className="border-t border-zinc-200 px-4 sm:px-6 py-4 flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border border-zinc-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-amber-500 text-white rounded-xl px-6 py-3 text-sm font-medium hover:bg-amber-600 disabled:opacity-50 transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
