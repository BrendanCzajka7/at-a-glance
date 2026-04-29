import { useState } from "react";

import type { NasaSpaceWeatherCard } from "../../types/dashboard";
import { formatTime } from "../weather/weatherFormat";

type Props = {
  notifications: NasaSpaceWeatherCard[];
};

export function NasaSpaceWeatherToday({ notifications }: Props) {
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <section>
      <h3>Space Weather Today</h3>

      {notifications.length === 0 && <p>No NASA space-weather notices today.</p>}

      {notifications.map((item) => {
        const isOpen = openId === item.message_id;

        return (
          <div key={item.message_id}>
            <button
              type="button"
              onClick={() => setOpenId(isOpen ? null : item.message_id)}
            >
              {item.title}
            </button>

            <small>
              {" "}
              {item.message_type ?? "NASA"} · {formatTime(item.message_issue_time)}
            </small>

            {isOpen && (
              <div>
                <p>{item.summary}</p>

                {item.message_url && (
                  <a href={item.message_url} target="_blank" rel="noreferrer">
                    View NASA notice
                  </a>
                )}
              </div>
            )}
          </div>
        );
      })}
    </section>
  );
}