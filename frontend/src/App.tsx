import { useEffect, useState } from "react";

type WeatherSnapshot = {
  id: number;
  location_name: string;
  temperature_f: number;
  wind_speed_mph: number | null;
  observed_at: string;
};

export default function App() {
  const [data, setData] = useState<WeatherSnapshot[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/weather/latest")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  const latest = data[0];

  return (
    <main style={{ padding: 24, fontFamily: "Arial" }}>
      <h1>Weather</h1>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!error && !latest && <p>No data yet.</p>}

      {latest && (
        <div>
          <h2>{latest.location_name}</h2>
          <p>{latest.temperature_f}°F</p>
          <p>Wind: {latest.wind_speed_mph ?? "N/A"} mph</p>
          <p>Observed: {new Date(latest.observed_at).toLocaleString()}</p>
        </div>
      )}
    </main>
  );
}