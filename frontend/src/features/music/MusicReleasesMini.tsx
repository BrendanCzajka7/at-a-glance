import type { MusicRelease } from "../../types/dashboard";

type Props = {
  releases: MusicRelease[];
};

export function MusicReleasesMini({ releases }: Props) {
  if (releases.length === 0) {
    return (
      <div>
        <strong>Music</strong>
        <p>No releases</p>
      </div>
    );
  }

  return (
    <div>
      <strong>Music</strong>

      {releases.map((release) => (
        <p key={`${release.artist_name}-${release.title}-${release.release_date}`}>
          {release.artist_name}: {release.title}
        </p>
      ))}
    </div>
  );
}