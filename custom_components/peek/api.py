"""API Client for Shinobi Video."""
from __future__ import annotations

import asyncio
import logging
import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)


class ShinobiApi:
    """Shinobi Video API client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        api_key: str,
        group_key: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._url = url.rstrip("/")
        self._api_key = api_key
        self._group_key = group_key

    async def test_connection(self) -> bool:
        """Test the connection to Shinobi."""
        try:
            # We just try to fetch the monitors list to verify credentials
            await self.get_monitors()
            return True
        except Exception as err:
            _LOGGER.error("Failed to connect to Shinobi: %s", err)
            return False

    async def get_monitors(self) -> list[dict]:
        """Get the list of monitors from Shinobi."""
        url = f"{self._url}/{self._api_key}/monitor/{self._group_key}"
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(url)
                response.raise_for_status()
                data = await response.json()
                
                # Shinobi might return {"success": false, "msg": "..."} instead of status error
                if isinstance(data, dict) and data.get("success") is False:
                    _LOGGER.error("Shinobi API error: %s", data.get("msg", "Unknown error"))
                    raise Exception(data.get("msg", "Unauthorized"))
                
                return data if isinstance(data, list) else []
        except Exception as err:
            _LOGGER.error("Error fetching monitors: %s", err)
            raise

    def get_snapshot_url(self, monitor_id: str) -> str:
        """Get the snapshot URL for a monitor."""
        return f"{self._url}/{self._api_key}/jpeg/{self._group_key}/{monitor_id}/s.jpg"

    def get_mjpeg_url(self, monitor_id: str) -> str:
        """Get the MJPEG stream URL for a monitor."""
        return f"{self._url}/{self._api_key}/mjpeg/{self._group_key}/{monitor_id}"

    def get_stream_url(self, monitor_id: str, stream_type: str = "hls") -> str:
        """Get the stream URL for a monitor."""
        if stream_type == "hls":
            return f"{self._url}/{self._api_key}/hls/{self._group_key}/{monitor_id}/s.m3u8"
        return self.get_mjpeg_url(monitor_id)
