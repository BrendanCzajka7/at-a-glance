import type { NasaSection } from "../../types/dashboard";

type Props = {
  nasa: NasaSection;
};

export function NasaEpicSection({ nasa }: Props) {
  const epic = nasa.epic;

  if (!epic) {
    return (
      <section>
        <h3>Earth</h3>
        <p>No EPIC image yet.</p>
      </section>
    );
  }

  return (
    <section>
      <h3>Earth</h3>

      <img
        src={epic.image_url}
        alt={epic.caption ?? "NASA EPIC Earth image"}
        style={{ maxWidth: 180, height: "auto" }}
      />

      {epic.caption && <p>{epic.caption}</p>}
    </section>
  );
}