import { MusicReleasesMini } from "../features/music/MusicReleasesMini";
import { weatherCodeLabel } from "../features/weather/weatherFormat";
import type { Dashboard, NasaNeo } from "../types/dashboard";
import { TmdbMoviesMini } from "../features/tmdb/TmdbMoviesMini";
import { TicketmasterConcertsMini } from "../features/ticketmaster/TicketmasterConcertsMini";

type Props = {
  dashboard: Dashboard;
};

function dateKey(value: string) {
  return new Date(value).toISOString().slice(0, 10);
}

function neosForDay(neos: NasaNeo[], dayKey: string) {
  return neos.filter((neo) => neo.close_approach_date === dayKey);
}

function releasesForDay(
  releases: Dashboard["music"]["month"],
  dayKey: string
) {
  return releases.filter((release) => release.release_date === dayKey);
}

function round(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return Math.round(value);
}
function moviesForDay(
  movies: Dashboard["tmdb"]["month"],
  dayKey: string
) {
  return movies.filter((movie) => movie.release_date === dayKey);
}
function concertsForDay(
  concerts: Dashboard["ticketmaster"]["month"],
  dayKey: string
) {
  return concerts.filter((concert) => concert.event_date === dayKey);
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
          const musicReleases = releasesForDay(dashboard.music.month, key);
          const date = new Date(day.forecast_for);
          const movies = moviesForDay(dashboard.tmdb.month, key);
          const concerts = concertsForDay(dashboard.ticketmaster.month, key);

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
                {round(day.temperature_max_f)}° /{" "}
                {round(day.temperature_min_f)}°
              </p>

              <small>{weatherCodeLabel(day.weather_code)}</small>

              {neos.length > 0 && <p>{neos.length} asteroid</p>}
              {movies.length > 0 && <TmdbMoviesMini movies={movies} />}
              {musicReleases.length > 0 && (
                <MusicReleasesMini releases={musicReleases} />
              )}
              {concerts.length > 0 && (
                <TicketmasterConcertsMini concerts={concerts} />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}