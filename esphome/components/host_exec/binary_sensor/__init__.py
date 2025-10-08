import esphome.codegen as cg
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import CONF_COMMAND, CONF_UPDATE_INTERVAL

from .. import host_exec_ns

HostExecBinarySensor = host_exec_ns.class_(
    "HostExecBinarySensor", binary_sensor.BinarySensor, cg.Component
)

CONFIG_SCHEMA = (
    binary_sensor.binary_sensor_schema(HostExecBinarySensor)
    .extend(
        {
          cv.Required(CONF_COMMAND): cv.string,
          cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.update_interval,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    var = await binary_sensor.new_binary_sensor(config)
    await cg.register_component(var, config)

    cg.add(var.set_command(config[CONF_COMMAND]))
