#pragma once

#include "esphome/core/component.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "../host_exec.h"

namespace esphome {
namespace host_exec {

class HostExecBinarySensor : public PollingComponent, public binary_sensor::BinarySensor {

  public:
    void set_command(const std::string &cmd) { this->command_ = cmd; }

    void update() override {
      std::string output = run_command(this->command_);
      bool state = (output == "1" || output == "true" || output == "on");
      this->publish_state(state);
    }

  protected:
    std::string command_;

};

}  // namespace host_exec
}  // namespace esphome
