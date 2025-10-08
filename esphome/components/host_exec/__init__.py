import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

host_exec_ns = cg.esphome_ns.namespace("host_exec")
HostExec = host_exec_ns.class_(
    "HostExec", cg.Component
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ID): cv.declare_id(HostExec),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
