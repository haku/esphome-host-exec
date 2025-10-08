#pragma once

#include "esphome/core/component.h"
#include "esphome/components/button/button.h"
#include "../host_exec.h"

namespace esphome {
namespace host_exec {

class HostExecButton : public button::Button, public Component {

  public:
    void set_command(const std::string &cmd) { this->command_ = cmd; }

  protected:
    void press_action() override {
      run_command(this->command_);
    }

    std::string command_;

};

}  // namespace host_exec
}  // namespace esphome
