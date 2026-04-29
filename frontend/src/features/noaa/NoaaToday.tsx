import type {
  NoaaSpaceWeather,
  NoaaTidePrediction,
  NoaaWeatherAlert,
} from "../../types/dashboard";
import { formatTime } from "../weather/weatherFormat";

type Props = {
  tides: NoaaTidePrediction[];
  weatherAlerts: NoaaWeatherAlert[];
  spaceWeather: NoaaSpaceWeather | null;
};

function tideLabel(type: string | null) {
  if (type === "H") return "High";
  if (type === "L") return "Low";
  return "Tide";
}

function formatHeight(value: number | null) {
  if (value === null || value === undefined) return "N/A";
  return `${value.toFixed(2)} ft`;
}

export function NoaaToday({ tides, weatherAlerts, spaceWeather }: Props) {
  return (
    <section>
      <h3>NOAA Today</h3>

      <div>
        <strong>Tides</strong>

        {tides.length === 0 && <p>No tide predictions for this location.</p>}

        {tides.map((tide) => (
          <p key={`${tide.station_id}-${tide.prediction_time}-${tide.tide_type}`}>
            {tideLabel(tide.tide_type)} · {formatTime(tide.prediction_time)} ·{" "}
            {formatHeight(tide.height_ft)}
          </p>
        ))}
      </div>

      <div>
        <strong>Local Alerts</strong>

        {weatherAlerts.length === 0 && <p>No active NWS alerts.</p>}

        {weatherAlerts.map((alert) => (
          <details key={`${alert.event}-${alert.effective}-${alert.expires}`}>
            <summary>
              {alert.severity ? `${alert.severity}: ` : ""}
              {alert.event}
            </summary>

            {alert.headline && <p>{alert.headline}</p>}
            {alert.description && <p>{alert.description}</p>}
            {alert.instruction && <p>{alert.instruction}</p>}

            {alert.source_url && (
              <a href={alert.source_url} target="_blank" rel="noreferrer">
                NWS alert
              </a>
            )}
          </details>
        ))}
      </div>

      <div>
        <strong>Space Weather</strong>

        {!spaceWeather && <p>No SWPC report ingested yet.</p>}

        {spaceWeather && (
          <>
            {spaceWeather.current_scales_summary && (
              <p>{spaceWeather.current_scales_summary}</p>
            )}

            {spaceWeather.forecast_summary && (
              <p>{spaceWeather.forecast_summary}</p>
            )}

            {spaceWeather.alert_titles.length > 0 && (
              <ul>
                {spaceWeather.alert_titles.slice(0, 5).map((title) => (
                  <li key={title}>{title}</li>
                ))}
              </ul>
            )}
          </>
        )}
      </div>
    </section>
  );
}