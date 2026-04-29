import { Droplets, Sun, Sunrise, Sunset, Thermometer } from "lucide-react";

import type { Dashboard } from "../../types/dashboard";
import { formatTime, weatherCodeLabel } from "./weatherFormat";

type Props = {
  weather: Dashboard["weather"];
};

function compactNumber(value: number | null, suffix = "") {
  if (value === null || value === undefined) return "N/A";
  return `${Math.round(value)}${suffix}`;
}

export function WeatherTodaySummary({ weather }: Props) {
  const summary = weather.today.summary;

  if (!summary) {
    return (
      <section>
        <h3>Weather Summary</h3>
        <p>No daily summary.</p>
      </section>
    );
  }

  return (
    <section>
      <h3>Weather Summary</h3>

      <p>{weatherCodeLabel(summary.weather_code)}</p>

      <p>
        <Thermometer size={16} /> {compactNumber(summary.temperature_max_f, "°F")}{" "}
        / {compactNumber(summary.temperature_min_f, "°F")}
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
    </section>
  );
}