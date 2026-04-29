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

export type NasaEpic = {
  identifier: string;
  caption: string | null;
  image_date: string;
  image_url: string;
};

export type NasaNeo = {
  neo_reference_id: string;
  name: string;
  nasa_jpl_url: string | null;
  close_approach_date: string;
  close_approach_time: string | null;
  estimated_diameter_max_m: number | null;
  miss_distance_lunar: number | null;
  relative_velocity_kph: number | null;
  is_potentially_hazardous: boolean;
};

export type NasaSection = {
  apod: NasaApod | null;
  epic: NasaEpic | null;
  neos: {
    today: NasaNeo[];
    week: NasaNeo[];
    month: NasaNeo[];
  };
};

export type MusicRelease = {
  artist_name: string;
  title: string;
  release_date: string;
  release_type: string | null;
  source_url: string | null;
};

export type MusicSection = {
  today: MusicRelease[];
  week: MusicRelease[];
  month: MusicRelease[];
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
  music: MusicSection;
};