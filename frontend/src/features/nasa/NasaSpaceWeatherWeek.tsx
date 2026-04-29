import type { NasaSpaceWeatherCard } from "../../types/dashboard";

type Props = {
  notifications: NasaSpaceWeatherCard[];
};

function formatShortDate(value: string) {
  return new Date(value).toLocaleDateString([], {
    month: "short",
    day: "numeric",
  });
}

export function NasaSpaceWeatherWeek({ notifications }: Props) {
  return (
    <section>
      <h3>Space Weather This Week</h3>

      {notifications.length === 0 && (
        <p>No NASA space-weather notices this week.</p>
      )}

      {notifications.map((item) => (
        <div key={item.message_id}>
          <strong>{formatShortDate(item.message_issue_time)}</strong>
          <span>
            {" "}
            — {item.title} {item.message_type ? `(${item.message_type})` : ""}
          </span>
        </div>
      ))}
    </section>
  );
}