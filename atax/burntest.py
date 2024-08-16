import argparse
import serial
import signal
import sys
import RPi.GPIO as GPIO
from burn_manager import BurnManager
from simple_stream import go_to_position, tell_machine_its_at_origin
from base_image import base_image_modes

valid_basefiles = list(base_image_modes.keys())
    
# Global variables
GRBL_port_path = '/dev/ttyACM0' # change port here if needed
BAUD_RATE = 115200
# lights gpio
UPPER_LIGHTS_PIN = 26
LOWER_LIGHTS_PIN = 16

X_MACHINE_OFFSET = 1
Y_MACHINE_OFFSET = 3.5

burn_manager = None
ser = None

def validate_basefile(basefile):
    global valid_basefiles
    if basefile not in valid_basefiles:
        raise argparse.ArgumentTypeError(f"Invalid basefile: '{basefile}'. Must be one of {valid_basefiles}.")
    return basefile

def handle_termination(burn_manager, ser):
    """Handle termination signals gracefully."""
    def signal_handler(sig, frame):
        print("Received termination signal. Shutting down gracefully...")
        go_to_position(ser, X_MACHINE_OFFSET * -1, Y_MACHINE_OFFSET * -1, 0)
        tell_machine_its_at_origin(ser)
        burn_manager.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def init(basefile_name):
    global burn_manager, ser
    ser = serial.Serial(GRBL_port_path, BAUD_RATE)
    GPIO.setmode(GPIO.BCM) 
    burn_manager = BurnManager(basefile_name, ser, GPIO)
    # move to the origin:
    go_to_position(ser, X_MACHINE_OFFSET, Y_MACHINE_OFFSET)
    tell_machine_its_at_origin(ser)

    
def loop():
    global burn_manager, ser
    handle_termination(burn_manager, ser)

    try:
        burn_manager.start()
        while True:
            # TODO: eventually incorporate other code here.
            continue

    except Exception as e:
        print(f"An error occurred: {e}")
        go_to_position(ser, X_MACHINE_OFFSET * -1, Y_MACHINE_OFFSET * -1, 0)
        tell_machine_its_at_origin(ser)
        burn_manager.stop()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The main burn loop for the amazing Atlas machine.")
    parser.add_argument('basefile', type=lambda b: validate_basefile(b), 
                        help=f"The basefile to use. Must be one of {', '.join(valid_basefiles)}.")
    args = parser.parse_args()

    init(args.basefile)
    loop()