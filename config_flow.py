from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from typing import Optional, Dict, Any

class SolarMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> config_entries.FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="Solar Monitor", data=user_input)
        return self.async_show_form(step_id="user")