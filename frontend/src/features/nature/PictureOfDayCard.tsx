import type { Dashboard, NaturePhoto } from "../../types/dashboard";

type Props = {
  nature: Dashboard["nature"];
  nasa: Dashboard["nasa"];
};

function shortDate(value: string | null | undefined) {
  if (!value) return "";

  return new Date(value).toLocaleDateString([], {
    month: "short",
    day: "numeric",
  });
}

function pickNaturePhoto(photos: NaturePhoto[]): NaturePhoto | null {
  if (photos.length === 0) return null;

  return photos[0];
}

function Caption({
  text,
  fallback,
}: {
  text: string | null | undefined;
  fallback?: string;
}) {
  const value = text || fallback;

  if (!value) return null;

  return (
    <details className="caption-details">
      <summary>Caption</summary>
      <p>{value}</p>
    </details>
  );
}

export function PictureOfDayCard({ nature, nasa }: Props) {
  const naturePhoto = pickNaturePhoto(nature.today);
  const apod = nasa.apod;
  const epic = nasa.epic;

  return (
     <div className="picture-card">
      <p className="card-eyebrow">Picture of the Day</p>
      <h2>Nature, space, and Earth</h2>

      <div className="picture-grid">
        <article className="picture-panel">
          <div className="picture-panel__header">
            <div>
              <h3>Nature</h3>
              <small>{naturePhoto?.theme ?? "No photo loaded"}</small>
            </div>
          </div>

          {!naturePhoto && <p>No nature photo ingested yet.</p>}

          {naturePhoto && (
            <>
              <a
                href={naturePhoto.pexels_url ?? naturePhoto.image_url}
                target="_blank"
                rel="noreferrer"
              >
                <img
                  className="picture-image"
                  src={naturePhoto.image_url}
                  alt={naturePhoto.alt ?? naturePhoto.theme}
                />
              </a>

              {naturePhoto.photographer && (
                <p className="picture-credit">
                  Photo by{" "}
                  {naturePhoto.photographer_url ? (
                    <a
                      href={naturePhoto.photographer_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {naturePhoto.photographer}
                    </a>
                  ) : (
                    naturePhoto.photographer
                  )}{" "}
                  on Pexels
                </p>
              )}

              <Caption text={naturePhoto.alt} fallback={naturePhoto.theme} />
            </>
          )}
        </article>

        <article className="picture-panel">
          <div className="picture-panel__header">
            <div>
              <h3>NASA</h3>
              <small>{apod ? shortDate(apod.apod_date) : "No APOD loaded"}</small>
            </div>
          </div>

          {!apod && <p>No NASA APOD data yet.</p>}

          {apod && (
            <>
              {apod.media_type === "image" && apod.image_url ? (
                <a
                  href={apod.hd_image_url ?? apod.image_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  <img
                    className="picture-image"
                    src={apod.image_url}
                    alt={apod.title}
                  />
                </a>
              ) : (
                <div className="picture-placeholder">
                  APOD is not an image today.
                </div>
              )}

              <p className="picture-title">{apod.title}</p>
              <Caption text={apod.explanation} />
            </>
          )}
        </article>

        <article className="picture-panel">
          <div className="picture-panel__header">
            <div>
              <h3>Earth</h3>
              <small>{epic ? shortDate(epic.image_date) : "No EPIC loaded"}</small>
            </div>
          </div>

          {!epic && <p>No NASA EPIC image yet.</p>}

          {epic && (
            <>
              <img
                className="picture-image"
                src={epic.image_url}
                alt={epic.caption ?? "NASA EPIC Earth image"}
              />

              <p className="picture-title">NASA EPIC Earth</p>
              <Caption text={epic.caption} />
            </>
          )}
        </article>
      </div>
    </div>
  );
}