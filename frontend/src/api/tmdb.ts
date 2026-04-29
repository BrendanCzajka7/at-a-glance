export type TmdbGenreSearchResult = {
  tmdb_id: number;
  name: string;
};

export type TmdbDirectorSearchResult = {
  tmdb_id: number;
  name: string;
  known_for_department: string | null;
  profile_path: string | null;
  popularity: number | null;
};

export type TmdbWatchItem = {
  id: number;
  kind: string;
  tmdb_id: number;
  name: string;
  is_active: boolean;
};

export async function searchTmdbGenres(): Promise<TmdbGenreSearchResult[]> {
  const res = await fetch("/api/tmdb/genre-search");

  if (!res.ok) {
    throw new Error(`TMDB genre search HTTP ${res.status}`);
  }

  return res.json();
}

export async function searchTmdbDirectors(
  name: string
): Promise<TmdbDirectorSearchResult[]> {
  const params = new URLSearchParams({ name });

  const res = await fetch(`/api/tmdb/director-search?${params}`);

  if (!res.ok) {
    throw new Error(`TMDB director search HTTP ${res.status}`);
  }

  return res.json();
}

export async function addTmdbWatchItem(
  kind: "genre" | "director",
  tmdbId: number,
  name: string
): Promise<TmdbWatchItem> {
  const params = new URLSearchParams({
    kind,
    tmdb_id: String(tmdbId),
    name,
    ingest_now: "true",
  });

  const res = await fetch(`/api/tmdb/watch-items?${params}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error(`TMDB add watch item HTTP ${res.status}`);
  }

  return res.json();
}