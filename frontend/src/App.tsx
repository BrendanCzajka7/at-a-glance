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
  precipitation_inches: number | null;
  wind_speed_mph: number | null;
  wind_gust_mph: number | null;
  wind_direction_degrees: number | null;
  cloud_cover: number | null;
  is_day: number | null;
  weather_code: number | null;
};

type WeatherHourly = {
  forecast_for: string;
  temperature_f: number | null;
  apparent_temperature_f: number | null;
  precipitation_probability: number | null;
  precipitation_inches: number | null;
  wind_speed_mph: number | null;
  wind_gust_mph: number | null;
  wind_direction_degrees: number | null;
  uv_index: number | null;
  cloud_cover: number | null;
  is_day: number | null;
  weather_code: number | null;
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
  weather_code: number | null;
};

type Dashboard = {
  generated_at: string;
  weather: {
    current: WeatherCurrent | null;
    hourly: WeatherHourly[];
    daily: WeatherDaily[];
  };
};

function formatTime(value: string | null) {
  if (!value) return "N/A";
  return new Date(value).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString();
}

function dayNight(value: number | null) {
  if (value === 1) return "Day";
  if (value === 0) return "Night";
  return "N/A";
}

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
          <p>Updated: {formatTime(dashboard.generated_at)}</p>

          <section>
            <h2>Weather</h2>

            <section>
              <h3>Current</h3>

              {dashboard.weather.current ? (
                <>
                  <p>{dashboard.weather.current.location_name}</p>
                  <p>
                    Temperature: {dashboard.weather.current.temperature_f}°F
                  </p>
                  <p>
                    Feels like:{" "}
                    {dashboard.weather.current.apparent_temperature_f}°F
                  </p>
                  <p>
                    Precipitation:{" "}
                    {dashboard.weather.current.precipitation_inches} in
                  </p>
                  <p>
                    Wind: {dashboard.weather.current.wind_speed_mph} mph
                  </p>
                  <p>
                    Gusts: {dashboard.weather.current.wind_gust_mph} mph
                  </p>
                  <p>
                    Wind direction:{" "}
                    {dashboard.weather.current.wind_direction_degrees}°
                  </p>
                  <p>
                    Cloud cover: {dashboard.weather.current.cloud_cover}%
                  </p>
                  <p>Day/night: {dayNight(dashboard.weather.current.is_day)}</p>
                  <p>
                    Weather code: {dashboard.weather.current.weather_code}
                  </p>
                  <p>
                    Observed: {formatTime(dashboard.weather.current.forecast_for)}
                  </p>
                </>
              ) : (
                <p>No current weather.</p>
              )}
            </section>

            <section>
              <h3>Next 6 Hours</h3>

              {upcomingHourly.map((hour) => (
                <div key={hour.forecast_for}>
                  <strong>{formatTime(hour.forecast_for)}</strong>
                  <p>Temperature: {hour.temperature_f}°F</p>
                  <p>Feels like: {hour.apparent_temperature_f}°F</p>
                  <p>Rain chance: {hour.precipitation_probability}%</p>
                  <p>Precipitation: {hour.precipitation_inches} in</p>
                  <p>Wind: {hour.wind_speed_mph} mph</p>
                  <p>Gusts: {hour.wind_gust_mph} mph</p>
                  <p>Wind direction: {hour.wind_direction_degrees}°</p>
                  <p>UV: {hour.uv_index}</p>
                  <p>Cloud cover: {hour.cloud_cover}%</p>
                  <p>Day/night: {dayNight(hour.is_day)}</p>
                  <p>Weather code: {hour.weather_code}</p>
                </div>
              ))}
            </section>

            <section>
              <h3>Daily</h3>

              {dashboard.weather.daily.map((day) => (
                <div key={day.forecast_for}>
                  <strong>{formatDate(day.forecast_for)}</strong>
                  <p>High: {day.temperature_max_f}°F</p>
                  <p>Low: {day.temperature_min_f}°F</p>
                  <p>Rain chance: {day.precipitation_probability}%</p>
                  <p>Precipitation: {day.precipitation_inches} in</p>
                  <p>UV max: {day.uv_index}</p>
                  <p>Sunrise: {formatTime(day.sunrise)}</p>
                  <p>Sunset: {formatTime(day.sunset)}</p>
                  <p>Weather code: {day.weather_code}</p>
                </div>
              ))}
            </section>
          </section>
        </>
      )}
    </main>
  );
}