import type { Location } from "../types/dashboard";

type Props = {
  locations: Location[];
  value: string;
  onChange: (value: string) => void;
};

export function LocationSelect({ locations, value, onChange }: Props) {
  return (
    <label>
      Location:{" "}
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {locations.map((location) => (
          <option key={location.key} value={location.key}>
            {location.name}
          </option>
        ))}
      </select>
    </label>
  );
}