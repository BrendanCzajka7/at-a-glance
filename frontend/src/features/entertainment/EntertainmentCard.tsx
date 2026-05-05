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
  const hasItems =
    concerts.length > 0 || movies.length > 0 || music.length > 0;

  return (
    <div className="entertainment-card">
      <p className="card-eyebrow">Entertainment</p>
      <h2>Things to watch and hear</h2>

      {!hasItems && <p>No concerts, movies, or music releases today.</p>}

      {hasItems && (
        <div className="entertainment-rail">
          {concerts.map((concert) => (
            <article
              className="entertainment-item"
              key={`concert-${concert.name}-${concert.event_date}-${concert.venue_name}`}
            >
              <small className="entertainment-label">Concert</small>

              <strong>
                {concert.source_url ? (
                  <a href={concert.source_url} target="_blank" rel="noreferrer">
                    {concert.name}
                  </a>
                ) : (
                  concert.name
                )}
              </strong>

              <p>
                {formatConcertTime(concert.event_time)}
                {concert.venue_name ? ` · ${concert.venue_name}` : ""}
              </p>

              <small>
                {concert.city}
                {concert.state ? `, ${concert.state}` : ""}
              </small>
            </article>
          ))}

          {movies.map((movie) => (
            <article
              className="entertainment-item"
              key={`movie-${movie.tmdb_movie_id}-${movie.matched_kind}-${movie.matched_name}`}
            >
              <small className="entertainment-label">Movie</small>

              <strong>
                {movie.source_url ? (
                  <a href={movie.source_url} target="_blank" rel="noreferrer">
                    {movie.title}
                  </a>
                ) : (
                  movie.title
                )}
              </strong>

              <p>
                {movie.matched_kind}: {movie.matched_name}
              </p>

              <small>{formatDate(movie.release_date)}</small>
            </article>
          ))}

          {music.map((release) => (
            <article
              className="entertainment-item"
              key={`music-${release.artist_name}-${release.title}-${release.release_date}`}
            >
              <small className="entertainment-label">Music</small>

              <strong>
                {release.source_url ? (
                  <a href={release.source_url} target="_blank" rel="noreferrer">
                    {release.artist_name}
                  </a>
                ) : (
                  release.artist_name
                )}
              </strong>

              <p>{release.title}</p>

              <small>{formatDate(release.release_date)}</small>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}