import { NasaSpaceWeatherWeek } from "../features/nasa/NasaSpaceWeatherWeek";
import { WeatherWeekSection } from "../features/weather/WeatherWeekSection";
import type {
  Dashboard,
  NasaSpaceWeatherCard,
  WeatherDay,
} from "../types/dashboard";
import { weatherCodeLabel } from "../features/weather/weatherFormat";

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

function noticesForDay(
  notices: NasaSpaceWeatherCard[],
  dayKey: string
) {
  return notices.filter(
    (notice) => dateKey(notice.message_issue_time) === dayKey
  );
}

function WeekDayBox({
  weatherDay,
  nasaNotices,
}: {
  weatherDay: WeatherDay;
  nasaNotices: NasaSpaceWeatherCard[];
}) {
  return (
    <section
      style={{
        minWidth: 180,
        border: "1px solid #ccc",
        padding: 12,
      }}
    >
      <h3>{formatWeekday(weatherDay.forecast_for)}</h3>

      <div>
        <strong>Weather</strong>
        <p>{weatherCodeLabel(weatherDay.weather_code)}</p>
        <p>
          {Math.round(weatherDay.temperature_max_f ?? 0)}° /{" "}
          {Math.round(weatherDay.temperature_min_f ?? 0)}°
        </p>
        <p>Rain: {weatherDay.precipitation_probability ?? "N/A"}%</p>
        <p>UV: {weatherDay.uv_index ?? "N/A"}</p>
      </div>

      <div>
        <strong>NASA</strong>

        {nasaNotices.length === 0 && <p>No notices</p>}

        {nasaNotices.map((notice) => (
          <p key={notice.message_id}>
            {notice.title} {notice.message_type ? `(${notice.message_type})` : ""}
          </p>
        ))}
      </div>
    </section>
  );
}

export function WeekView({ dashboard }: Props) {
  const weekDays = dashboard.weather.week.days;
  const nasaWeek = dashboard.nasa.space_weather.week;

  return (
    <section>
      <h2>Week</h2>

      <div style={{ display: "flex", gap: 12, overflowX: "auto" }}>
        {weekDays.map((day) => {
          const key = dateKey(day.forecast_for);

          return (
            <WeekDayBox
              key={day.forecast_for}
              weatherDay={day}
              nasaNotices={noticesForDay(nasaWeek, key)}
            />
          );
        })}
      </div>
    </section>
  );
}