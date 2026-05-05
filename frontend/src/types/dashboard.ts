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
  precipitation_inches: number | null;
  uv_index: number | null;
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
  wind_direction_degrees: number | null;
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

export type TmdbMovieRelease = {
  tmdb_movie_id: number;
  title: string;
  overview: string | null;
  poster_path: string | null;
  release_date: string;
  matched_kind: string;
  matched_name: string;
  source_url: string | null;
};

export type TmdbSection = {
  today: TmdbMovieRelease[];
  week: TmdbMovieRelease[];
  month: TmdbMovieRelease[];
};

export type TicketmasterConcert = {
  name: string;
  event_date: string;
  event_time: string | null;

  venue_name: string | null;
  city: string | null;
  state: string | null;

  genre: string | null;
  sub_genre: string | null;

  image_url: string | null;
  source_url: string | null;
};

export type TicketmasterSection = {
  today: TicketmasterConcert[];
  week: TicketmasterConcert[];
  month: TicketmasterConcert[];
};

export type SpaceLaunch = {
  name: string;
  net: string;

  status_name: string | null;
  mission_name: string | null;

  provider_name: string | null;
  rocket_name: string | null;

  pad_name: string | null;
  location_name: string | null;

  image_url: string | null;
  webcast_url: string | null;
  source_url: string | null;
  flightclub_url: string | null;

  is_crewed: boolean | null;
};

export type SpaceSection = {
  today: SpaceLaunch[];
  week: SpaceLaunch[];
  month: SpaceLaunch[];
};

export type UsgsEarthquake = {
  title: string;
  place: string | null;

  magnitude: number | null;
  event_time: string;

  longitude: number | null;
  latitude: number | null;
  depth_km: number | null;

  tsunami: number | null;
  significance: number | null;
  alert: string | null;
  status: string | null;

  source_url: string | null;
};

export type UsgsSection = {
  largest_today: UsgsEarthquake | null;
  most_significant_today: UsgsEarthquake | null;
  tsunami_events_today: UsgsEarthquake[];
  alert_events_today: UsgsEarthquake[];
};

export type NoaaTidePrediction = {
  station_id: string;
  prediction_time: string;
  tide_type: string | null;
  height_ft: number | null;
};

export type NoaaWeatherAlert = {
  event: string;
  headline: string | null;

  severity: string | null;
  urgency: string | null;
  certainty: string | null;

  effective: string | null;
  expires: string | null;

  description: string | null;
  instruction: string | null;
  source_url: string | null;
};

export type NoaaSpaceWeatherDay = {
  label: string;
  date: string | null;

  radio_blackout_minor_prob: number | null;
  radio_blackout_major_prob: number | null;

  solar_radiation_storm_prob: number | null;

  geomagnetic_scale: string | null;
  geomagnetic_text: string | null;
};

export type NoaaSpaceWeather = {
  fetched_at: string | null;

  current_radio_blackout_scale: string | null;
  current_radio_blackout_text: string | null;

  current_solar_radiation_scale: string | null;
  current_solar_radiation_text: string | null;

  current_geomagnetic_scale: string | null;
  current_geomagnetic_text: string | null;

  forecast_days: NoaaSpaceWeatherDay[];

  alert_count: number;
  recent_alert_titles: string[];
};

export type NoaaSection = {
  tides_today: NoaaTidePrediction[];
  weather_alerts: NoaaWeatherAlert[];
  space_weather: NoaaSpaceWeather | null;
};

export type OceanConditions = {
  station_id: string;
  observed_at: string;
  water_temperature_f: number | null;
  wave_height_ft: number | null;
};

export type OceanSection = {
  current: OceanConditions | null;
};

export type NaturePhoto = {
  photo_date: string;
  theme: string;

  photographer: string | null;
  photographer_url: string | null;

  pexels_url: string | null;
  image_url: string;

  alt: string | null;
  avg_color: string | null;
};

export type NatureSection = {
  today: NaturePhoto[];
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
  tmdb: TmdbSection;
  ticketmaster: TicketmasterSection;
  space: SpaceSection;
  usgs: UsgsSection;
  noaa: NoaaSection;
  ocean: OceanSection;
  nature: NatureSection;
};