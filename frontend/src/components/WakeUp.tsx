"use client";
import { useEffect } from "react";

export default function WakeUp() {
  useEffect(() => {
    const api = "https://api-production-8de3.up.railway.app/api/v1";
    const ping = (retries = 3) => {
      fetch(`${api}/health`).catch(() => {
        if (retries > 0) setTimeout(() => ping(retries - 1), 5000);
      });
    };
    ping();
  }, []);
  return null;
}
