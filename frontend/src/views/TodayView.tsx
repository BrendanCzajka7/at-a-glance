import { MusicReleasesSection } from "../features/music/MusicReleasesSection";
import { NasaApodSection } from "../features/nasa/NasaApodSection";
import { NasaEpicSection } from "../features/nasa/NasaEpicSection";
import { NasaNeoToday } from "../features/nasa/NasaNeoToday";
import { WeatherAtGlance } from "../features/weather/WeatherAtGlance";
import { WeatherTodaySummary } from "../features/weather/WeatherTodaySummary";
import { WeatherUpcomingHours } from "../features/weather/WeatherUpcomingHours";
import type { Dashboard } from "../types/dashboard";
import { TmdbMoviesMini } from "../features/tmdb/TmdbMoviesMini";
import { TicketmasterConcertsMini } from "../features/ticketmaster/TicketmasterConcertsMini";
import { SpaceLaunchesMini } from "../features/space/SpaceLaunchesMini";
import { UsgsEarthToday } from "../features/usgs/UsgsEarthToday";

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
        <UsgsEarthToday
        largest={dashboard.usgs.largest_today}
        mostSignificant={dashboard.usgs.most_significant_today}
        tsunamiEvents={dashboard.usgs.tsunami_events_today}
        alertEvents={dashboard.usgs.alert_events_today}
      />

        <MusicReleasesSection
          title="Music Releases Today"
          releases={dashboard.music.today}
        />
        <TmdbMoviesMini movies={dashboard.tmdb.today} />
        <TicketmasterConcertsMini concerts={dashboard.ticketmaster.today} />
        <NasaApodSection nasa={dashboard.nasa} />
        <NasaEpicSection nasa={dashboard.nasa} />
        <NasaNeoToday neos={dashboard.nasa.neos.today} />
        <SpaceLaunchesMini launches={dashboard.space.today} />
      </section>
    </div>
  );
}