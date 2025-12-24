"""Config flow for Shinobi Video integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import ShinobiApi
from .const import DOMAIN, CONF_URL, CONF_API_KEY, CONF_GROUP_KEY, CONF_VERIFY_SSL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_GROUP_KEY): cv.string,
        vol.Optional(CONF_VERIFY_SSL, default=True): cv.boolean,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api = ShinobiApi(
        session,
        data[CONF_URL],
        data[CONF_API_KEY],
        data[CONF_GROUP_KEY],
        data.get(CONF_VERIFY_SSL, True),
    )

    try:
        if not await api.test_connection():
            raise CannotConnect
    except Exception as err:
        _LOGGER.error("Connection validation failed: %s", err)
        if "Unauthorized" in str(err) or "Invalid" in str(err) or "Access denied" in str(err):
            raise InvalidAuth
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": "Shinobi Video"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Shinobi Video."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
