from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.service import async_register_admin_service

DOMAIN = "solar_monitor"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    # Register services
    async_register_admin_service(
        hass,
        DOMAIN,
        "set_charging_mode",
        set_charging_mode,
        schema=SET_CHARGING_MODE_SCHEMA,
    )
    async_register_admin_service(
        hass,
        DOMAIN,
        "set_voltage",
        set_voltage,
        schema=SET_VOLTAGE_SCHEMA,
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

async def set_charging_mode(hass: HomeAssistant, call) -> None:
    """Service to set the charging mode."""
    client = hass.data[DOMAIN][call.data["entry_id"]]
    mode = call.data["mode"]
    await client.set_charging_mode(mode)

async def set_voltage(hass: HomeAssistant, call) -> None:
    """Service to set the voltage."""
    client = hass.data[DOMAIN][call.data["entry_id"]]
    voltage = call.data["voltage"]
    await client.set_voltage(voltage)