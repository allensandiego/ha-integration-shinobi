"""The Shinobi Video integration."""
from __future__ import annotations
from datetime import timedelta

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ShinobiApi
from .const import DOMAIN, CONF_GROUP_KEY, CONF_URL, CONF_API_KEY, CONF_VERIFY_SSL

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "camera", "switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Shinobi Video from a config entry."""
    session = async_get_clientsession(hass)
    api = ShinobiApi(
        session,
        entry.data[CONF_URL],
        entry.data[CONF_API_KEY],
        entry.data[CONF_GROUP_KEY],
        entry.data.get(CONF_VERIFY_SSL, True),
    )

    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            monitors = await api.get_monitors()
            # Shinobi returns a list of monitors. Convert to dict for easier lookup.
            return {monitor["mid"]: monitor for monitor in monitors}
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    # Fetch initial data so we have data when setting up platforms
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
