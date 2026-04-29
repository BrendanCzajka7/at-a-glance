import type { Dashboard } from "../types/dashboard";
import { WeatherTodaySection } from "../features/weather/WeatherTodaySection";

type Props = {
  dashboard: Dashboard;
};

export function TodayView({ dashboard }: Props) {
  return <WeatherTodaySection weather={dashboard.weather} />;
}