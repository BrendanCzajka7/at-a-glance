export function formatTime(value: string | null) {
  if (!value) return "N/A";
  return new Date(value).toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
  });
}

export function formatDate(value: string | null) {
  if (!value) return "N/A";
  return new Date(value).toLocaleDateString();
}

export function weatherCodeLabel(code: number | null) {
  switch (code) {
    case 0:
      return "Clear";
    case 1:
      return "Mostly clear";
    case 2:
      return "Partly cloudy";
    case 3:
      return "Overcast";
    case 45:
    case 48:
      return "Fog";
    case 51:
    case 53:
    case 55:
      return "Drizzle";
    case 61:
      return "Light rain";
    case 63:
      return "Rain";
    case 65:
      return "Heavy rain";
    case 80:
    case 81:
    case 82:
      return "Showers";
    case 95:
      return "Thunderstorm";
    default:
      return "Unknown";
  }
}