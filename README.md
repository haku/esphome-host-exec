What this does
--------------

* A simple way to use Home Assistant to run pre-defined commands on any linux
box with very minimal overheads.
* The daemon uses ~3 MiB of RAM.
* Configuration is done via the same yaml files as when ESPHome is run on
microcontroller.  There are examples in the `device-configs` directory.
* This repo contains tooling to build ESPHome in [Host
Platform](https://esphome.io/components/host/) mode and install it as a systemd
service.

Usage
-----

These commands assume a Debian-like OS, but may work on a variety of distros.

```shell
$ ./venv install
$ . ./venv
$ nice -n 19 ionice -c 3 esphome compile ./example.yaml
$ ./install-systemd-service.py ./example.yaml
```

Then manually add device in Home Assistant ESPHome.

Note: you must manually put the NIC MAC in the yaml config file as ESPHome does
not seem to detect this automatically in host mode.

Allowing Agent to Call Shutdown
-------------------------------

Allowing a `DynamicUser=yes` unit to shutdown does not seem to be possible ATM
(on bookworm), so this is the best approach i can come up with.  systemd
generally inhibits setuid so we have to go via polkit, buut...  polkit does not
like systemd's DynamicUser=true OR SupplementaryGroups so lets just given the
user permission directly.

```
$ useradd --system esphome
$ vim /etc/polkit-1/rules.d/esphome.rules
polkit.addRule(function(action, subject) {
  //polkit.log("action=" + action);
  //polkit.log("subject=" + subject);

  if (action.id == "org.freedesktop.login1.power-off" ||
      action.id == "org.freedesktop.login1.power-off-ignore-inhibit" ||
      action.id == "org.freedesktop.login1.power-off-multiple-sessions") {
    if (subject.user == "esphome") {
        return polkit.Result.YES;
    }
  }
});
```

Possible Improvements
---------------------

* Review `host_exec.h` as it can likely be further improved.
* Maybe add a sensor that reads the content of a file?  Maybe with regexps?
* Maybe make a number sensor that reads command output?
* Could use root component for some kinda monitoring (currently its only there
  to make the build happy).
