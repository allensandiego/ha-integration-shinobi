from homeassistant.components.camera import Camera
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
        self._attr_name = monitor["name"]
        self._attr_unique_id = f"shinobi_{self._monitor_id}"

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
        url = self._api.get_snapshot_url(self._monitor_id)
        try:
            response = await self._api._session.get(url)
            if response.status == 200:
                return await response.read()
        except Exception:
            pass
        return None

    async def stream_source(self) -> str | None:
        """Return the source of the stream."""
        return self._api.get_stream_url(self._monitor_id)
