import type { MusicRelease } from "../../types/dashboard";

type Props = {
  title: string;
  releases: MusicRelease[];
};

function formatDate(value: string) {
  return new Date(value).toLocaleDateString([], {
    month: "short",
    day: "numeric",
  });
}

export function MusicReleasesSection({ title, releases }: Props) {
  return (
    <section>
      <h3>{title}</h3>

      {releases.length === 0 && <p>No upcoming releases.</p>}

      {releases.map((release) => (
        <div
          key={`${release.artist_name}-${release.title}-${release.release_date}`}
        >
          <strong>{release.artist_name}</strong>
          <p>
            {release.title} — {formatDate(release.release_date)}
          </p>

          {release.release_type && <small>{release.release_type}</small>}

          {release.source_url && (
            <p>
              <a href={release.source_url} target="_blank" rel="noreferrer">
                MusicBrainz
              </a>
            </p>
          )}
        </div>
      ))}
    </section>
  );
}