from datetime import datetime

import httpx


class NoaaClient:
    COOPS_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    NWS_URL = "https://api.weather.gov"
    SWPC_PRODUCTS_URL = "https://services.swpc.noaa.gov/products"
    SWPC_TEXT_URL = "https://services.swpc.noaa.gov/text"

    def __init__(self):
        self.headers = {
            "User-Agent": "AtAGlance/0.1 (contact@example.com)",
            "Accept": "application/json",
        }

    async def fetch_tide_predictions(
        self,
        station_id: str,
        start: datetime,
        end: datetime,
    ) -> list[dict]:
        params = {
            "product": "predictions",
            "application": "AtAGlance",
            "begin_date": start.strftime("%Y%m%d"),
            "end_date": end.strftime("%Y%m%d"),
            "datum": "MLLW",
            "station": station_id,
            "time_zone": "lst_ldt",
            "units": "english",
            "interval": "hilo",
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=20, headers=self.headers) as client:
            response = await client.get(self.COOPS_URL, params=params)
            response.raise_for_status()
            data = response.json()

        return data.get("predictions", [])

    async def fetch_active_weather_alerts(
        self,
        latitude: float,
        longitude: float,
    ) -> list[dict]:
        params = {
            "point": f"{latitude},{longitude}",
        }

        async with httpx.AsyncClient(timeout=20, headers=self.headers) as client:
            response = await client.get(
                f"{self.NWS_URL}/alerts/active",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        return data.get("features", [])

    async def fetch_space_weather_scales(self) -> dict:
        async with httpx.AsyncClient(timeout=20, headers=self.headers) as client:
            response = await client.get(f"{self.SWPC_PRODUCTS_URL}/noaa-scales.json")
            response.raise_for_status()
            return response.json()

    async def fetch_space_weather_alerts(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=20, headers=self.headers) as client:
            response = await client.get(f"{self.SWPC_PRODUCTS_URL}/alerts.json")
            response.raise_for_status()
            data = response.json()

        if isinstance(data, list):
            return data

        return []

    async def fetch_three_day_space_weather_forecast(self) -> str:
        async with httpx.AsyncClient(timeout=20, headers=self.headers) as client:
            response = await client.get(f"{self.SWPC_TEXT_URL}/3-day-forecast.txt")
            response.raise_for_status()
            return response.text