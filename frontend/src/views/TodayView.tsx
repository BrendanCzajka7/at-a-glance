import { DashboardGrid } from "../components/layout/DashboardGrid";
import { Card } from "../components/ui/Card";
import { EntertainmentCard } from "../features/entertainment/EntertainmentCard";
import { PictureOfDayCard } from "../features/nature/PictureOfDayCard";
import { EarthSpaceCard } from "../features/space/EarthSpaceCard";
import { WeatherTodayCard } from "../features/weather/WeatherTodayCard";
import type { Dashboard } from "../types/dashboard";

type Props = {
  dashboard: Dashboard;
};

export function TodayView({ dashboard }: Props) {
  return (
    <DashboardGrid className="today-fit-grid">
      <Card className="today-weather-card">
        <WeatherTodayCard
          weather={dashboard.weather}
          ocean={dashboard.ocean.current}
          tides={dashboard.noaa.tides_today}
        />
      </Card>

      <Card className="today-earth-card">
        <EarthSpaceCard
          noaa={dashboard.noaa}
          usgs={dashboard.usgs}
          nasa={dashboard.nasa}
          launches={dashboard.space.today}
        />
      </Card>

      <Card className="today-picture-card">
        <PictureOfDayCard nature={dashboard.nature} nasa={dashboard.nasa} />
      </Card>

      <Card className="today-entertainment-card">
        <EntertainmentCard
          concerts={dashboard.ticketmaster.today}
          movies={dashboard.tmdb.today}
          music={dashboard.music.today}
        />
      </Card>
    </DashboardGrid>
  );
}