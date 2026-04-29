import type { NasaNeo } from "../../types/dashboard";

type Props = {
  neos: NasaNeo[];
};

function round(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return Math.round(value).toLocaleString();
}

export function NasaNeoMini({ neos }: Props) {
  if (neos.length === 0) {
    return (
      <div>
        <strong>Asteroids</strong>
        <p>None notable</p>
      </div>
    );
  }

  const closest = [...neos].sort(
    (a, b) => (a.miss_distance_lunar ?? 999999) - (b.miss_distance_lunar ?? 999999)
  )[0];

  const largest = [...neos].sort(
    (a, b) =>
      (b.estimated_diameter_max_m ?? 0) - (a.estimated_diameter_max_m ?? 0)
  )[0];

  return (
    <div>
      <strong>Asteroids</strong>
      <p>{neos.length} notable</p>

      {closest && (
        <p>
          Closest: {closest.name}, {round(closest.miss_distance_lunar)} lunar
          distances
        </p>
      )}

      {largest && largest.neo_reference_id !== closest?.neo_reference_id && (
        <p>Largest: {largest.name}, ~{round(largest.estimated_diameter_max_m)} m</p>
      )}
    </div>
  );
}