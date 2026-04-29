import { useState } from "react";

import {
  addArtist,
  listArtists,
  searchArtists,
  type ArtistSearchResult,
  type MusicArtist,
} from "../api/music";
import {
  addTmdbWatchItem,
  listTmdbWatchItems,
  searchTmdbDirectors,
  searchTmdbGenres,
  type TmdbDirectorSearchResult,
  type TmdbGenreSearchResult,
  type TmdbWatchItem,
} from "../api/tmdb";
import { RecentErrorsPanel } from "./RecentErrorsPanel";

type Props = {
  onChanged?: () => void;
};

export function AppToolbar({ onChanged }: Props) {
  const [artistQuery, setArtistQuery] = useState("");
  const [artistResults, setArtistResults] = useState<ArtistSearchResult[]>([]);
  const [currentArtists, setCurrentArtists] = useState<MusicArtist[]>([]);

  const [directorQuery, setDirectorQuery] = useState("");
  const [directorResults, setDirectorResults] = useState<
    TmdbDirectorSearchResult[]
  >([]);
  const [genreResults, setGenreResults] = useState<TmdbGenreSearchResult[]>([]);
  const [currentWatchItems, setCurrentWatchItems] = useState<TmdbWatchItem[]>(
    []
  );

  const [message, setMessage] = useState("");
  const [isBusy, setIsBusy] = useState(false);
  const [showCurrent, setShowCurrent] = useState(false);

  async function refreshCurrentItems() {
    const [artists, watchItems] = await Promise.all([
      listArtists(),
      listTmdbWatchItems(),
    ]);

    setCurrentArtists(artists);
    setCurrentWatchItems(watchItems);
  }

  async function handleShowCurrent() {
    try {
      setMessage("");
      setIsBusy(true);

      await refreshCurrentItems();
      setShowCurrent((value) => !value);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed to load current items");
    } finally {
      setIsBusy(false);
    }
  }

  async function handleArtistSearch() {
    const query = artistQuery.trim();
    if (!query) return;

    try {
      setMessage("");
      setIsBusy(true);

      if (currentArtists.length === 0) {
        await refreshCurrentItems();
      }

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
      await refreshCurrentItems();

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

      if (currentWatchItems.length === 0) {
        await refreshCurrentItems();
      }

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
      await refreshCurrentItems();

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

      if (currentWatchItems.length === 0) {
        await refreshCurrentItems();
      }

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
      await refreshCurrentItems();

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

  function artistAlreadyAdded(artist: ArtistSearchResult) {
    return currentArtists.some(
      (item) => item.musicbrainz_artist_id === artist.musicbrainz_artist_id
    );
  }

  function watchItemAlreadyAdded(kind: "genre" | "director", tmdbId: number) {
    return currentWatchItems.some(
      (item) => item.kind === kind && item.tmdb_id === tmdbId
    );
  }

  const currentGenres = currentWatchItems.filter((item) => item.kind === "genre");
  const currentDirectors = currentWatchItems.filter(
    (item) => item.kind === "director"
  );

  return (
    <section
      style={{
        border: "1px solid #ccc",
        padding: 12,
        marginBottom: 16,
      }}
    >
      <h2>Tools</h2>
      <RecentErrorsPanel />

      <button type="button" onClick={handleShowCurrent} disabled={isBusy}>
        {showCurrent ? "Hide Current Items" : "Show Current Items"}
      </button>

      {showCurrent && (
        <section>
          <h3>Current Items</h3>

          <div>
            <strong>Music Artists</strong>
            {currentArtists.length === 0 && <p>None added.</p>}
            {currentArtists.map((artist) => (
              <p key={artist.musicbrainz_artist_id}>{artist.name}</p>
            ))}
          </div>

          <div>
            <strong>Movie Genres</strong>
            {currentGenres.length === 0 && <p>None added.</p>}
            {currentGenres.map((genre) => (
              <p key={genre.tmdb_id}>{genre.name}</p>
            ))}
          </div>

          <div>
            <strong>Directors</strong>
            {currentDirectors.length === 0 && <p>None added.</p>}
            {currentDirectors.map((director) => (
              <p key={director.tmdb_id}>{director.name}</p>
            ))}
          </div>
        </section>
      )}

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

        {artistResults.map((artist) => {
          const alreadyAdded = artistAlreadyAdded(artist);

          return (
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
                disabled={isBusy || alreadyAdded}
                onClick={() => handleAddArtist(artist)}
              >
                {alreadyAdded ? "Added" : "Add"}
              </button>
            </div>
          );
        })}
      </section>

      <section>
        <h3>Add Movie Genre</h3>

        <button type="button" onClick={handleLoadGenres} disabled={isBusy}>
          Load Genres
        </button>

        {genreResults.map((genre) => {
          const alreadyAdded = watchItemAlreadyAdded("genre", genre.tmdb_id);

          return (
            <div key={genre.tmdb_id}>
              <strong>{genre.name}</strong>{" "}
              <button
                type="button"
                disabled={isBusy || alreadyAdded}
                onClick={() => handleAddGenre(genre)}
              >
                {alreadyAdded ? "Added" : "Add"}
              </button>
            </div>
          );
        })}
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

        {directorResults.map((director) => {
          const alreadyAdded = watchItemAlreadyAdded(
            "director",
            director.tmdb_id
          );

          return (
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
                disabled={isBusy || alreadyAdded}
                onClick={() => handleAddDirector(director)}
              >
                {alreadyAdded ? "Added" : "Add"}
              </button>
            </div>
          );
        })}
      </section>

      {message && <p>{message}</p>}
    </section>
  );
}