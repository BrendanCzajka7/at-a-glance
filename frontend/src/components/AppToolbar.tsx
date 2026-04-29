import { useState } from "react";

import {
  addArtist,
  searchArtists,
  type ArtistSearchResult,
} from "../api/music";

type Props = {
  onChanged?: () => void;
};

export function AppToolbar({ onChanged }: Props) {
  const [artistQuery, setArtistQuery] = useState("");
  const [artistResults, setArtistResults] = useState<ArtistSearchResult[]>([]);
  const [message, setMessage] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  async function handleSearch() {
    const query = artistQuery.trim();
    if (!query) return;

    try {
      setMessage("");
      setIsSearching(true);
      setArtistResults(await searchArtists(query));
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Artist search failed");
    } finally {
      setIsSearching(false);
    }
  }

  async function handleAddArtist(artist: ArtistSearchResult) {
    try {
      setMessage("");
      setIsSaving(true);

      await addArtist(artist.name, artist.musicbrainz_artist_id);

      setMessage(`Added ${artist.name}`);
      setArtistQuery("");
      setArtistResults([]);

      onChanged?.();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Add artist failed");
    } finally {
      setIsSaving(false);
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

      <div>
        <h3>Add Music Artist</h3>

        <input
          value={artistQuery}
          onChange={(e) => setArtistQuery(e.target.value)}
          placeholder="Search artist..."
        />

        <button
          type="button"
          onClick={handleSearch}
          disabled={isSearching || !artistQuery.trim()}
        >
          {isSearching ? "Searching..." : "Search"}
        </button>
      </div>

      {artistResults.length > 0 && (
        <div>
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
                disabled={isSaving}
                onClick={() => handleAddArtist(artist)}
              >
                Add
              </button>
            </div>
          ))}
        </div>
      )}

      {message && <p>{message}</p>}
    </section>
  );
}