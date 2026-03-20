# Meshmonitor-dice-roller
Script for Meshmonitor that can be used with the auto-responder module to respond to /roll {dice}, /coinflip, and /8ball

## Setup
1. Place `roll.py` in Meshmonitor's /data/scripts directory.
2. Make it executable with `chmod +x roll.py`
3. Open MeshMonitor, go to the automation page, and enable Auto Responder.
4. Add a Trigger - `/roll {dice}` - with type Script and select `roll.py`
5. Select the channels and/or DMs you'd like the auto repsonder to listen on.
6. Click Add next to `roll.py` to create the trigger.
7. Add triggers for `/coinflip` and `8ball` too, both calling the `roll.py` script.
8. Click save at the bottom of the page to save the Automation settings.
