# Atlas Axiom Robot Code

This repo contains code for a robot which holds a torch and burns patterns/art into a 2D surface like wood.

From a code / control perspective, it can be thought of as a fancy, fire-wielding plotter.

## Required components
* Raspberry Pi (using raspberry pi 2 model B)
* Stepper motors & drivers (& ideally entire plotter)
* 5V (or other voltage) power supply for motors

## Software setup
On your raspberry pi, run the following commands to install python3, pip & pipenv:

```sh
# install some dependencies for building python:
sudo apt install -y libbz2-dev libncurses5-dev libncursesw5-dev libffi-dev libreadline-dev libssl-dev zlib1g-dev

# install and set up pyenv:
curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
exec "$SHELL"

# install newest python3 version
pyenv install 3.12.4

# set global python version to 3.12.4
pyenv global 3.12.4

# check python version
python --version

# install pipenv:
pip install --user pipenv
```

Clone this repo:
```sh
git clone https://github.com/TyGuy/atlas-axiom.git
cd atlas-axiom
```


---

## The plan
At a high level, the software components we need to find and/or build are:
* User input collector -> take in some words, or combination of button presses, for example
* Image generator -> choose an image based on the input (either AI gen, predefined set, something else)
* GCode generator -> convert an image (some file format) to GCode
* GCode executor -> convert GCode to mechanics (X/Y movement, open/close solenoid, change distance or aperature)

---

## Useful links
* Good for understanding GCode: https://www.simplify3d.com/resources/articles/3d-printing-gcode-tutorial/
* Python code we could probably use for GCode generator: https://github.com/arpruss/gcodeplot
* Helpful for understanding mechanics/components of a plotter: https://www.youtube.com/watch?v=virDtVVt2Xo


