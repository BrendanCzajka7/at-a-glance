import {
  Cloud,
  CloudRain,
  Droplets,
  Sun,
  Sunrise,
  Sunset,
  Thermometer,
  Wind,
} from "lucide-react";

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

export function WeatherTodaySection({ weather }: Props) {
  const current = weather.current;
  const summary = weather.today.summary;
  const currentUv = weather.next_hours[0]?.uv_index ?? null;

  return (
    <div style={{ display: "flex", gap: 24 }}>
      <section style={{ flex: 1 }}>
        <h2>At a Glance</h2>

        {current && (
          <>
            <h3>{current.location_name}</h3>

            <p>
              <Thermometer size={16} />{" "}
              {compactNumber(current.temperature_f, "°F")}
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
          </>
        )}

        {summary && (
          <>
            <h3>Today Summary</h3>

            <p>
              <Thermometer size={16} />{" "}
              {compactNumber(summary.temperature_max_f, "°F")} /{" "}
              {compactNumber(summary.temperature_min_f, "°F")}
            </p>

            <p>
              <Droplets size={16} />{" "}
              {compactNumber(summary.precipitation_probability, "%")}
            </p>

            <p>
              <Sun size={16} /> {summary.uv_index ?? "N/A"}
            </p>

            <p>
              <Sunrise size={16} /> {formatTime(summary.sunrise)}
            </p>

            <p>
              <Sunset size={16} /> {formatTime(summary.sunset)}
            </p>

            <p>
              {summary.weather_code !== null &&
                weatherCodeLabel(summary.weather_code)}
            </p>
          </>
        )}
      </section>

      <section style={{ flex: 1 }}>
        <h2>Next Hours</h2>

        {weather.next_hours.map((hour) => (
          <div key={hour.forecast_for}>
            <strong>{formatTime(hour.forecast_for)}</strong>

            <p>
              <Thermometer size={14} /> {compactNumber(hour.temperature_f, "°F")}{" "}
              · {weatherCodeLabel(hour.weather_code)} ·{" "}
              <Droplets size={14} />{" "}
              {compactNumber(hour.precipitation_probability, "%")} ·{" "}
              <Cloud size={14} /> {cloudCoverLabel(hour.cloud_cover)} ·{" "}
              <Wind size={14} /> {compactNumber(hour.wind_speed_mph, " mph")}{" "}
              {windDirectionLabel(hour.wind_direction_degrees)} ·{" "}
              <Sun size={14} /> {hour.uv_index ?? "N/A"}
            </p>
          </div>
        ))}
      </section>
    </div>
  );
}