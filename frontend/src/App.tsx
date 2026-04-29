import { useEffect, useState } from "react";

import { fetchDashboard, fetchLocations } from "./api/dashboard";
import { LocationSelect } from "./components/LocationSelect";
import { ViewTabs } from "./components/ViewTabs";
import type { DashboardView } from "./components/ViewTabs";
import type { Dashboard, Location } from "./types/dashboard";
import { TodayView } from "./views/TodayView";
import { WeekView } from "./views/WeekView";
import { MonthView } from "./views/MonthView";
import { formatTime } from "./features/weather/weatherFormat";

export default function App() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocationKey, setSelectedLocationKey] =
    useState("okaloosa_island");
  const [view, setView] = useState<DashboardView>("today");
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchLocations()
      .then(setLocations)
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setDashboard(await fetchDashboard(selectedLocationKey));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    }

    loadDashboard();
    const id = setInterval(loadDashboard, 60_000);

    return () => clearInterval(id);
  }, [selectedLocationKey]);

  return (
    <main>
      <h1>At a Glance</h1>

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

          {view === "today" && <TodayView dashboard={dashboard} />}
          {view === "week" && <WeekView dashboard={dashboard} />}
          {view === "month" && <MonthView dashboard={dashboard} />}
        </>
      )}
    </main>
  );
}