import type {
  MusicRelease,
  TicketmasterConcert,
  TmdbMovieRelease,
} from "../../types/dashboard";

type Props = {
  concerts: TicketmasterConcert[];
  movies: TmdbMovieRelease[];
  music: MusicRelease[];
};

function formatDate(value: string) {
  return new Date(value).toLocaleDateString([], {
    month: "short",
    day: "numeric",
  });
}

function formatConcertTime(value: string | null) {
  if (!value) return "";

  const [hourRaw, minute] = value.split(":");
  const hour = Number(hourRaw);

  if (Number.isNaN(hour)) return value;

  const suffix = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;

  return `${displayHour}:${minute} ${suffix}`;
}

export function EntertainmentCard({ concerts, movies, music }: Props) {
  return (
    <div>
      <p className="card-eyebrow">Entertainment</p>
      <h2>Things to watch and hear</h2>

      <div className="split-card-grid">
        <div>
          <h3>Concerts</h3>

          {concerts.length === 0 && <p>No concerts today.</p>}

          {concerts.slice(0, 4).map((concert) => (
            <p key={`${concert.name}-${concert.event_date}-${concert.venue_name}`}>
              {concert.source_url ? (
                <a href={concert.source_url} target="_blank" rel="noreferrer">
                  {concert.name}
                </a>
              ) : (
                concert.name
              )}
              <small>
                {" "}
                · {formatConcertTime(concert.event_time)}
                {concert.venue_name ? ` · ${concert.venue_name}` : ""}
              </small>
            </p>
          ))}
        </div>

        <div>
          <h3>Movies</h3>

          {movies.length === 0 && <p>No movie releases today.</p>}

          {movies.slice(0, 4).map((movie) => (
            <p key={`${movie.tmdb_movie_id}-${movie.matched_kind}-${movie.matched_name}`}>
              {movie.source_url ? (
                <a href={movie.source_url} target="_blank" rel="noreferrer">
                  {movie.title}
                </a>
              ) : (
                movie.title
              )}
              <small>
                {" "}
                · {movie.matched_kind}: {movie.matched_name}
              </small>
            </p>
          ))}
        </div>

        <div>
          <h3>Music</h3>

          {music.length === 0 && <p>No music releases today.</p>}

          {music.slice(0, 4).map((release) => (
            <p key={`${release.artist_name}-${release.title}-${release.release_date}`}>
              {release.source_url ? (
                <a href={release.source_url} target="_blank" rel="noreferrer">
                  {release.artist_name}: {release.title}
                </a>
              ) : (
                <>
                  {release.artist_name}: {release.title}
                </>
              )}
              <small> · {formatDate(release.release_date)}</small>
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}