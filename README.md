# Atlas Axiom Robot Code

This repo contains code The Atlas / Axiom robot.

## Usage:
Structure:
* Things in `atax` are for the "main pi" / drawing pi
* Things in `image_display` are for the "image display" pi
* Things in `images` contain `user` and `base` for user-selected gcode image files and base image file segments, respectively.
* Things in `state` control state. 3 files.

### running the thing
```shell
cd ~/atlas
# needs to be run from atlas directory, not atax; run it like this:
python atax/burntest.py --basefile B1_heart_gear # also, make sure this is not inconsistent with what's in the state file.
```

### Running arbitrary gcode
```shell
cd ~/atlas
python atax/gcode_repl.py
# then type any gcode, and enter it. Type "exit" to quit.
```

### Running just the torch
```shell
cd ~/atlas
python atax/torch.py
# then type "on" to turn it on, "off" to turn it off, "exit" to exit.
```

### Starting UGS
Just run `start_ugs` from anywhere.

### Other notes:
* Make sure the thing is at machine 0,0 (below/left of canvas 0,0), and that Z is at 0, before starting the script
* Also make sure the machine knows where it is. You can run reset commands manually from the above script, but UGS is the best way to be sure.
  * You should re-zero twice (zero, disconnect & reconnect, and zero again)
* Make sure you're not trying to connect from
* Check state files before/after running
* Type `ctrl-C` to stop the script(s). This will end it gracefully, finishing gcode commands, returning to origin (and Z0), and turning off the torch.
  * Hit `ctrl-C` twice to stop the burntest script immediately. This will not go back to origin and do cleanup stuff; but GRBL will finish whatever gcode command(s) it has received.

---

## Useful links [WIP needs more]
* Good for understanding GCode: https://www.simplify3d.com/resources/articles/3d-printing-gcode-tutorial/
* Python code we could probably use for GCode generator: https://github.com/arpruss/gcodeplot
* Helpful for understanding mechanics/components of a plotter: https://www.youtube.com/watch?v=virDtVVt2Xo


