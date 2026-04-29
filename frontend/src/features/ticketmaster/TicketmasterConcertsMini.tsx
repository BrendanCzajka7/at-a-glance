import type { TicketmasterConcert } from "../../types/dashboard";

type Props = {
  concerts: TicketmasterConcert[];
};

function formatTime(value: string | null) {
  if (!value) return "";

  const [hourRaw, minute] = value.split(":");
  const hour = Number(hourRaw);

  if (Number.isNaN(hour)) return value;

  const suffix = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;

  return `${displayHour}:${minute} ${suffix}`;
}

export function TicketmasterConcertsMini({ concerts }: Props) {
  if (concerts.length === 0) {
    return (
      <div>
        <strong>Concerts</strong>
        <p>No concerts</p>
      </div>
    );
  }

  return (
    <div>
      <strong>Concerts</strong>

      {concerts.map((concert) => (
        <div key={`${concert.name}-${concert.event_date}-${concert.venue_name}`}>
          <p>
            {concert.source_url ? (
              <a href={concert.source_url} target="_blank" rel="noreferrer">
                {concert.name}
              </a>
            ) : (
              concert.name
            )}
          </p>

          <small>
            {formatTime(concert.event_time)}
            {concert.venue_name ? ` · ${concert.venue_name}` : ""}
            {concert.city ? ` · ${concert.city}` : ""}
            {concert.state ? `, ${concert.state}` : ""}
          </small>
        </div>
      ))}
    </div>
  );
}