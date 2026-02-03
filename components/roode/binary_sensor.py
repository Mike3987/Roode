import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    CONF_DEVICE_CLASS,
    DEVICE_CLASS_OCCUPANCY,
)
from . import Roode, CONF_ROODE_ID

DEPENDENCIES = ["roode"]

CONF_PRESENCE = "presence_sensor"
TYPES = [CONF_PRESENCE]

# Create a custom binary sensor class for the presence sensor
RoodePresenceBinarySensor = cg.class_(
    "RoodePresenceBinarySensor", binary_sensor.BinarySensor, cg.Component
)

# Use the new schema generator instead of the removed BINARY_SENSOR_SCHEMA
PRESENCE_BINARY_SENSOR_SCHEMA = binary_sensor.binary_sensor_schema(
    RoodePresenceBinarySensor
).extend(
    {
        cv.GenerateID(CONF_ID): cv.declare_id(RoodePresenceBinarySensor),
        cv.Optional(CONF_DEVICE_CLASS): cv.enum(binary_sensor.BINARY_SENSOR_DEVICE_CLASSES),
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ROODE_ID): cv.use_id(Roode),
        cv.Optional(CONF_PRESENCE): PRESENCE_BINARY_SENSOR_SCHEMA,
    }
)

async def setup_conf(config, key, hub):
    if key in config:
        conf = config[key]
        sens = cg.new_Pvariable(conf[CONF_ID])
        # Register as a binary sensor
        await binary_sensor.register_binary_sensor(sens, conf)
        # Attach to the hub using setter
        cg.add(getattr(hub, f"set_{key}_binary_sensor")(sens))

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ROODE_ID])
    for key in TYPES:
        await setup_conf(config, key, hub)
