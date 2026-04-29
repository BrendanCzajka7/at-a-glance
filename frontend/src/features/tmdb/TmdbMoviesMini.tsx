import type { TmdbMovieRelease } from "../../types/dashboard";

type Props = {
  movies: TmdbMovieRelease[];
};

export function TmdbMoviesMini({ movies }: Props) {
  if (movies.length === 0) {
    return (
      <div>
        <strong>Movies</strong>
        <p>No releases</p>
      </div>
    );
  }

  return (
    <div>
      <strong>Movies</strong>

      {movies.map((movie) => (
        <p key={`${movie.tmdb_movie_id}-${movie.matched_kind}-${movie.matched_name}`}>
          {movie.title}{" "}
          <small>
            ({movie.matched_kind}: {movie.matched_name})
          </small>
        </p>
      ))}
    </div>
  );
}