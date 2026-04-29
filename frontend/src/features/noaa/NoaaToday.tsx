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
            <p>
                Current: R{spaceWeather.current_radio_blackout_scale ?? "0"} · S
                {spaceWeather.current_solar_radiation_scale ?? "0"} · G
                {spaceWeather.current_geomagnetic_scale ?? "0"}
            </p>

            {spaceWeather.forecast_days[0] && (
                <p>
                Today outlook: R1-R2{" "}
                {spaceWeather.forecast_days[0].radio_blackout_minor_prob ?? 0}%,
                R3-R5{" "}
                {spaceWeather.forecast_days[0].radio_blackout_major_prob ?? 0}%,
                S1+{" "}
                {spaceWeather.forecast_days[0].solar_radiation_storm_prob ?? 0}%,
                G{spaceWeather.forecast_days[0].geomagnetic_scale ?? "0"}
                </p>
            )}

            <p>Recent SWPC alerts: {spaceWeather.alert_count}</p>
            </>
        )}
        </div>
    </section>
  );
}