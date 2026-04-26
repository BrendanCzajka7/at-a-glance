import httpx


class OpenMeteoClient:
    async def fetch_current_weather(self, latitude: float, longitude: float) -> dict:
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/Chicago",
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()