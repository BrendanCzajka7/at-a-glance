import type { NaturePhoto } from "../types/dashboard";

export async function fetchNatureThemes(): Promise<string[]> {
  const res = await fetch("/api/nature/themes");

  if (!res.ok) {
    throw new Error(`Nature themes HTTP ${res.status}`);
  }

  return res.json();
}

export async function ingestNaturePhoto(
  theme: string
): Promise<NaturePhoto | null> {
  const params = new URLSearchParams({ theme });

  const res = await fetch(`/api/nature/ingest-photo?${params}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error(`Nature photo ingest HTTP ${res.status}`);
  }

  return res.json();
}