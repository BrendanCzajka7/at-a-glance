import { Cloud, CloudRain, Sun, Thermometer, Wind } from "lucide-react";

import type { Dashboard } from "../../types/dashboard";
import {
  cloudCoverLabel,
  formatTime,
  windDirectionLabel,
} from "./weatherFormat";

type Props = {
  weather: Dashboard["weather"];
};

function compactNumber(value: number | null, suffix = "") {
  if (value === null || value === undefined) return "N/A";
  return `${Math.round(value)}${suffix}`;
}

export function WeatherAtGlance({ weather }: Props) {
  const current = weather.current;
  const currentUv = weather.next_hours[0]?.uv_index ?? null;

  if (!current) {
    return (
      <section>
        <h3>Weather</h3>
        <p>No current weather.</p>
      </section>
    );
  }

  return (
    <section>
      <h3>Weather</h3>

      <p>{current.location_name}</p>

      <p>
        <Thermometer size={16} /> {compactNumber(current.temperature_f, "°F")}
      </p>

      <p>
        <Cloud size={16} /> {cloudCoverLabel(current.cloud_cover)}
      </p>

      <p>
        <Sun size={16} /> {currentUv ?? "N/A"}
      </p>

      <p>
        <CloudRain size={16} /> {current.precipitation_inches ?? "N/A"} in
      </p>

      <p>
        <Wind size={16} /> {compactNumber(current.wind_speed_mph, " mph")}{" "}
        {windDirectionLabel(current.wind_direction_degrees)}
      </p>

      <small>Observed {formatTime(current.forecast_for)}</small>
    </section>
  );
}