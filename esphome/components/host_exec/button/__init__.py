import esphome.codegen as cg
from esphome.components import button
import esphome.config_validation as cv
from esphome.const import CONF_COMMAND

from .. import host_exec_ns

HostExecButton = host_exec_ns.class_(
    "HostExecButton", button.Button, cg.Component
)

CONFIG_SCHEMA = (
    button.button_schema(HostExecButton)
    .extend(
        {
          cv.Required(CONF_COMMAND): cv.string,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    var = await button.new_button(config)
    cg.add(var.set_command(config[CONF_COMMAND]))
    await cg.register_component(var, config)
