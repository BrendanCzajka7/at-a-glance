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
import { NatureThemePicker } from "./NatureThemePicker";
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
  const [hasLoadedCurrent, setHasLoadedCurrent] = useState(false);

  async function refreshCurrentItems() {
    const [artists, watchItems] = await Promise.all([
      listArtists(),
      listTmdbWatchItems(),
    ]);

    setCurrentArtists(artists);
    setCurrentWatchItems(watchItems);
    setHasLoadedCurrent(true);
  }

  async function handleLoadCultureChoices() {
    try {
      setMessage("");
      setIsBusy(true);
      await refreshCurrentItems();
    } catch (err) {
      setMessage(
        err instanceof Error ? err.message : "Failed to load culture choices"
      );
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

      if (!hasLoadedCurrent) {
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

      if (!hasLoadedCurrent) {
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

      if (!hasLoadedCurrent) {
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
    <div>
      <section className="tools-section">
        <NatureThemePicker onChanged={onChanged} />
      </section>

      <section className="tools-section">
        <h3>Culture Choices</h3>

        <button
          type="button"
          onClick={handleLoadCultureChoices}
          disabled={isBusy}
        >
          {hasLoadedCurrent ? "Refresh Choices" : "Load Choices"}
        </button>

        {hasLoadedCurrent && (
          <div className="tools-list">
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
          </div>
        )}
      </section>

      <section className="tools-section">
        <h3>Add Culture</h3>

        <div className="tools-list">
          <div>
            <strong>Add Music Artist</strong>

            <div className="tools-row">
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
            </div>

            <div className="tools-list">
              {artistResults.map((artist) => {
                const alreadyAdded = artistAlreadyAdded(artist);

                return (
                  <div className="tools-result" key={artist.musicbrainz_artist_id}>
                    <div>
                      <strong>{artist.name}</strong>{" "}
                      <small>
                        {artist.type ?? "Artist"}
                        {artist.country ? ` · ${artist.country}` : ""}
                        {artist.disambiguation
                          ? ` · ${artist.disambiguation}`
                          : ""}
                        {artist.score !== null ? ` · score ${artist.score}` : ""}
                      </small>
                    </div>

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
            </div>
          </div>

          <div>
            <strong>Add Movie Genre</strong>

            <div className="tools-row">
              <button type="button" onClick={handleLoadGenres} disabled={isBusy}>
                Load Genres
              </button>
            </div>

            <div className="tools-list">
              {genreResults.map((genre) => {
                const alreadyAdded = watchItemAlreadyAdded(
                  "genre",
                  genre.tmdb_id
                );

                return (
                  <div className="tools-result" key={genre.tmdb_id}>
                    <strong>{genre.name}</strong>

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
            </div>
          </div>

          <div>
            <strong>Add Director</strong>

            <div className="tools-row">
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
            </div>

            <div className="tools-list">
              {directorResults.map((director) => {
                const alreadyAdded = watchItemAlreadyAdded(
                  "director",
                  director.tmdb_id
                );

                return (
                  <div className="tools-result" key={director.tmdb_id}>
                    <div>
                      <strong>{director.name}</strong>{" "}
                      <small>
                        {director.known_for_department ?? "Person"}
                        {director.popularity !== null
                          ? ` · popularity ${Math.round(director.popularity)}`
                          : ""}
                      </small>
                    </div>

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
            </div>
          </div>
        </div>

        {message && <p className="tools-message">{message}</p>}
      </section>

      <section className="tools-section">
        <RecentErrorsPanel />
      </section>
    </div>
  );
}