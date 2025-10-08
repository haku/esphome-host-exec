WARNING
=======

Barely tested prototype that still includes some LLM generated code that needs
further review.  You MUST review this code yourself before using.

What this does
--------------

Provides a CLI interface when running esphome in [Host
Platform](https://esphome.io/components/host/) mode.  Thus any linux box can
expose sensors and actions to Home Assistant.

Notes
-----

TODO:
* Properly review `host_exec.h`.
* Change the sensor to use the command exit code?
* Make a number sensor that reads command output?
* Use root component for some kinda monitoring (currently its only there to make the build happy).
