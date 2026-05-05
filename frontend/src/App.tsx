import { useEffect, useState } from "react";

import { fetchDashboard, fetchLocations } from "./api/dashboard";
import { AppToolbar } from "./components/AppToolbar";
import { AppShell } from "./components/layout/AppShell";
import { LocationSelect } from "./components/LocationSelect";
import { StatusText } from "./components/ui/StatusText";
import { ViewTabs } from "./components/ViewTabs";
import type { Dashboard, Location } from "./types/dashboard";
import { getDashboardView, type DashboardView } from "./views/viewRegistry";

export default function App() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocationKey, setSelectedLocationKey] =
    useState("okaloosa_island");
  const [view, setView] = useState<DashboardView>("today");
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const ActiveView = getDashboardView(view).Component;

  useEffect(() => {
    fetchLocations()
      .then(setLocations)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load locations")
      );
  }, []);

  async function loadDashboard() {
    try {
      setError("");
      setIsLoading(true);
      setDashboard(await fetchDashboard(selectedLocationKey));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
    const id = setInterval(loadDashboard, 60_000);

    return () => clearInterval(id);
  }, [selectedLocationKey]);

  return (
    <AppShell
      title="At a Glance"
      updatedAt={dashboard?.generated_at ?? null}
      controls={
        <>
          <LocationSelect
            locations={locations}
            value={selectedLocationKey}
            onChange={setSelectedLocationKey}
          />

          <ViewTabs value={view} onChange={setView} />
        </>
      }
      admin={<AppToolbar onChanged={loadDashboard} />}
    >
      <StatusText error={error} isLoading={isLoading && !dashboard} />

      {dashboard && <ActiveView dashboard={dashboard} />}
    </AppShell>
  );
}