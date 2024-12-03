from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import DiscoveryInfoType
from .const import DOMAIN

class SolarMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Solar Monitor", data=user_input)
        return self.async_show_form(step_id="user")

    async def async_step_bluetooth(self, discovery_info: DiscoveryInfoType):
        """Handle the Bluetooth discovery step."""
        address = discovery_info.address
        name = discovery_info.name

        # Check if the device is already configured
        await self.async_set_unique_id(address)
        self._abort_if_unique_id_configured()

        # Store the discovered device information
        self.context["title_placeholders"] = {"name": name}

        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={"name": name},
        )

    async def async_step_bluetooth_confirm(self, user_input=None):
        """Handle the Bluetooth confirmation step."""
        if user_input is not None:
            return self.async_create_entry(title=self.context["title_placeholders"]["name"], data=user_input)

        return self.async_show_form(step_id="bluetooth_confirm")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SolarMonitorOptionsFlow(config_entry)

class SolarMonitorOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init")

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up Solar Monitor from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Register Bluetooth discovery callback
    entry.async_on_unload(
        bluetooth.async_register_callback(
            hass,
            _async_discovered_device,
            {"local_name": "SolarMonitor_*"},  # Example matcher
            bluetooth.BluetoothScanningMode.ACTIVE,
        )
    )

@callback
def _async_discovered_device(service_info: bluetooth.BluetoothServiceInfoBleak, change: bluetooth.BluetoothChange):
    """Handle discovered Bluetooth device."""
    hass = service_info.hass
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_BLUETOOTH},
            data=service_info,
        )
    )