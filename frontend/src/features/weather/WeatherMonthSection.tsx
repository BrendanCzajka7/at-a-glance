import type { WeatherDay } from "../../types/dashboard";
import { weatherCodeLabel } from "./weatherFormat";

type Props = {
  days: WeatherDay[];
};

export function WeatherMonthSection({ days }: Props) {
  return (
    <section>
      <h2>Month</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, minmax(80px, 1fr))",
          gap: 8,
        }}
      >
        {days.map((day) => {
          const date = new Date(day.forecast_for);

          return (
            <div
              key={day.forecast_for}
              style={{
                border: "1px solid #ccc",
                padding: 8,
                minHeight: 80,
              }}
            >
              <strong>{date.getDate()}</strong>
              <p>
                {day.temperature_max_f}° / {day.temperature_min_f}°
              </p>
              <p>{day.precipitation_probability}% rain</p>
              <small>{weatherCodeLabel(day.weather_code)}</small>
            </div>
          );
        })}
      </div>
    </section>
  );
}