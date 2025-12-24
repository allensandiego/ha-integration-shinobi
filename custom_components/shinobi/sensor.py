from typing import Any
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import logging
from .const import DOMAIN

_LOGGER = logging.getLogger("Shinobi Video")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    monitors_dict = coordinator.data
    if not monitors_dict:
        _LOGGER.warning("No monitors found to set up sensor entities")
        return

    _LOGGER.debug("Setting up %d sensor entities", len(monitors_dict))

    entities = []
    for mid, monitor in monitors_dict.items():
        entities.append(ShinobiStatusSensor(coordinator, monitor))

    async_add_entities(entities)


class ShinobiStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Shinobi Monitor Status sensor."""

    def __init__(self, coordinator, monitor) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._monitor_id = monitor["mid"]
        self._attr_name = f"{monitor['name']} Status"
        self._attr_unique_id = f"shinobi_{self._monitor_id}_status"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        monitor = self.coordinator.data.get(self._monitor_id)
        if monitor:
            return monitor.get("status")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        monitor = self.coordinator.data.get(self._monitor_id)
        if monitor:
            extra_attributes = {
                "mid": monitor.get("mid"),
                "type": monitor.get("type"),
                "mode": monitor.get("mode"),
            }
            
            streams = monitor.get("streams", [])
            if streams and isinstance(streams, list):
                extra_attributes["stream_url"] = streams[0]
            
            return extra_attributes
        return {}
