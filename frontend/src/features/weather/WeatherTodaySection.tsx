import type { Dashboard } from "../../types/dashboard";
import { formatTime, weatherCodeLabel } from "./weatherFormat";

type Props = {
  weather: Dashboard["weather"];
};

export function WeatherTodaySection({ weather }: Props) {
  const current = weather.current;
  const summary = weather.today.summary;

  return (
    <div style={{ display: "flex", gap: 24 }}>
      <section style={{ flex: 1 }}>
        <h2>At a Glance</h2>

        {current && (
          <>
            <h3>{current.location_name}</h3>
            <p>
              {current.temperature_f}°F, feels {current.apparent_temperature_f}°F
            </p>
            <p>{weatherCodeLabel(current.weather_code)}</p>
            <p>
              Wind: {current.wind_speed_mph} mph, gusts {current.wind_gust_mph} mph
            </p>
            <p>Cloud cover: {current.cloud_cover}%</p>
          </>
        )}

        {summary && (
          <>
            <h3>Today Summary</h3>
            <p>
              High {summary.temperature_max_f}°F / Low{" "}
              {summary.temperature_min_f}°F
            </p>
            <p>Rain: {summary.precipitation_probability}%</p>
            <p>UV: {summary.uv_index}</p>
            <p>Sunrise: {formatTime(summary.sunrise)}</p>
            <p>Sunset: {formatTime(summary.sunset)}</p>
          </>
        )}
      </section>

      <section style={{ flex: 1 }}>
        <h2>Next Hours</h2>

        {weather.next_hours.map((hour) => (
          <div key={hour.forecast_for}>
            <strong>{formatTime(hour.forecast_for)}</strong>
            <p>
              {hour.temperature_f}°F — {weatherCodeLabel(hour.weather_code)} —
              Rain {hour.precipitation_probability}% — Cloud{" "}
              {hour.cloud_cover}% — Wind {hour.wind_speed_mph} mph
            </p>
          </div>
        ))}
      </section>
    </div>
  );
}