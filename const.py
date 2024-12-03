from homeassistant.helpers import config_validation as cv
import voluptuous as vol

DOMAIN = "solar_monitor"

SET_CHARGING_MODE_SCHEMA = vol.Schema({
    vol.Required("entry_id"): cv.string,
    vol.Required("mode"): cv.string,
})

SET_VOLTAGE_SCHEMA = vol.Schema({
    vol.Required("entry_id"): cv.string,
    vol.Required("voltage"): cv.positive_float,
})