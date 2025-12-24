from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_STREAM_TYPE

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

    stream_type = entry.data.get(CONF_STREAM_TYPE, "hls")

    entities = []
    for mid, monitor in monitors_dict.items():
        entities.append(ShinobiCamera(coordinator, api, monitor, stream_type))

    async_add_entities(entities)


class ShinobiCamera(CoordinatorEntity, Camera):
    """Representation of a Shinobi Video camera."""

    def __init__(self, coordinator, api, monitor, stream_type) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._api = api
        self._monitor_id = monitor["mid"]
        self._stream_type = stream_type
        self._attr_name = monitor["name"]
        self._attr_unique_id = f"shinobi_{self._monitor_id}"
        self._attr_brand = "Shinobi"
        self._attr_model = monitor.get("type", "Unknown")
        
        if self._stream_type == "hls":
            self._attr_supported_features = CameraEntityFeature.STREAM
        else:
            self._attr_supported_features = CameraEntityFeature(0)

    @property
    def is_recording(self) -> bool:
        """Return true if the device is recording."""
        monitor = self.coordinator.data.get(self._monitor_id)
        if monitor:
            # Shinobi status can be "recording", "watching", etc.
            return monitor.get("status") == "recording"
        return False

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response from the camera."""
        return await self._api.async_get_camera_image(self._monitor_id)

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        if self._stream_type == "hls":
            return self._api.get_stream_url(self._monitor_id, "hls")
        return None
