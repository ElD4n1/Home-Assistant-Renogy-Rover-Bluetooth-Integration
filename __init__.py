from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.service import async_register_admin_service
from .renogy_rover import RenogyRover
from .const import SET_CHARGING_MODE_SCHEMA, SET_VOLTAGE_SCHEMA

DOMAIN = "solar_monitor"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    address = entry.data["address"]
    rover = RenogyRover(address)

    await rover.connect()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = rover

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

    entry.async_on_unload(entry.add_update_listener(async_update_entry))
    entry.async_on_unload(rover.disconnect)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    rover = hass.data[DOMAIN].pop(entry.entry_id)
    await rover.disconnect()
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    rover = hass.data[DOMAIN][entry.entry_id]
    await rover.disconnect()
    await rover.connect()

async def set_charging_mode(hass: HomeAssistant, call) -> None:
    """Service to set the charging mode."""
    rover = hass.data[DOMAIN][call.data["entry_id"]]
    mode = call.data["mode"]
    await rover.set_charging_mode(mode)

async def set_voltage(hass: HomeAssistant, call) -> None:
    """Service to set the voltage."""
    rover = hass.data[DOMAIN][call.data["entry_id"]]
    voltage = call.data["voltage"]
    await rover.set_voltage(voltage)