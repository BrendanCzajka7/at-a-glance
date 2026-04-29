import type { OceanConditions } from "../../types/dashboard";
import { formatTime } from "../weather/weatherFormat";

type Props = {
  ocean: OceanConditions | null;
};

function formatNumber(value: number | null, suffix: string) {
  if (value === null || value === undefined) return "N/A";
  return `${Math.round(value)}${suffix}`;
}

function formatWave(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return `${value.toFixed(1)} ft`;
}

export function OceanConditionsToday({ ocean }: Props) {
  return (
    <section>
      <h3>Ocean</h3>

      {!ocean && <p>No ocean conditions yet.</p>}

      {ocean && (
        <>
          <p>Water temp: {formatNumber(ocean.water_temperature_f, "°F")}</p>
          <p>Wave height: {formatWave(ocean.wave_height_ft)}</p>
          <small>
            Buoy {ocean.station_id} · Observed {formatTime(ocean.observed_at)}
          </small>
        </>
      )}
    </section>
  );
}