import { useState } from "react";

import { fetchRecentAppEvents, type AppEvent } from "../api/appEvents";

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

export function RecentErrorsPanel() {
  const [events, setEvents] = useState<AppEvent[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleToggle() {
    try {
      setMessage("");

      const nextOpen = !isOpen;
      setIsOpen(nextOpen);

      if (!nextOpen) return;

      setIsLoading(true);
      const rows = await fetchRecentAppEvents(25);
      setEvents(rows);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed to load events");
    } finally {
      setIsLoading(false);
    }
  }

  const errors = events.filter((event) => event.level === "error");

  return (
    <div>
      <h3>Debug</h3>

      <button type="button" onClick={handleToggle} disabled={isLoading}>
        {isOpen ? "Hide Debug Info" : "Show Debug Info"}
      </button>

      {isOpen && (
        <div className="tools-list">
          {isLoading && <p>Loading errors...</p>}
          {message && <p className="tools-message">{message}</p>}

          {!isLoading && errors.length === 0 && <p>No recent errors.</p>}

          {errors.map((event) => (
            <details key={event.id}>
              <summary>
                <strong>{event.source}</strong> — {event.message}{" "}
                <small>{formatDate(event.created_at)}</small>
              </summary>

              <p>
                <strong>Type:</strong> {event.event_type}
              </p>

              {event.details && (
                <pre style={{ whiteSpace: "pre-wrap", maxWidth: "100%" }}>
                  {event.details}
                </pre>
              )}
            </details>
          ))}
        </div>
      )}
    </div>
  );
}