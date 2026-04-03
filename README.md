What this does
--------------

Provides a CLI interface when running ESPHome in [Host
Platform](https://esphome.io/components/host/) mode.  Thus any linux box can
expose sensors and actions to Home Assistant.

Usage
-----

```shell
$ ./venv install
$ . ./venv
$ nice -n 19 ionice -c 3 esphome compile ./example.yaml
$ ./install-systemd-service.py ./example.yaml
```

Then manually add device in Home Assistant ESPHome.

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

Notes
-----

TODO:
* Properly review `host_exec.h`.
* Add a sensor that reads the content of a file?  Maybe with regexps?
* Make a number sensor that reads command output?
* Use root component for some kinda monitoring (currently its only there to make the build happy).
