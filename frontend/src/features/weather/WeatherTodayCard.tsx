import { Cloud, CloudRain, Droplets, Sun, Thermometer, Waves, Wind } from "lucide-react";

import type {
  Dashboard,
  NoaaTidePrediction,
  WeatherHour,
} from "../../types/dashboard";
import {
  cloudCoverLabel,
  formatTime,
  weatherCodeLabel,
  windDirectionLabel,
} from "./weatherFormat";

type Props = {
  weather: Dashboard["weather"];
  ocean: Dashboard["ocean"]["current"];
  tides: Dashboard["noaa"]["tides_today"];
};

function formatNumber(value: number | null | undefined, suffix = "") {
  if (value === null || value === undefined) return "N/A";
  return `${Math.round(value)}${suffix}`;
}

function formatDecimal(value: number | null | undefined, suffix = "") {
  if (value === null || value === undefined) return "N/A";
  return `${value.toFixed(1)}${suffix}`;
}

function tideLabel(type: string | null) {
  if (type === "H") return "High";
  if (type === "L") return "Low";
  return "Tide";
}

function getRelevantTides(tides: NoaaTidePrediction[]) {
  const now = new Date();

  const sorted = [...tides].sort(
    (a, b) =>
      new Date(a.prediction_time).getTime() -
      new Date(b.prediction_time).getTime()
  );

  const nextIndex = sorted.findIndex(
    (tide) => new Date(tide.prediction_time) >= now
  );

  if (nextIndex === -1) {
    return sorted.slice(-2);
  }

  const previous = nextIndex > 0 ? [sorted[nextIndex - 1]] : [];
  const upcoming = sorted.slice(nextIndex, nextIndex + 2);

  return [...previous, ...upcoming];
}

function HourPill({ hour }: { hour: WeatherHour }) {
  return (
    <div className="weather-hour-pill">
      <strong>{formatTime(hour.forecast_for)}</strong>
      <span>{formatNumber(hour.temperature_f, "°")}</span>
      <small>{weatherCodeLabel(hour.weather_code)}</small>
    </div>
  );
}

export function WeatherTodayCard({ weather, ocean, tides }: Props) {
  const current = weather.current;
  const summary = weather.today.summary;
  const relevantTides = getRelevantTides(tides);
  const nextHours = weather.next_hours.slice(0, 5);

  if (!current && !summary) {
    return (
      <div>
        <p className="card-eyebrow">Weather Today</p>
        <h2>Weather unavailable</h2>
        <p>No current weather data has been ingested yet.</p>
      </div>
    );
  }

  return (
    <div>
      <p className="card-eyebrow">Weather Today</p>

      <div className="weather-snapshot-header">
        <div>
          <h2 className="weather-temp">
            {formatNumber(current?.temperature_f, "°")}
          </h2>
          <p className="weather-location">{current?.location_name ?? "Selected location"}</p>
        </div>

        <div className="weather-summary-pill">
          {summary ? weatherCodeLabel(summary.weather_code) : "Current"}
        </div>
      </div>

      <div className="metric-grid">
        <div className="metric-item">
          <Thermometer size={16} />
          <span>
            {formatNumber(summary?.temperature_max_f, "°")} /{" "}
            {formatNumber(summary?.temperature_min_f, "°")}
          </span>
          <small>High / low</small>
        </div>

        <div className="metric-item">
          <CloudRain size={16} />
          <span>{formatNumber(summary?.precipitation_probability, "%")}</span>
          <small>Rain chance</small>
        </div>

        <div className="metric-item">
          <Sun size={16} />
          <span>{summary?.uv_index ?? "N/A"}</span>
          <small>UV</small>
        </div>

        <div className="metric-item">
          <Wind size={16} />
          <span>
            {formatNumber(current?.wind_speed_mph, " mph")}{" "}
            {windDirectionLabel(current?.wind_direction_degrees ?? null)}
          </span>
          <small>Wind</small>
        </div>

        <div className="metric-item">
          <Cloud size={16} />
          <span>{cloudCoverLabel(current?.cloud_cover ?? null)}</span>
          <small>Clouds</small>
        </div>

        <div className="metric-item">
          <Droplets size={16} />
          <span>{formatDecimal(current?.precipitation_inches, " in")}</span>
          <small>Now</small>
        </div>
      </div>

      <div className="weather-ocean-row">
        <div>
          <p className="mini-label">Ocean</p>
          {ocean ? (
            <>
              <p>
                <Waves size={16} /> Water {formatNumber(ocean.water_temperature_f, "°F")}
              </p>
              <p>Waves {formatDecimal(ocean.wave_height_ft, " ft")}</p>
            </>
          ) : (
            <p>No ocean conditions yet.</p>
          )}
        </div>

        <div>
          <p className="mini-label">Tides</p>
          {relevantTides.length === 0 && <p>No tide predictions loaded.</p>}
          {relevantTides.map((tide) => (
            <p key={`${tide.station_id}-${tide.prediction_time}-${tide.tide_type}`}>
              {tideLabel(tide.tide_type)} · {formatTime(tide.prediction_time)} ·{" "}
              {formatDecimal(tide.height_ft, " ft")}
            </p>
          ))}
        </div>
      </div>

      {nextHours.length > 0 && (
        <div className="weather-hours-strip">
          {nextHours.map((hour) => (
            <HourPill key={hour.forecast_for} hour={hour} />
          ))}
        </div>
      )}

      {current && <small>Observed {formatTime(current.forecast_for)}</small>}
    </div>
  );
}