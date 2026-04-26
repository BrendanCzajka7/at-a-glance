import { useEffect, useState } from "react";

type Location = {
  key: string;
  name: string;
};

type WeatherCurrent = {
  location_name: string;
  forecast_for: string;
  temperature_f: number | null;
  apparent_temperature_f: number | null;
  wind_speed_mph: number | null;
  wind_gust_mph: number | null;
};

type WeatherHourly = {
  forecast_for: string;
  temperature_f: number | null;
  precipitation_probability: number | null;
  wind_speed_mph: number | null;
};

type WeatherDaily = {
  forecast_for: string;
  temperature_max_f: number | null;
  temperature_min_f: number | null;
  precipitation_probability: number | null;
  uv_index: number | null;
};

type Dashboard = {
  generated_at: string;
  weather: {
    current: WeatherCurrent | null;
    hourly: WeatherHourly[];
    daily: WeatherDaily[];
  };
};

export default function App() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [selectedLocationKey, setSelectedLocationKey] =
    useState("okaloosa_island");
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/locations")
      .then((res) => {
        if (!res.ok) throw new Error(`Locations HTTP ${res.status}`);
        return res.json();
      })
      .then(setLocations)
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const res = await fetch(
          `/api/dashboard?location_key=${selectedLocationKey}`
        );

        if (!res.ok) throw new Error(`Dashboard HTTP ${res.status}`);

        setDashboard(await res.json());
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    }

    loadDashboard();
    const id = setInterval(loadDashboard, 60_000);

    return () => clearInterval(id);
  }, [selectedLocationKey]);

  const hourly = dashboard?.weather.hourly ?? [];
  const now = new Date();

  const upcomingHourly = hourly
    .filter((hour) => new Date(hour.forecast_for) >= now)
    .slice(0, 6);

  return (
    <main>
      <h1>At a Glance</h1>

      <label>
        Location:{" "}
        <select
          value={selectedLocationKey}
          onChange={(e) => setSelectedLocationKey(e.target.value)}
        >
          {locations.map((location) => (
            <option key={location.key} value={location.key}>
              {location.name}
            </option>
          ))}
        </select>
      </label>

      {error && <p>Error: {error}</p>}

      {!dashboard && !error && <p>Loading...</p>}

      {dashboard && (
        <>
          <p>Updated: {new Date(dashboard.generated_at).toLocaleTimeString()}</p>

          <section>
            <h2>Weather</h2>

            {dashboard.weather.current && (
              <section>
                <h3>Current</h3>
                <p>{dashboard.weather.current.location_name}</p>
                <p>
                  {dashboard.weather.current.temperature_f}°F, feels like{" "}
                  {dashboard.weather.current.apparent_temperature_f}°F
                </p>
                <p>
                  Wind: {dashboard.weather.current.wind_speed_mph} mph, gusts{" "}
                  {dashboard.weather.current.wind_gust_mph} mph
                </p>
              </section>
            )}

            <section>
              <h3>Daily</h3>
              {dashboard.weather.daily.map((day) => (
                <div key={day.forecast_for}>
                  <strong>
                    {new Date(day.forecast_for).toLocaleDateString()}
                  </strong>
                  <p>
                    High {day.temperature_max_f}°F / Low{" "}
                    {day.temperature_min_f}°F
                  </p>
                  <p>
                    Rain: {day.precipitation_probability}% | UV: {day.uv_index}
                  </p>
                </div>
              ))}
            </section>

            <section>
              <h3>Next 6 Hours</h3>
              {upcomingHourly.map((hour) => (
                <div key={hour.forecast_for}>
                  <strong>
                    {new Date(hour.forecast_for).toLocaleTimeString([], {
                      hour: "numeric",
                      minute: "2-digit",
                    })}
                  </strong>
                  <span>
                    {" "}
                    — {hour.temperature_f}°F, rain{" "}
                    {hour.precipitation_probability}%, wind{" "}
                    {hour.wind_speed_mph} mph
                  </span>
                </div>
              ))}
            </section>
          </section>
        </>
      )}
    </main>
  );
}