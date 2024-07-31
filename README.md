# Atlas Axiom Robot Code

This repo contains code for a robot which holds a torch and burns patterns/art into a 2D surface like wood.

From a code / control perspective, it can be thought of as a fancy, fire-wielding plotter.

## Required components
* Raspberry Pi (using raspberry pi 2 model B)
* Arduino connected to CNC Atlas machine and set up running GRBL (aka Stepper motors, sensors, etc)
* Pi connected to Arduino via serial connection

## Setup
On your raspberry pi, startt by cloning the repo (**NOTE: this project uses git submodules, so be sure to include the option below**):
```sh
git clone --recurse-submodules https://github.com/TyGuy/atlas-axiom.git
cd atlas-axiom
```

Install pyenv, python 3, and pipenv via this script:
```sh
./scripts/install_python_deps.sh
```

Install java & UGS (Universal GCode sender) via this script:
```sh
./scripts/install_java_and_ugs.sh
```

## Running UGS
Run UGS using `./scripts/start_ugs.sh`
* Doing it this way also adds a "port" option of 8080, so we can optionally connect to UGS via a local REST API if desired.

---

## The plan [WIP, out of date]
At a high level, the software components we need to find and/or build are:
* User input collector -> take in some words, or combination of button presses, for example
* Image generator -> choose an image based on the input (either AI gen, predefined set, something else)
* GCode generator -> convert an image (some file format) to GCode
* GCode executor -> convert GCode to mechanics (X/Y movement, open/close solenoid, change distance or aperature)

---

## Useful links [WIP needs more]
* Good for understanding GCode: https://www.simplify3d.com/resources/articles/3d-printing-gcode-tutorial/
* Python code we could probably use for GCode generator: https://github.com/arpruss/gcodeplot
* Helpful for understanding mechanics/components of a plotter: https://www.youtube.com/watch?v=virDtVVt2Xo


