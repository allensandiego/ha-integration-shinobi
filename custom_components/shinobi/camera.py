from typing import Any
from homeassistant.components.camera import Camera, CameraEntityFeature
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
    """Set up the camera platform."""
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    coordinator = data["coordinator"]

    monitors_dict = coordinator.data
    if not monitors_dict:
        return

    entities = []
    for mid, monitor in monitors_dict.items():
        entities.append(ShinobiCamera(coordinator, api, monitor))

    async_add_entities(entities)


class ShinobiCamera(CoordinatorEntity, Camera):
    """Representation of a Shinobi Video camera."""

    def __init__(self, coordinator, api, monitor) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._api = api
        self._monitor_id = monitor["mid"]
        
        # Derive stream_type from details.stream_type in the JSON response
        details = monitor.get("details", {})
        if isinstance(details, str):
            import json
            try:
                details = json.loads(details)
            except:
                details = {}
        
        self._stream_type = details.get("stream_type", "hls")
        
        self._attr_name = monitor["name"]
        self._attr_unique_id = f"shinobi_{self._monitor_id}"
        self._attr_brand = "Shinobi"
        self._attr_model = monitor.get("type", "Unknown")
        
        if self._stream_type == "hls":
            self._attr_supported_features = CameraEntityFeature.STREAM
        else:
            self._attr_supported_features = CameraEntityFeature(0)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        monitor = self.coordinator.data.get(self._monitor_id)
        if monitor:
            extra_attributes = {
                "mid": monitor.get("mid"),
                "type": monitor.get("type"),
            }
            
            # Derive stream_url similar to sensor.py
            streams = monitor.get("streams", [])
            if streams and isinstance(streams, list):
                extra_attributes["stream_url"] = streams[0]
            
            return extra_attributes
        return {}

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        monitor = self.coordinator.data.get(self._monitor_id)
        if monitor:
            return monitor.get("mode") == "record"
        return False

    @property
    def is_on(self) -> bool:
        """Return true if the camera is active."""
        return True

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response from the camera."""
        return await self._api.async_get_camera_image(self._monitor_id)

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if self._stream_type == "hls":
            monitor = self.coordinator.data.get(self._monitor_id)
            stream_url = None
            if monitor and monitor.get("streams"):
                stream_url = monitor["streams"][0]
            
            return self._api.get_stream_url(self._monitor_id, stream_url)
        return None
