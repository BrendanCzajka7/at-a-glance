import { useState } from "react";

import {
  addArtist,
  searchArtists,
  type ArtistSearchResult,
} from "../api/music";
import {
  addTmdbWatchItem,
  searchTmdbDirectors,
  searchTmdbGenres,
  type TmdbDirectorSearchResult,
  type TmdbGenreSearchResult,
} from "../api/tmdb";

type Props = {
  onChanged?: () => void;
};

export function AppToolbar({ onChanged }: Props) {
  const [artistQuery, setArtistQuery] = useState("");
  const [artistResults, setArtistResults] = useState<ArtistSearchResult[]>([]);

  const [directorQuery, setDirectorQuery] = useState("");
  const [directorResults, setDirectorResults] = useState<
    TmdbDirectorSearchResult[]
  >([]);

  const [genreResults, setGenreResults] = useState<TmdbGenreSearchResult[]>([]);

  const [message, setMessage] = useState("");
  const [isBusy, setIsBusy] = useState(false);

  async function handleArtistSearch() {
    const query = artistQuery.trim();
    if (!query) return;

    try {
      setMessage("");
      setIsBusy(true);
      setArtistResults(await searchArtists(query));
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Artist search failed");
    } finally {
      setIsBusy(false);
    }
  }

  async function handleAddArtist(artist: ArtistSearchResult) {
    try {
      setMessage("");
      setIsBusy(true);

      await addArtist(artist.name, artist.musicbrainz_artist_id);

      setMessage(`Added music artist: ${artist.name}`);
      setArtistQuery("");
      setArtistResults([]);

      onChanged?.();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Add artist failed");
    } finally {
      setIsBusy(false);
    }
  }

  async function handleLoadGenres() {
    try {
      setMessage("");
      setIsBusy(true);
      setGenreResults(await searchTmdbGenres());
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Genre lookup failed");
    } finally {
      setIsBusy(false);
    }
  }

  async function handleAddGenre(genre: TmdbGenreSearchResult) {
    try {
      setMessage("");
      setIsBusy(true);

      await addTmdbWatchItem("genre", genre.tmdb_id, genre.name);

      setMessage(`Added movie genre: ${genre.name}`);
      setGenreResults([]);

      onChanged?.();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Add genre failed");
    } finally {
      setIsBusy(false);
    }
  }

  async function handleDirectorSearch() {
    const query = directorQuery.trim();
    if (!query) return;

    try {
      setMessage("");
      setIsBusy(true);
      setDirectorResults(await searchTmdbDirectors(query));
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Director search failed");
    } finally {
      setIsBusy(false);
    }
  }

  async function handleAddDirector(director: TmdbDirectorSearchResult) {
    try {
      setMessage("");
      setIsBusy(true);

      await addTmdbWatchItem("director", director.tmdb_id, director.name);

      setMessage(`Added director: ${director.name}`);
      setDirectorQuery("");
      setDirectorResults([]);

      onChanged?.();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Add director failed");
    } finally {
      setIsBusy(false);
    }
  }

  return (
    <section
      style={{
        border: "1px solid #ccc",
        padding: 12,
        marginBottom: 16,
      }}
    >
      <h2>Tools</h2>

      <section>
        <h3>Add Music Artist</h3>

        <input
          value={artistQuery}
          onChange={(e) => setArtistQuery(e.target.value)}
          placeholder="Search artist..."
        />

        <button
          type="button"
          onClick={handleArtistSearch}
          disabled={isBusy || !artistQuery.trim()}
        >
          Search
        </button>

        {artistResults.map((artist) => (
          <div key={artist.musicbrainz_artist_id}>
            <strong>{artist.name}</strong>{" "}
            <small>
              {artist.type ?? "Artist"}
              {artist.country ? ` · ${artist.country}` : ""}
              {artist.disambiguation ? ` · ${artist.disambiguation}` : ""}
              {artist.score !== null ? ` · score ${artist.score}` : ""}
            </small>{" "}
            <button
              type="button"
              disabled={isBusy}
              onClick={() => handleAddArtist(artist)}
            >
              Add
            </button>
          </div>
        ))}
      </section>

      <section>
        <h3>Add Movie Genre</h3>

        <button type="button" onClick={handleLoadGenres} disabled={isBusy}>
          Load Genres
        </button>

        {genreResults.map((genre) => (
          <div key={genre.tmdb_id}>
            <strong>{genre.name}</strong>{" "}
            <button
              type="button"
              disabled={isBusy}
              onClick={() => handleAddGenre(genre)}
            >
              Add
            </button>
          </div>
        ))}
      </section>

      <section>
        <h3>Add Director</h3>

        <input
          value={directorQuery}
          onChange={(e) => setDirectorQuery(e.target.value)}
          placeholder="Search director..."
        />

        <button
          type="button"
          onClick={handleDirectorSearch}
          disabled={isBusy || !directorQuery.trim()}
        >
          Search
        </button>

        {directorResults.map((director) => (
          <div key={director.tmdb_id}>
            <strong>{director.name}</strong>{" "}
            <small>
              {director.known_for_department ?? "Person"}
              {director.popularity !== null
                ? ` · popularity ${Math.round(director.popularity)}`
                : ""}
            </small>{" "}
            <button
              type="button"
              disabled={isBusy}
              onClick={() => handleAddDirector(director)}
            >
              Add
            </button>
          </div>
        ))}
      </section>

      {message && <p>{message}</p>}
    </section>
  );
}