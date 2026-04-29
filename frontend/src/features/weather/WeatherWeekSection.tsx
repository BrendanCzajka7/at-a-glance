import type { WeatherDay } from "../../types/dashboard";
import { formatDate, weatherCodeLabel } from "./weatherFormat";

type Props = {
  days: WeatherDay[];
};

export function WeatherWeekSection({ days }: Props) {
  return (
    <section>
      <h2>Week</h2>

      <div style={{ display: "flex", gap: 12, overflowX: "auto" }}>
        {days.map((day) => (
          <div
            key={day.forecast_for}
            style={{
              minWidth: 160,
              border: "1px solid #ccc",
              padding: 12,
            }}
          >
            <h3>{formatDate(day.forecast_for)}</h3>
            <p>{weatherCodeLabel(day.weather_code)}</p>
            <p>
              {day.temperature_max_f}° / {day.temperature_min_f}°
            </p>
            <p>Rain: {day.precipitation_probability}%</p>
            <p>UV: {day.uv_index}</p>
          </div>
        ))}
      </div>
    </section>
  );
}