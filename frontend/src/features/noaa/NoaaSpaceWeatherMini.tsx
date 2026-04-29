// frontend/src/features/noaa/NoaaSpaceWeatherMini.tsx

import type { NoaaSpaceWeatherDay } from "../../types/dashboard";

type Props = {
  day: NoaaSpaceWeatherDay | null;
};

export function NoaaSpaceWeatherMini({ day }: Props) {
  if (!day) return null;

  return (
    <div>
      <strong>Space Weather</strong>
      <p>
        R1-R2 {day.radio_blackout_minor_prob ?? 0}% · R3-R5{" "}
        {day.radio_blackout_major_prob ?? 0}% · S1+{" "}
        {day.solar_radiation_storm_prob ?? 0}% · G
        {day.geomagnetic_scale ?? "0"}
      </p>
    </div>
  );
}