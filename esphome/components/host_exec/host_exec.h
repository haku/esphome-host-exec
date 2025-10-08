#pragma once
#include "esphome/core/component.h"
#include "esphome/core/log.h"
#include <cstdio>
#include <string>

namespace esphome {
namespace host_exec {

  static int run_status_only(const std::string &cmd) {
    FILE *fp = popen(cmd.c_str(), "r");
    if (!fp) return -1;
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), fp)) {
    }
    return pclose(fp);
  }

  static std::string run_command(const std::string &cmd) {
    FILE *fp = popen(cmd.c_str(), "r");
    if (!fp) return "";
    char buffer[256];
    std::string result;
    while (fgets(buffer, sizeof(buffer), fp)) {
      result += buffer;
    }
    pclose(fp);
    while (!result.empty() && (result.back() == '\n' || result.back() == '\r'))
      result.pop_back();
    return result;
  }

  class HostExec : public Component {
  };

}  // namespace host_exec
}  // namespace esphome
