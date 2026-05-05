import type { Dashboard } from "../../types/dashboard";

type Props = {
  nasa: Dashboard["nasa"];
};

export function NasaImagesCard({ nasa }: Props) {
  const apod = nasa.apod;
  const epic = nasa.epic;

  return (
    <div>
      <p className="card-eyebrow">NASA Images</p>
      <h2>Picture of the day</h2>

      <div className="nasa-image-grid">
        <div>
          {!apod && <p>No APOD data yet.</p>}

          {apod && (
            <>
              <h3>{apod.title}</h3>

              {apod.media_type === "image" && apod.image_url && (
                <a href={apod.hd_image_url ?? apod.image_url} target="_blank" rel="noreferrer">
                  <img
                    className="feature-image"
                    src={apod.image_url}
                    alt={apod.title}
                  />
                </a>
              )}

              <p className="clamped-text">{apod.explanation}</p>
            </>
          )}
        </div>

        <div>
          <h3>Earth</h3>

          {!epic && <p>No EPIC image yet.</p>}

          {epic && (
            <>
              <img
                className="feature-image feature-image--small"
                src={epic.image_url}
                alt={epic.caption ?? "NASA EPIC Earth image"}
              />

              {epic.caption && <p>{epic.caption}</p>}
            </>
          )}
        </div>
      </div>
    </div>
  );
}