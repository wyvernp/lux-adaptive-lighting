import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import entity_registry

from .const import DOMAIN

class LuxAdaptiveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    # Temporary variables to store the values during the configuration process
    sensor = None
    light = None
    target_lux = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # Start with sensor selection
        return await self.async_step_select_sensor()

    async def async_step_select_sensor(self, user_input=None):
        """Handle sensor selection."""
        if user_input is not None:
            self.sensor = user_input["sensor"]
            return await self.async_step_select_light()

        registry = await entity_registry.async_get_registry(self.hass)
        sensors = [
            entity.entity_id
            for entity in registry.entities.values()
            if entity.domain == "sensor"
        ]
        return self.async_show_form(
            step_id="select_sensor",
            data_schema=vol.Schema({
                vol.Required("sensor"): vol.In(sensors)
            })
        )

    async def async_step_select_light(self, user_input=None):
        """Handle light selection."""
        if user_input is not None:
            self.light = user_input["light"]
            return await self.async_step_set_lux()

        registry = await entity_registry.async_get_registry(self.hass)
        lights = [
            entity.entity_id
            for entity in registry.entities.values()
            if entity.domain == "light"
        ]
        return self.async_show_form(
            step_id="select_light",
            data_schema=vol.Schema({
                vol.Required("light"): vol.In(lights)
            })
        )

    async def async_step_set_lux(self, user_input=None):
        """Handle lux value input."""
        if user_input is not None:
            self.target_lux = user_input["target_lux"]
            return self.async_create_entry(
                title=f"Mapping for {self.sensor}",
                data={
                    "sensor": self.sensor,
                    "light": self.light,
                    "target_lux": self.target_lux
                }
            )

        return self.async_show_form(
            step_id="set_lux",
            data_schema=vol.Schema({
                vol.Required("target_lux"): int
            })
        )
