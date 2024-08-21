# Atlas Axiom Robot Code

This repo contains code The Atlas / Axiom robot.

## Structure:
* Things in `atax` are for the "main pi" / "burn pi"
* Things in `image_display` are for the "image display" pi
* Things in `images` contain `user` and `base` for user-selected gcode image files and base image file segments, respectively.
* Things in `state` control state. 3 files.

## Running the main program

### Setup

#### Make sure of the following:
* Cables are connected properly
  * (make sure usb cables are in the right ports, for burn pi <-> GRBL, and image display pi <-> GC -- otherwise, you might have to change the serial port in the scripts)
* Propane is open in the right places
* Everything is powered (incl the motors)
* The machine is at 0,0,0 (machine position, not canvas position)
* Mouse, keyboard, and monitor are connected to the burn pi


On the burn pi, you'll need 3 terminal windows open:
* The first is for UGS
* The second is for the main script (don't run it yet though)
* The third is optional, but will be useful for debugging, or running scripts such as `torch.py`, `gcode_repl.py`, or `direct_ugi.py`.

#### Before running the scripts:
Zero with UGS.
* Open a terminal window, and open UGS, by running `start_ugs` from anywhere.
* Connect to the GRBL machine in UGS, and zero the machine TWICE (zero, disconnect & reconnect, zero again)
* Close the connection in UGS (You can keep UGS open, but you need to close the connection to the machine)

Check the state files, and make sure they're ok.
* They should EITHER be non-existent, OR the `state/base_image_state.json` should have the same base image file reference as the command you want to run. Otherwise, you need to run the script with the basefile matching what's in state, OR remove the state files.
* Look in the "state" directory (you can do this from the desktop of the pi; you don't need to use a terminal).
* If the files are not what you want, you can modify them manually with the default editor (geany), or you can remove them completely with `rm state/*` from the terminal. Be carfeful with this; if you do it, you can't get them back.
* If you remove them, the program will create new ones with default values when you run it.

### Run the main burn script
* Open a terminal window, and navigate to the `atlas` directory, then run the main file. We're going to try 2 different variants; the first (`atax_burner.py`) has cooler stuff including camera and audio and light control, but the second (`burntest.py`) has been proven to work.

Variant 1 (try this for camera/lights/audio):
```shell
cd ~/atlas
python atax/atax_burner.py --basefile B1_heart_gear
```

Variant 2 (for a simple burn experience):
```shell
cd ~/atlas
python atax/burntest.py --basefile B1_heart_gear
```

### Run the image display
There are 3 ways we could potentially run this, let's start with most ambitious, and scale back to simpler methods if needed.

For the first 2, start by opening a terminal window on the image display pi.

Variant 1 (user presses physical buttons to determine images):
```shell
cd atlas-axiom/image-display
python3 image_display.py
```

Variant 2 (Alan used keyboard input on image display Pi to determine images):
```shell
cd atlas-axiom/image-display
python3 image_display_k.py
```

Notes on the keyboard script:
- Works with keyboard input. Use the following commands:
  - Press `O` (capital O) to start.
  - Enter numbers `1-16` followed by `Enter` to select images.
  - To overlay more images, enter another number.
  - Press `R` to clear the screen if you want to start over.
  - Press `S` to submit your selection. You can submit even after entering just one number.

Variant 3 (cut out the image display pi completely, and run the following on the BURN PI):
```shell
cd ~/atlas
python atax/direct_ugi.py
```

Instructions are printed when you start the script.

### Killing the burn script
Hit ctrl+c ONCE to stop the burn script.
* This will stop the script gracefully, finishing gcode commands, returning to origin (and Z0), and turning off the torch.
* If you hit it twice, it will stop the script immediately, but GRBL will finish whatever gcode command(s) it has received (you cannot stop this, unless you cut the power, which you probably should not do).


## Troubleshooting:
Cannot connect to GRBL:
* Confirm the serial port is correct in the script
  * If you can connect in UGS, you can see what the correct port value is.

Cannot connect to the serial port for the GC on image display pi:
* Confirm the serial port is correct in the script

[probably other stuff but I can't think of it right now]...

## Other potentially useful scripts, for debugging or testing:

### Running arbitrary gcode (from burn pi)
```shell
cd ~/atlas
python atax/gcode_repl.py
# then type any gcode, and enter it. Type "exit" to quit.
```

### Running just the torch (from burn pi)
```shell
cd ~/atlas
python atax/torch.py
# then type "on" to turn it on, "off" to turn it off, "exit" to exit.
```

### Starting UGS
Just run `start_ugs` from anywhere. This should actually work now.

---

## Old stuff below here

### Useful links [WIP needs more]
* Good for understanding GCode: https://www.simplify3d.com/resources/articles/3d-printing-gcode-tutorial/
* Python code we could probably use for GCode generator: https://github.com/arpruss/gcodeplot
* Helpful for understanding mechanics/components of a plotter: https://www.youtube.com/watch?v=virDtVVt2Xo


