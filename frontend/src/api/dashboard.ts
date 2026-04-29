import type { Dashboard, Location } from "../types/dashboard";

export async function fetchLocations(): Promise<Location[]> {
  const res = await fetch("/api/locations");
  if (!res.ok) throw new Error(`Locations HTTP ${res.status}`);
  return res.json();
}

export async function fetchDashboard(locationKey: string): Promise<Dashboard> {
  const res = await fetch(`/api/dashboard?location_key=${locationKey}`);
  if (!res.ok) throw new Error(`Dashboard HTTP ${res.status}`);
  return res.json();
}