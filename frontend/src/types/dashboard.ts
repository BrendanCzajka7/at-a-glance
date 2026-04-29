export type Location = {
  key: string;
  name: string;
};

export type WeatherCurrent = {
  location_name: string;
  forecast_for: string;
  temperature_f: number | null;
  apparent_temperature_f: number | null;
  wind_speed_mph: number | null;
  wind_gust_mph: number | null;
  wind_direction_degrees: number | null;
  cloud_cover: number | null;
  is_day: number | null;
  weather_code: number | null;
};

export type WeatherHour = {
  forecast_for: string;
  temperature_f: number | null;
  apparent_temperature_f: number | null;
  precipitation_probability: number | null;
  wind_speed_mph: number | null;
  cloud_cover: number | null;
  uv_index: number | null;
  weather_code: number | null;
};

export type WeatherDay = {
  forecast_for: string;
  temperature_max_f: number | null;
  temperature_min_f: number | null;
  precipitation_probability: number | null;
  uv_index: number | null;
  sunrise: string | null;
  sunset: string | null;
  weather_code: number | null;
};

export type NasaApod = {
  apod_date: string;
  title: string;
  explanation: string;
  image_url: string | null;
  hd_image_url: string | null;
  media_type: string;
  copyright: string | null;
};

export type NasaSection = {
  apod: NasaApod | null;
};

export type Dashboard = {
  generated_at: string;
  weather: {
    current: WeatherCurrent | null;
    today: {
      summary: WeatherDay | null;
      hours: WeatherHour[];
    };
    next_hours: WeatherHour[];
    week: {
      days: WeatherDay[];
    };
    month: {
      days: WeatherDay[];
    };
  };
  nasa: NasaSection;
};