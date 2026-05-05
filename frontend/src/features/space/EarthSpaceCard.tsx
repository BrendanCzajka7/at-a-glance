import type { Dashboard, UsgsEarthquake } from "../../types/dashboard";
import { NasaNeoMini } from "../nasa/NasaNeoMini";
import { describeSpaceWeatherDay } from "../noaa/spaceWeatherFormat";
import { SpaceLaunchesMini } from "./SpaceLaunchesMini";
import { formatTime } from "../weather/weatherFormat";

type Props = {
  noaa: Dashboard["noaa"];
  usgs: Dashboard["usgs"];
  nasa: Dashboard["nasa"];
  launches: Dashboard["space"]["today"];
};

function formatMagnitude(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return value.toFixed(1);
}

function QuakeSummary({ quake }: { quake: UsgsEarthquake }) {
  const text = `M${formatMagnitude(quake.magnitude)} · ${
    quake.place ?? "Unknown location"
  }`;

  return (
    <p>
      {quake.source_url ? (
        <a href={quake.source_url} target="_blank" rel="noreferrer">
          {text}
        </a>
      ) : (
        text
      )}
      <small> · {formatTime(quake.event_time)}</small>
    </p>
  );
}

export function EarthSpaceCard({ noaa, usgs, nasa, launches }: Props) {
  const spaceWeather = noaa.space_weather;
  const todaySpaceWeather = spaceWeather?.forecast_days[0] ?? null;

  return (
    <div>
      <p className="card-eyebrow">Earth + Space</p>
      <h2>Signals around the planet</h2>

      <div className="split-card-grid">
        <div>
          <h3>Space Weather</h3>

          {!spaceWeather && <p>No SWPC report ingested yet.</p>}

          {spaceWeather && (
            <>
              <p>
                R{spaceWeather.current_radio_blackout_scale ?? "0"} · S
                {spaceWeather.current_solar_radiation_scale ?? "0"} · G
                {spaceWeather.current_geomagnetic_scale ?? "0"}
              </p>

              {todaySpaceWeather &&
                describeSpaceWeatherDay(todaySpaceWeather).map((line) => (
                  <p key={line}>{line}</p>
                ))}

              <small>{spaceWeather.alert_count} recent SWPC alerts</small>
            </>
          )}
        </div>

        <div>
          <h3>Earthquakes</h3>

          {!usgs.largest_today && !usgs.most_significant_today && (
            <p>No notable M2.5+ earthquake activity.</p>
          )}

          {usgs.largest_today && (
            <>
              <small>Largest past 24h</small>
              <QuakeSummary quake={usgs.largest_today} />
            </>
          )}

          {usgs.alert_events_today.length > 0 && (
            <p>{usgs.alert_events_today.length} USGS alert event(s)</p>
          )}

          {usgs.tsunami_events_today.length > 0 && (
            <p>{usgs.tsunami_events_today.length} tsunami-flagged event(s)</p>
          )}
        </div>

        <div>
          <NasaNeoMini neos={nasa.neos.today} />
        </div>

        <div>
          <SpaceLaunchesMini launches={launches} />
        </div>
      </div>
    </div>
  );
}