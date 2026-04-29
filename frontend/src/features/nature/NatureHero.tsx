import { useMemo, useState } from "react";

import type { NaturePhoto } from "../../types/dashboard";

type Props = {
  photos: NaturePhoto[];
};

export function NatureHero({ photos }: Props) {
  const [selectedTheme, setSelectedTheme] = useState("");

  const selectedPhoto = useMemo(() => {
    if (photos.length === 0) return null;

    if (!selectedTheme) return photos[0];

    return photos.find((photo) => photo.theme === selectedTheme) ?? photos[0];
  }, [photos, selectedTheme]);

  if (photos.length === 0 || !selectedPhoto) {
    return (
      <section>
        <h3>Today on Earth</h3>
        <p>No nature photo ingested yet.</p>
      </section>
    );
  }

  return (
    <section style={{ marginBottom: 16 }}>
      <h3>Today on Earth</h3>

      <select
        value={selectedPhoto.theme}
        onChange={(e) => setSelectedTheme(e.target.value)}
      >
        {photos.map((photo) => (
          <option key={photo.theme} value={photo.theme}>
            {photo.theme}
          </option>
        ))}
      </select>

      <a href={selectedPhoto.pexels_url ?? selectedPhoto.image_url} target="_blank" rel="noreferrer">
        <img
          src={selectedPhoto.image_url}
          alt={selectedPhoto.alt ?? selectedPhoto.theme}
          style={{
            width: "100%",
            maxHeight: 320,
            objectFit: "cover",
            borderRadius: 12,
          }}
        />
      </a>

      <p>
        <strong>{selectedPhoto.theme}</strong>
      </p>

      {selectedPhoto.photographer && (
        <p>
          Photo by{" "}
          {selectedPhoto.photographer_url ? (
            <a href={selectedPhoto.photographer_url} target="_blank" rel="noreferrer">
              {selectedPhoto.photographer}
            </a>
          ) : (
            selectedPhoto.photographer
          )}{" "}
          on Pexels
        </p>
      )}
    </section>
  );
}