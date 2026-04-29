// frontend/src/api/appEvents.ts

export type AppEvent = {
  id: number;
  level: string;
  source: string;
  event_type: string;
  message: string;
  details: string | null;
  created_at: string;
};

export async function fetchRecentAppEvents(limit = 25): Promise<AppEvent[]> {
  const params = new URLSearchParams({ limit: String(limit) });

  const res = await fetch(`/api/app-events?${params}`);

  if (!res.ok) {
    throw new Error(`App events HTTP ${res.status}`);
  }

  return res.json();
}