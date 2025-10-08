What this does
--------------

Provides a CLI interface when running ESPHome in [Host
Platform](https://esphome.io/components/host/) mode.  Thus any linux box can
expose sensors and actions to Home Assistant.

Notes
-----

TODO:
* Properly review `host_exec.h`.
* Add a sensor that reads the content of a file?  Maybe with regexps?
* Make a number sensor that reads command output?
* Use root component for some kinda monitoring (currently its only there to make the build happy).
