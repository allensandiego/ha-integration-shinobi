"""Switch platform for Shinobi Video."""
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
        self._attr_icon = "mdi:record-rec"

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
        if await self._api.async_change_mode(self._monitor_id, "record"):
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (set to watch/stop)."""
        # We default to 'watch' when turning off recording
        if await self._api.async_change_mode(self._monitor_id, "watch"):
            await self.coordinator.async_request_refresh()
