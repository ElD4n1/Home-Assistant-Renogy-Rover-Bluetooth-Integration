from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import DiscoveryInfoType
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    scanner = bluetooth.async_get_scanner(hass)
    scanner.async_register_callback(
        _async_discovered_device,
        {"address": entry.data["address"]},
        bluetooth.BluetoothScanningMode.ACTIVE,
    )
    return True

@callback
def _async_discovered_device(service_info: DiscoveryInfoType, change: bluetooth.BluetoothChange) -> None:
    _LOGGER.info("Discovered device: %s", service_info)