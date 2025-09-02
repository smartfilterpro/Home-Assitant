from __future__ import annotations
import secrets
from homeassistant import config_entries
import voluptuous as vol
import aiohttp
from .const import DOMAIN, DEFAULT_API_BASE, CONF_API_BASE, CONF_WEBHOOK_ID

class SmartFilterProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            token = user_input["token"]
            api_base = user_input.get(CONF_API_BASE, DEFAULT_API_BASE).rstrip("/")
            # Validate token by calling /me
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(f"{api_base}/me", headers={"Authorization": f"Bearer {token}"}):
                        pass
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                # Create a HA webhook for push
                webhook_id = secrets.token_hex(16)
                data = {"token": token, "api_base": api_base, CONF_WEBHOOK_ID: webhook_id}
                return self.async_create_entry(title="SmartFilterPro", data=data)

        schema = vol.Schema({
            vol.Required("token"): str,
            vol.Optional(CONF_API_BASE, default=DEFAULT_API_BASE): str
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
