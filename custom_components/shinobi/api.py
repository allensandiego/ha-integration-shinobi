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
        verify_ssl: bool = True,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"
        self._url = url.rstrip("/")
        self._api_key = api_key
        self._group_key = group_key
        self._verify_ssl = verify_ssl
        _LOGGER.debug("Initialized Shinobi API client for %s", self._url)

    async def test_connection(self) -> bool:
        """Test the connection to Shinobi."""
        _LOGGER.debug("Testing connection to Shinobi URL: %s", self._url)
        try:
            # We just try to fetch the monitors list to verify credentials
            await self.get_monitors()
            _LOGGER.info("Successfully connected to Shinobi Video at %s", self._url)
            return True
        except Exception as err:
            _LOGGER.error("Failed to connect to Shinobi: %s", err)
            return False

    async def get_monitors(self) -> list[dict]:
        """Get the list of monitors from Shinobi."""
        url = f"{self._url}/{self._api_key}/monitor/{self._group_key}"
        _LOGGER.debug("Fetching monitors from: %s", url)
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(url, ssl=None if self._verify_ssl else False)
                
                if response.status == 401:
                    raise Exception("Invalid API Key or Group Key (Unauthorized)")
                if response.status == 403:
                    raise Exception("Access denied (Forbidden). Check API Key restrictions.")
                
                response.raise_for_status()
                
                # Check content type to ensure it's JSON
                if "application/json" not in response.headers.get("content-type", "").lower():
                    text = await response.text()
                    _LOGGER.error("Expected JSON but got: %s", text[:100])
                    raise Exception("Server did not return JSON. Check the URL.")

                data = await response.json()
                
                # Shinobi might return {"success": false, "msg": "..."} instead of status error
                if isinstance(data, dict) and data.get("success") is False:
                    _LOGGER.error("Shinobi API error: %s", data.get("msg", "Unknown error"))
                    raise Exception(data.get("msg", "Unauthorized"))
                
                if not isinstance(data, list):
                    _LOGGER.warning("Shinobi API returned non-list data: %s", data)
                    return []
                
                _LOGGER.debug("Found %d monitors", len(data))
                return data
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout connecting to Shinobi at %s", self._url)
            raise Exception("Connection timed out. Check the URL and network.")
        except aiohttp.ClientConnectorError as err:
            _LOGGER.error("Connection error: %s", err)
            raise Exception(f"Failed to connect: {err}")
        except Exception as err:
            _LOGGER.error("Error fetching monitors: %s", err)
            raise

    def get_snapshot_url(self, monitor_id: str) -> str:
        """Get the snapshot URL for a monitor."""
        return f"{self._url}/{self._api_key}/jpeg/{self._group_key}/{monitor_id}/s.jpg"

    def get_mjpeg_stream_coro(self, monitor_id: str, stream_url: str):
        """Return the coroutine for the MJPEG stream."""
        url = self.get_stream_url(monitor_id, stream_url)
        return self._session.get(url, ssl=None if self._verify_ssl else False)

    def get_stream_url(self, monitor_id: str, stream_url: str | None = None) -> str:
        """Get the stream URL for a monitor. Use stream_url if available."""
        _LOGGER.info("Generating stream URL for monitor %s. Provided URL: %s", monitor_id, stream_url)
        
        if stream_url:
            if stream_url.startswith("/"):
                res = f"{self._url}{stream_url}"
            else:
                res = stream_url
        else:
            # Fallback to default HLS path if no stream_url provided
            res = f"{self._url}/{self._api_key}/hls/{self._group_key}/{monitor_id}/index.m3u8"
            
        _LOGGER.info("Final stream URL for %s: %s", monitor_id, res)
        return res

    async def async_get_camera_image(self, monitor_id: str) -> bytes | None:
        """Fetch a still image from the camera."""
        url = self.get_snapshot_url(monitor_id)
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(url, ssl=None if self._verify_ssl else False)
                if response.status == 200:
                    return await response.read()
        except Exception as err:
            _LOGGER.error("Error fetching camera image for %s: %s", monitor_id, err)
        return None

    async def async_change_mode(self, monitor_id: str, mode: str) -> bool:
        """Change the monitor mode."""
        url = f"{self._url}/{self._api_key}/monitor/{self._group_key}/{monitor_id}/{mode}"
        _LOGGER.info("Changing mode for monitor %s to %s", monitor_id, mode)
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(url, ssl=None if self._verify_ssl else False)
                if response.status == 200:
                    _LOGGER.info("Successfully changed mode for monitor %s to %s", monitor_id, mode)
                    return True
                _LOGGER.error("Error changing mode for %s to %s: HTTP %s", monitor_id, mode, response.status)
        except Exception as err:
            _LOGGER.error("Exception while changing mode for %s to %s: %s", monitor_id, mode, err)
        return False

