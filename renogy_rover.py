import logging
from bleak import BleakClient

_LOGGER = logging.getLogger(__name__)


def Bytes2Int(bytes_val: bytes) -> int:
    """Convert bytes to an integer."""
    return int.from_bytes(bytes_val, byteorder='big')


def Int2Bytes(value: int, length: int) -> bytes:
    """Convert an integer to bytes."""
    return value.to_bytes(length, byteorder='big')


class RenogyRover:
    def __init__(self, address: str) -> None:
        self.address = address
        self.client = BleakClient(address)

    async def connect(self) -> None:
        """Connect to the Renogy Rover via Bluetooth."""
        await self.client.connect()
        _LOGGER.info("Connected to Renogy Rover at %s", self.address)

    async def disconnect(self) -> None:
        """Disconnect from the Renogy Rover."""
        await self.client.disconnect()
        _LOGGER.info("Disconnected from Renogy Rover")

    async def read_characteristic(self, uuid: str) -> bytes:
        """Read a characteristic from the Renogy Rover."""
        if not self.client.is_connected:
            raise ConnectionError("Not connected to Renogy Rover")

        response = await self.client.read_gatt_char(uuid)
        return response

    async def write_characteristic(self, uuid: str, data: bytes) -> None:
        """Write a characteristic to the Renogy Rover."""
        if not self.client.is_connected:
            raise ConnectionError("Not connected to Renogy Rover")

        await self.client.write_gatt_char(uuid, data)

    async def solar_voltage(self) -> float:
        """Get the solar voltage."""
        uuid = "00002a19-0000-1000-8000-00805f9b34fb"  # Example UUID
        response = await self.read_characteristic(uuid)
        voltage = self.parse_voltage(response)
        return voltage

    async def solar_current(self) -> float:
        """Get the solar current."""
        uuid = "00002a1c-0000-1000-8000-00805f9b34fb"  # Example UUID
        response = await self.read_characteristic(uuid)
        current = self.parse_current(response)
        return current

    async def solar_power(self) -> float:
        """Get the solar power."""
        voltage = await self.solar_voltage()
        current = await self.solar_current()
        power = voltage * current
        return power

    async def battery_voltage(self) -> float:
        """Get the battery voltage."""
        uuid = "00002a1d-0000-1000-8000-00805f9b34fb"  # Example UUID
        response = await self.read_characteristic(uuid)
        voltage = self.parse_voltage(response)
        return voltage

    async def power_generation_today(self) -> float:
        """Get the energy production today."""
        uuid = "00002a1e-0000-1000-8000-00805f9b34fb"  # Example UUID
        response = await self.read_characteristic(uuid)
        energy = self.parse_energy(response)
        return energy

    async def controller_temperature(self) -> float:
        """Get the controller temperature."""
        uuid = "00002a1f-0000-1000-8000-00805f9b34fb"  # Example UUID
        response = await self.read_characteristic(uuid)
        temperature = self.parse_temperature(response)
        return temperature

    async def charging_status_label(self) -> str:
        """Get the charging status."""
        uuid = "00002a20-0000-1000-8000-00805f9b34fb"  # Example UUID
        response = await self.read_characteristic(uuid)
        status = self.parse_status(response)
        return status

    async def set_charging_mode(self, mode: str) -> None:
        """Set the charging mode of the Renogy Rover."""
        uuid = "00002a21-0000-1000-8000-00805f9b34fb"  # Example UUID
        command = self.build_set_mode_command(mode)
        await self.write_characteristic(uuid, command)
        _LOGGER.info("Set charging mode to %s", mode)

    async def set_voltage(self, voltage: float) -> None:
        """Set the voltage of the Renogy Rover."""
        uuid = "00002a22-0000-1000-8000-00805f9b34fb"  # Example UUID
        command = self.build_set_voltage_command(voltage)
        await self.write_characteristic(uuid, command)
        _LOGGER.info("Set voltage to %.2f", voltage)

    def parse_voltage(self, response: bytes) -> float:
        """Parse the voltage from the response."""
        voltage_int = Bytes2Int(response)
        voltage = voltage_int / 100.0  # Example conversion
        return voltage

    def parse_current(self, response: bytes) -> float:
        """Parse the current from the response."""
        current_int = Bytes2Int(response)
        current = current_int / 100.0  # Example conversion
        return current

    def parse_energy(self, response: bytes) -> float:
        """Parse the energy from the response."""
        energy_int = Bytes2Int(response)
        energy = energy_int / 100.0  # Example conversion
        return energy

    def parse_temperature(self, response: bytes) -> float:
        """Parse the temperature from the response."""
        temperature_int = Bytes2Int(response)
        temperature = temperature_int / 100.0  # Example conversion
        return temperature

    def parse_status(self, response: bytes) -> str:
        """Parse the status from the response."""
        status_int = Bytes2Int(response)
        status = self.status_int_to_label(status_int)
        return status

    def build_set_mode_command(self, mode: str) -> bytes:
        """Build the command to set the charging mode."""
        mode_int = self.mode_label_to_int(mode)
        command = Int2Bytes(mode_int, 2)  # Example length
        return command

    def build_set_voltage_command(self, voltage: float) -> bytes:
        """Build the command to set the voltage."""
        voltage_int = int(voltage * 100)  # Example conversion
        command = Int2Bytes(voltage_int, 2)  # Example length
        return command

    def status_int_to_label(self, status_int: int) -> str:
        """Convert status integer to label."""
        return STATUS_MAPPING.get(status_int, "Unknown")

    # TODO not sure if mode == status
    def mode_label_to_int(self, mode: str) -> int:
        """Convert mode label to integer."""

        return MODE_MAPPING.get(mode, 0)


STATUS_MAPPING = {
    0: "Deactivated",
    1: "Activated",
    2: "Mppt",
    3: "Equalizing",
    4: "Boost",
    5: "Floating",
    6: "Current limiting"
}

MODE_MAPPING = {
    "Deactivated": 0,
    "Activated": 1,
    "Mppt": 2,
    "Equalizing": 3,
    "Boost": 4,
    "Floating": 5,
    "Current limiting": 6
}
