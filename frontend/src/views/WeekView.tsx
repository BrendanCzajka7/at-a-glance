import { MusicReleasesMini } from "../features/music/MusicReleasesMini";
import { NoaaSpaceWeatherMini } from "../features/noaa/NoaaSpaceWeatherMini";
import { NasaNeoMini } from "../features/nasa/NasaNeoMini";
import { SpaceLaunchesMini } from "../features/space/SpaceLaunchesMini";
import { TicketmasterConcertsMini } from "../features/ticketmaster/TicketmasterConcertsMini";
import { TmdbMoviesMini } from "../features/tmdb/TmdbMoviesMini";
import { weatherCodeLabel } from "../features/weather/weatherFormat";
import type {
  Dashboard,
  NasaNeo,
  NoaaSpaceWeatherDay,
  WeatherDay,
} from "../types/dashboard";

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

function releasesForDay(
  releases: Dashboard["music"]["week"],
  dayKey: string
) {
  return releases.filter((release) => release.release_date === dayKey);
}

function moviesForDay(
  movies: Dashboard["tmdb"]["week"],
  dayKey: string
) {
  return movies.filter((movie) => movie.release_date === dayKey);
}

function concertsForDay(
  concerts: Dashboard["ticketmaster"]["week"],
  dayKey: string
) {
  return concerts.filter((concert) => concert.event_date === dayKey);
}

function launchesForDay(
  launches: Dashboard["space"]["week"],
  dayKey: string
) {
  return launches.filter(
    (launch) => new Date(launch.net).toISOString().slice(0, 10) === dayKey
  );
}

function spaceWeatherForDay(
  days: NoaaSpaceWeatherDay[] | undefined,
  dayKey: string
): NoaaSpaceWeatherDay | null {
  return days?.find((item) => item.date === dayKey) ?? null;
}

function round(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return Math.round(value);
}

function WeekDayBox({
  weatherDay,
  neos,
  musicReleases,
  movies,
  concerts,
  launches,
  spaceWeatherDay,
}: {
  weatherDay: WeatherDay;
  neos: NasaNeo[];
  musicReleases: Dashboard["music"]["week"];
  movies: Dashboard["tmdb"]["week"];
  concerts: Dashboard["ticketmaster"]["week"];
  launches: Dashboard["space"]["week"];
  spaceWeatherDay: NoaaSpaceWeatherDay | null;
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

      <NoaaSpaceWeatherMini day={spaceWeatherDay} />

      <TicketmasterConcertsMini concerts={concerts} />

      <MusicReleasesMini releases={musicReleases} />

      <TmdbMoviesMini movies={movies} />

      <SpaceLaunchesMini launches={launches} />

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
              musicReleases={releasesForDay(dashboard.music.week, key)}
              movies={moviesForDay(dashboard.tmdb.week, key)}
              concerts={concertsForDay(dashboard.ticketmaster.week, key)}
              launches={launchesForDay(dashboard.space.week, key)}
              spaceWeatherDay={spaceWeatherForDay(
                dashboard.noaa.space_weather?.forecast_days,
                key
              )}
            />
          );
        })}
      </div>
    </section>
  );
}