export type ArtistSearchResult = {
  musicbrainz_artist_id: string;
  name: string;
  sort_name: string | null;
  country: string | null;
  disambiguation: string | null;
  score: number | null;
  type: string | null;
};

export type MusicArtist = {
  id: number;
  name: string;
  musicbrainz_artist_id: string;
  is_active: boolean;
};

export async function searchArtists(
  name: string
): Promise<ArtistSearchResult[]> {
  const params = new URLSearchParams({ name });

  const res = await fetch(`/api/music/artist-search?${params}`);

  if (!res.ok) {
    throw new Error(`Artist search HTTP ${res.status}`);
  }

  return res.json();
}

export async function addArtist(
  name: string,
  musicbrainzArtistId: string
): Promise<MusicArtist> {
  const params = new URLSearchParams({
    name,
    musicbrainz_artist_id: musicbrainzArtistId,
  });

  const res = await fetch(`/api/music/artists?${params}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error(`Add artist HTTP ${res.status}`);
  }

  return res.json();
}