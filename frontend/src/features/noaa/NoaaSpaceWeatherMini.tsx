import type { NoaaSpaceWeatherDay } from "../../types/dashboard";
import { describeSpaceWeatherDay } from "./spaceWeatherFormat";

type Props = {
  day: NoaaSpaceWeatherDay | null;
};

export function NoaaSpaceWeatherMini({ day }: Props) {
  if (!day) return null;

  const lines = describeSpaceWeatherDay(day);

  return (
    <div>
      <strong>Space Weather</strong>
      {lines.map((line) => (
        <p key={line}>{line}</p>
      ))}
    </div>
  );
}