# Meshmonitor-dice-roller
Script for Meshmonitor that can be used with the auto-responder module to respond to /roll {dice}, /coinflip, and /8ball

## Setup
1. Place `roll.py` in Meshmonitor's /data/scripts directory.
2. Make it executable with `chmod +x roll.py`
3. Open MeshMonitor, go to the automation page, and enable Auto Responder.
4. Add a Trigger - `/roll {dice}, /coinflip, /8ball{question:.*}` - with type Script and select `roll.py`
5. Select the channels and/or DMs you'd like the auto repsonder to listen on.
6. Click Add next to `roll.py` to create the trigger.
7. Click save at the bottom of the page to save the Automation settings.

## Features & How It Works

`roll.py` is a Python script designed to be used with [MeshMonitor's Auto Responder](https://meshmonitor.org/features/automation.html#auto-responder). It listens for specific command patterns sent over your Meshtastic LoRa network and automatically replies with randomized dice rolls, coin flips, or magic 8-ball answers.

**Core Capabilities:**
* **Dice Parsing:** Supports standard RPG dice notation (e.g., `1d20`, `2d6+4`, `1d20-1`).
* **Advantage/Disadvantage:** Supports `adv` and `dis` modifiers (e.g., `1d20 adv`), which rolls two separate sets of dice and keeps the highest or lowest sum, respectively.
* **Built-in Minigames & Commands:** Handled transparently when the triggers `/roll help`, `/coinflip`, or `/8ball` are used.
* **Flavor Text:** Includes humorous, custom responses for specific rolls, such as critical successes/failures (nat 20 / nat 1 on a d20), casting "fireball" (8d6), or attempting impossible rolls (like 0 dice or a d0).
* **Mesh-Safe Limits:** Caps rolls at 10,000 dice and strictly truncates the final output to 200 characters to prevent spam and conserve LoRa airtime.

**How it integrates with Meshmonitor:**
When a node on the mesh sends a message matching your configured triggers (`/roll {dice}`, `/coinflip`, or `/8ball`), Meshmonitor's Auto Responder intercepts it and executes `roll.py`. The script reads the incoming command via the `MESSAGE` or `TRIGGER` environment variables automatically injected by MeshMonitor. It processes the text, calculates the result, and outputs a JSON object (e.g., `{"response": "You rolled 15"}`). Meshmonitor then parses this JSON and transmits the text response back to the channel or node over the Meshtastic network.
