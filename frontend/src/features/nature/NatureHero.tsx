import type { NaturePhoto } from "../../types/dashboard";

type Props = {
  photo: NaturePhoto | null;
};

export function NatureHero({ photo }: Props) {
  if (!photo) return null;

  return (
    <section style={{ marginBottom: 16 }}>
      <h2>Today on Earth</h2>

      <a href={photo.pexels_url ?? photo.image_url} target="_blank" rel="noreferrer">
        <img
          src={photo.image_url}
          alt={photo.alt ?? photo.theme}
          style={{
            width: "100%",
            maxHeight: 320,
            objectFit: "cover",
            borderRadius: 12,
          }}
        />
      </a>

      <p>
        <strong>{photo.theme}</strong>
      </p>

      {photo.photographer && (
        <p>
          Photo by{" "}
          {photo.photographer_url ? (
            <a href={photo.photographer_url} target="_blank" rel="noreferrer">
              {photo.photographer}
            </a>
          ) : (
            photo.photographer
          )}{" "}
          on Pexels
        </p>
      )}
    </section>
  );
}