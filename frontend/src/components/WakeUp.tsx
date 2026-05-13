"use client";
import { useEffect } from "react";

export default function WakeUp() {
  useEffect(() => {
    const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    fetch(`${api}/health`, { method: "GET" }).catch(() => {});
  }, []);
  return null;
}
