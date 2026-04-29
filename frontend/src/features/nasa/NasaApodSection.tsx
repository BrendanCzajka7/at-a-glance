import type { NasaSection } from "../../types/dashboard";

type Props = {
  nasa: NasaSection;
};

export function NasaApodSection({ nasa }: Props) {
  const apod = nasa.apod;

  if (!apod) {
    return (
      <section>
        <h2>NASA</h2>
        <p>No APOD data yet.</p>
      </section>
    );
  }

  return (
    <section>
      <h2>NASA Picture of the Day</h2>

      <h3>{apod.title}</h3>

      {apod.media_type === "image" && apod.image_url && (
        <img
          src={apod.image_url}
          alt={apod.title}
          style={{ maxWidth: 240, height: "auto" }}
        />
      )}

      <p>{apod.explanation}</p>
    </section>
  );
}