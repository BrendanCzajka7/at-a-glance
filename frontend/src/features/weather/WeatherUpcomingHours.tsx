import { Cloud, Droplets, Sun, Thermometer, Wind } from "lucide-react";

import type { Dashboard } from "../../types/dashboard";
import {
  cloudCoverLabel,
  formatTime,
  weatherCodeLabel,
  windDirectionLabel,
} from "./weatherFormat";

type Props = {
  weather: Dashboard["weather"];
};

function compactNumber(value: number | null, suffix = "") {
  if (value === null || value === undefined) return "N/A";
  return `${Math.round(value)}${suffix}`;
}

export function WeatherUpcomingHours({ weather }: Props) {
  return (
    <section>
      <h3>Upcoming Hours</h3>

      {weather.next_hours.map((hour) => (
        <div key={hour.forecast_for}>
          <strong>{formatTime(hour.forecast_for)}</strong>

          <p>
            <Thermometer size={14} /> {compactNumber(hour.temperature_f, "°F")} ·{" "}
            {weatherCodeLabel(hour.weather_code)} · <Droplets size={14} />{" "}
            {compactNumber(hour.precipitation_probability, "%")} ·{" "}
            <Cloud size={14} /> {cloudCoverLabel(hour.cloud_cover)} ·{" "}
            <Wind size={14} /> {compactNumber(hour.wind_speed_mph, " mph")}{" "}
            {windDirectionLabel(hour.wind_direction_degrees)} ·{" "}
            <Sun size={14} /> {hour.uv_index ?? "N/A"}
          </p>
        </div>
      ))}
    </section>
  );
}