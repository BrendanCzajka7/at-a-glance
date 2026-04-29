import type { SpaceLaunch } from "../../types/dashboard";
import { formatTime } from "../weather/weatherFormat";

type Props = {
  launches: SpaceLaunch[];
};

export function SpaceLaunchesMini({ launches }: Props) {
  if (launches.length === 0) {
    return (
      <div>
        <strong>Launches</strong>
        <p>No launches</p>
      </div>
    );
  }

  return (
    <div>
      <strong>Launches</strong>

      {launches.map((launch) => (
        <div key={`${launch.name}-${launch.net}`}>
          <p>
            {launch.source_url ? (
              <a href={launch.source_url} target="_blank" rel="noreferrer">
                {launch.name}
              </a>
            ) : (
              launch.name
            )}
          </p>

          <small>
            {formatTime(launch.net)}
            {launch.provider_name ? ` · ${launch.provider_name}` : ""}
            {launch.location_name ? ` · ${launch.location_name}` : ""}
            {launch.status_name ? ` · ${launch.status_name}` : ""}
          </small>
        </div>
      ))}
    </div>
  );
}