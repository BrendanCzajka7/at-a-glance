import { weatherCodeLabel } from "../features/weather/weatherFormat";
import type { Dashboard, NasaNeo } from "../types/dashboard";

type Props = {
  dashboard: Dashboard;
};

function dateKey(value: string) {
  return new Date(value).toISOString().slice(0, 10);
}

function neosForDay(neos: NasaNeo[], dayKey: string) {
  return neos.filter((neo) => neo.close_approach_date === dayKey);
}

function round(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return Math.round(value);
}

export function MonthView({ dashboard }: Props) {
  return (
    <section>
      <h2>Month</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, minmax(90px, 1fr))",
          gap: 8,
        }}
      >
        {dashboard.weather.month.days.map((day) => {
          const key = dateKey(day.forecast_for);
          const neos = neosForDay(dashboard.nasa.neos.month, key);
          const date = new Date(day.forecast_for);

          return (
            <div
              key={day.forecast_for}
              style={{
                border: "1px solid #ccc",
                padding: 8,
                minHeight: 95,
              }}
            >
              <strong>{date.getDate()}</strong>

              <p>
                {round(day.temperature_max_f)}° / {round(day.temperature_min_f)}°
              </p>

              <small>{weatherCodeLabel(day.weather_code)}</small>

              {neos.length > 0 && <p>{neos.length} asteroid</p>}
            </div>
          );
        })}
      </div>
    </section>
  );
}