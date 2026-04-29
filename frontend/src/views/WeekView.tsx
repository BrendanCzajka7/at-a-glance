import type { Dashboard } from "../types/dashboard";
import { WeatherWeekSection } from "../features/weather/WeatherWeekSection";

type Props = {
  dashboard: Dashboard;
};

export function WeekView({ dashboard }: Props) {
  return <WeatherWeekSection days={dashboard.weather.week.days} />;
}