import { useEffect, useState } from "react";

type WeatherCurrent = {
  location_name: string;
  forecast_for: string;
  temperature_f: number | null;
  apparent_temperature_f: number | null;
  precipitation_inches: number | null;
  wind_speed_mph: number | null;
  wind_gust_mph: number | null;
};

type WeatherHourly = {
  forecast_for: string;
  temperature_f: number | null;
  apparent_temperature_f: number | null;
  precipitation_probability: number | null;
  wind_speed_mph: number | null;
  uv_index: number | null;
};

type WeatherDaily = {
  forecast_for: string;
  temperature_max_f: number | null;
  temperature_min_f: number | null;
  precipitation_probability: number | null;
  precipitation_inches: number | null;
  uv_index: number | null;
  sunrise: string | null;
  sunset: string | null;
};

type Dashboard = {
  generated_at: string;
  start: string;
  end: string;
  weather: {
    current: WeatherCurrent | null;
    hourly: WeatherHourly[];
    daily: WeatherDaily[];
  };
};

export default function App() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const res = await fetch("/api/dashboard");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        setDashboard(await res.json());
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    }

    loadDashboard();
    const id = setInterval(loadDashboard, 60_000);

    return () => clearInterval(id);
  }, []);

  if (error) {
    return <main>Error: {error}</main>;
  }

  if (!dashboard) {
    return <main>Loading...</main>;
  }

  const { current, hourly, daily } = dashboard.weather;
  const now = new Date();

  const upcomingHourly = hourly
    .filter((hour) => new Date(hour.forecast_for) >= now)
    .slice(0, 6);

  return (
    <main>
      <h1>At a Glance</h1>
      <p>Updated: {new Date(dashboard.generated_at).toLocaleTimeString()}</p>

      <section>
        <h2>Weather</h2>

        {current && (
          <section>
            <h3>Current</h3>
            <p>{current.location_name}</p>
            <p>
              {current.temperature_f}°F, feels like{" "}
              {current.apparent_temperature_f}°F
            </p>
            <p>
              Wind: {current.wind_speed_mph} mph, gusts{" "}
              {current.wind_gust_mph} mph
            </p>
          </section>
        )}

        <section>
          <h3>Daily</h3>
          {daily.map((day) => (
            <div key={day.forecast_for}>
              <strong>{new Date(day.forecast_for).toLocaleDateString()}</strong>
              <p>
                High {day.temperature_max_f}°F / Low {day.temperature_min_f}°F
              </p>
              <p>
                Rain: {day.precipitation_probability}% | UV: {day.uv_index}
              </p>
              <p>
                Sunrise:{" "}
                {day.sunrise ? new Date(day.sunrise).toLocaleTimeString() : "N/A"}{" "}
                | Sunset:{" "}
                {day.sunset ? new Date(day.sunset).toLocaleTimeString() : "N/A"}
              </p>
            </div>
          ))}
        </section>

        <section>
          <h3>Next 6 Hours</h3>
          {upcomingHourly.map((hour) => (
            <div key={hour.forecast_for}>
              <strong>{new Date(hour.forecast_for).toLocaleTimeString()}</strong>
              <span>
                {" "}
                — {hour.temperature_f}°F, rain{" "}
                {hour.precipitation_probability}%, wind {hour.wind_speed_mph} mph
              </span>
            </div>
          ))}
        </section>
      </section>
    </main>
  );
}