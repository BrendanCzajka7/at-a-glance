import type { UsgsEarthquake } from "../../types/dashboard";
import { formatTime } from "../weather/weatherFormat";

type Props = {
  largest: UsgsEarthquake | null;
  mostSignificant: UsgsEarthquake | null;
  tsunamiEvents: UsgsEarthquake[];
  alertEvents: UsgsEarthquake[];
};

function formatMagnitude(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return value.toFixed(1);
}

function formatDepth(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return `${Math.round(value)} km deep`;
}

function QuakeLine({ quake }: { quake: UsgsEarthquake }) {
  const text = `M${formatMagnitude(quake.magnitude)} · ${
    quake.place ?? "Unknown location"
  } · ${formatTime(quake.event_time)} · ${formatDepth(quake.depth_km)}`;

  return (
    <p>
      {quake.source_url ? (
        <a href={quake.source_url} target="_blank" rel="noreferrer">
          {text}
        </a>
      ) : (
        text
      )}
    </p>
  );
}

export function UsgsEarthToday({
  largest,
  mostSignificant,
  tsunamiEvents,
  alertEvents,
}: Props) {
  if (!largest && !mostSignificant && tsunamiEvents.length === 0) {
    return (
      <section>
        <h3>Earth Today</h3>
        <p>No notable M2.5+ earthquake activity in the current feed.</p>
      </section>
    );
  }

  const showMostSignificant =
    mostSignificant &&
    mostSignificant.source_url !== largest?.source_url;

  return (
    <section>
      <h3>Earth Today</h3>

      {largest && (
        <div>
          <strong>Largest quake, past 24h</strong>
          <QuakeLine quake={largest} />
        </div>
      )}

      {showMostSignificant && mostSignificant && (
        <div>
          <strong>Most significant quake</strong>
          <QuakeLine quake={mostSignificant} />
        </div>
      )}

      {tsunamiEvents.length > 0 && (
        <div>
          <strong>Tsunami-flagged events</strong>
          {tsunamiEvents.map((quake) => (
            <QuakeLine key={quake.source_url ?? quake.title} quake={quake} />
          ))}
        </div>
      )}

      {alertEvents.length > 0 && (
        <div>
          <strong>USGS alert events</strong>
          {alertEvents.map((quake) => (
            <p key={quake.source_url ?? quake.title}>
              {quake.alert?.toUpperCase()} — {quake.title}
            </p>
          ))}
        </div>
      )}
    </section>
  );
}