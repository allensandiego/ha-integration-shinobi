"""Switch platform for Peek (Shinobi Video)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    coordinator = data["coordinator"]

    monitors_dict = coordinator.data
    if not monitors_dict:
        return

    entities = []
    for mid, monitor in monitors_dict.items():
        entities.append(ShinobiRecordingSwitch(coordinator, api, monitor))

    async_add_entities(entities)


class ShinobiRecordingSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Shinobi Recording Switch."""

    def __init__(self, coordinator, api, monitor) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._api = api
        self._monitor_id = monitor["mid"]
        self._attr_name = f"{monitor['name']} Recording"
        self._attr_unique_id = f"shinobi_{self._monitor_id}_recording"

    @property
    def is_on(self) -> bool:
        """Return true if the monitor is in 'record' mode."""
        monitor = self.coordinator.data.get(self._monitor_id)
        if monitor:
            # Mode can be 'record', 'watch', 'stop', 'start'
            return monitor.get("mode") == "record"
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (start recording)."""
        await self._change_mode("record")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (stop recording/change to watch)."""
        # Usually, when turning recording off, we might want to go back to 'watch' mode
        await self._change_mode("watch")

    async def _change_mode(self, mode: str) -> None:
        """Change the monitor mode via API."""
        # Shinobi mode command: /[API_KEY]/monitor/[GROUP_KEY]/[MONITOR_ID]/[MODE]
        url = f"{self._api._url}/{self._api._api_key}/monitor/{self._api._group_key}/{self._monitor_id}/{mode}"
        try:
            response = await self._api._session.get(url)
            if response.status == 200:
                # Force refresh to update the state in HA
                await self.coordinator.async_request_refresh()
        except Exception:
            pass
