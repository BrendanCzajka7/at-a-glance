import { NasaNeoMini } from "../features/nasa/NasaNeoMini";
import { weatherCodeLabel } from "../features/weather/weatherFormat";
import type { Dashboard, NasaNeo, WeatherDay } from "../types/dashboard";

type Props = {
  dashboard: Dashboard;
};

function dateKey(value: string) {
  return new Date(value).toISOString().slice(0, 10);
}

function formatWeekday(value: string) {
  return new Date(value).toLocaleDateString([], {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
}

function neosForDay(neos: NasaNeo[], dayKey: string) {
  return neos.filter((neo) => neo.close_approach_date === dayKey);
}

function round(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return Math.round(value);
}

function WeekDayBox({
  weatherDay,
  neos,
}: {
  weatherDay: WeatherDay;
  neos: NasaNeo[];
}) {
  return (
    <section
      style={{
        minWidth: 190,
        border: "1px solid #ccc",
        padding: 12,
      }}
    >
      <h3>{formatWeekday(weatherDay.forecast_for)}</h3>

      <div>
        <strong>Weather</strong>
        <p>{weatherCodeLabel(weatherDay.weather_code)}</p>
        <p>
          {round(weatherDay.temperature_max_f)}° /{" "}
          {round(weatherDay.temperature_min_f)}°
        </p>
        <p>Rain: {weatherDay.precipitation_probability ?? "N/A"}%</p>
        <p>UV: {weatherDay.uv_index ?? "N/A"}</p>
      </div>

      <NasaNeoMini neos={neos} />
    </section>
  );
}

export function WeekView({ dashboard }: Props) {
  return (
    <section>
      <h2>Week</h2>

      <div style={{ display: "flex", gap: 12, overflowX: "auto" }}>
        {dashboard.weather.week.days.map((day) => {
          const key = dateKey(day.forecast_for);

          return (
            <WeekDayBox
              key={day.forecast_for}
              weatherDay={day}
              neos={neosForDay(dashboard.nasa.neos.week, key)}
            />
          );
        })}
      </div>
    </section>
  );
}