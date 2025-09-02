from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.components import webhook
from .const import DOMAIN, PLATFORMS, CONF_WEBHOOK_ID
from .coordinator import SmartFilterProCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = SmartFilterProCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Register webhook for push updates (optional but recommended)
    wh_id = entry.data.get(CONF_WEBHOOK_ID)
    if wh_id:
        webhook.async_register(
            hass, DOMAIN, "SmartFilterPro", wh_id, coordinator.async_handle_webhook
        )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_update_listener))
    return True

async def _update_listener(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator: SmartFilterProCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
    wh_id = entry.data.get(CONF_WEBHOOK_ID)
    if wh_id:
        webhook.async_unregister(hass, wh_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok

