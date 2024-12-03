from homeassistant.helpers.entity import Entity
from .const import DOMAIN

class RenogyRoverEntity(Entity):
    def __init__(self, config_entry_data: Mapping[str, Any]) -> None:
        self._config_entry_data = config_entry_data

    @property
    def should_poll(self) -> bool:
        return True

    async def async_update(self) -> None:
        """Fetch new state data for the entity."""
        raise NotImplementedError

    async def async_set_charging_mode(self, mode: str) -> None:
        """Set the charging mode."""
        client = self.hass.data[DOMAIN][self._config_entry_data["entry_id"]]
        await client.set_charging_mode(mode)

    async def async_set_voltage(self, voltage: float) -> None:
        """Set the voltage."""
        client = self.hass.data[DOMAIN][self._config_entry_data["entry_id"]]
        await client.set_voltage(voltage)