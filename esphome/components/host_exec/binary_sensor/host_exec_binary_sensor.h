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
      int status = run_status_only(this->command_);
      this->publish_state(status == 0);
    }

  protected:
    std::string command_;

};

}  // namespace host_exec
}  // namespace esphome
