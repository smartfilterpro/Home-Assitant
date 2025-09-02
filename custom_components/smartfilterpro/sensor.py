from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

SENSORS = {
    "filter_life_pct": ("Filter Life", "%"),
    "runtime_hours": ("Runtime", "h"),
    "next_change": ("Next Change", None),
    "hvac_status": ("HVAC Status", None),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for device_id in coordinator.data or {}:
        for key, (name, unit) in SENSORS.items():
            entities.append(SmartFilterProSensor(coordinator, device_id, key, name, unit))
    async_add_entities(entities)

class SmartFilterProSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, device_id, key, name, unit):
        super().__init__(coordinator)
        self._device_id = device_id
        self._key = key
        self._attr_name = f"SmartFilterPro {name} ({device_id[-6:]})"
        self._attr_unique_id = f"{DOMAIN}_{device_id}_{key}"
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self._device_id, {}).get(self._key)
