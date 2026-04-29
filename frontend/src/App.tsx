import { useEffect, useState } from "react";

import { fetchDashboard, fetchLocations } from "./api/dashboard";
import { AppToolbar } from "./components/AppToolbar";
import { LocationSelect } from "./components/LocationSelect";
import { ViewTabs } from "./components/ViewTabs";
import type { Dashboard, Location } from "./types/dashboard";
import { formatTime } from "./features/weather/weatherFormat";
import { getDashboardView, type DashboardView } from "./views/viewRegistry";

export default function App() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocationKey, setSelectedLocationKey] =
    useState("okaloosa_island");
  const [view, setView] = useState<DashboardView>("today");
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");

  const ActiveView = getDashboardView(view).Component;

  useEffect(() => {
    fetchLocations()
      .then(setLocations)
      .catch((err) => setError(err.message));
  }, []);

  async function loadDashboard() {
    try {
      setError("");
      setDashboard(await fetchDashboard(selectedLocationKey));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    }
  }

  useEffect(() => {
    loadDashboard();
    const id = setInterval(loadDashboard, 60_000);

    return () => clearInterval(id);
  }, [selectedLocationKey]);

  return (
    <main>
      <h1>At a Glance</h1>

      <AppToolbar onChanged={loadDashboard} />

      <LocationSelect
        locations={locations}
        value={selectedLocationKey}
        onChange={setSelectedLocationKey}
      />

      <ViewTabs value={view} onChange={setView} />

      {error && <p>Error: {error}</p>}
      {!dashboard && !error && <p>Loading...</p>}

      {dashboard && (
        <>
          <p>Updated: {formatTime(dashboard.generated_at)}</p>
          <ActiveView dashboard={dashboard} />
        </>
      )}
    </main>
  );
}