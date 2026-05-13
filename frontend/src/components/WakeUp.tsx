"use client";
import { useEffect } from "react";

export default function WakeUp() {
  useEffect(() => {
    const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    const ping = (retries = 3) => {
      fetch(`${api}/health`).catch(() => {
        if (retries > 0) setTimeout(() => ping(retries - 1), 5000);
      });
    };
    ping();
  }, []);
  return null;
}
