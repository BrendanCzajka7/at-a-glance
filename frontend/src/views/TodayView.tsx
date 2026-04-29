import { NasaApodSection } from "../features/nasa/NasaApodSection";
import { NasaSpaceWeatherToday } from "../features/nasa/NasaSpaceWeatherToday";
import { WeatherAtGlance } from "../features/weather/WeatherAtGlance";
import { WeatherTodaySummary } from "../features/weather/WeatherTodaySummary";
import { WeatherUpcomingHours } from "../features/weather/WeatherUpcomingHours";
import type { Dashboard } from "../types/dashboard";

type Props = {
  dashboard: Dashboard;
};

export function TodayView({ dashboard }: Props) {
  return (
    <div style={{ display: "flex", gap: 24 }}>
      <section style={{ flex: 1 }}>
        <h2>At a Glance</h2>
        <WeatherAtGlance weather={dashboard.weather} />
        <WeatherUpcomingHours weather={dashboard.weather} />
      </section>

      <section style={{ flex: 1 }}>
        <h2>Today</h2>
        <WeatherTodaySummary weather={dashboard.weather} />
        <NasaApodSection nasa={dashboard.nasa} />
        <NasaSpaceWeatherToday
          notifications={dashboard.nasa.space_weather.today}
        />
      </section>
    </div>
  );
}