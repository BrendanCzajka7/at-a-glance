import type { Dashboard } from "../types/dashboard";
import { WeatherMonthSection } from "../features/weather/WeatherMonthSection";

type Props = {
  dashboard: Dashboard;
};

export function MonthView({ dashboard }: Props) {
  return <WeatherMonthSection days={dashboard.weather.month.days} />;
}