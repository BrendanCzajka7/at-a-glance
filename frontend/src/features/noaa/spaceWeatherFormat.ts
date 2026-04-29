import type { NoaaSpaceWeatherDay } from "../../types/dashboard";

export function describeSpaceWeatherDay(day: NoaaSpaceWeatherDay): string[] {
  const lines: string[] = [];

  const minor = day.radio_blackout_minor_prob ?? 0;
  const major = day.radio_blackout_major_prob ?? 0;
  const solar = day.solar_radiation_storm_prob ?? 0;
  const g = day.geomagnetic_scale ?? "0";

  if (minor >= 50) lines.push("Elevated solar flare risk");
  else if (minor >= 20) lines.push("Some solar flare chance");

  if (major >= 10) lines.push("Small chance of stronger flare impacts");

  if (solar >= 10) lines.push("Low radiation storm chance");

  if (g === "0") lines.push("No geomagnetic storm expected");
  else if (g === "1") lines.push("Minor geomagnetic storm possible");
  else lines.push(`Geomagnetic storm risk G${g}`);

  return lines;
}