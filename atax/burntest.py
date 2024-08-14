import serial
import signal
import sys
import RPi.GPIO as GPIO
from burn_manager import BurnManager
    
# Global variables
GRBL_port_path = '/dev/ttyACM0' # change port here if needed
basefile_name = 'B1_heart_gear'
BAUD_RATE = 115200
# lights gpio
UPPER_LIGHTS_PIN = 26
LOWER_LIGHTS_PIN = 16

burn_manager = None

def handle_termination():
    """Handle termination signals gracefully."""
    def signal_handler(sig, frame):
        print("Received termination signal. Shutting down gracefully...")
        burn_manager.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def init():
    ser = serial.Serial(GRBL_port_path, BAUD_RATE)
    GPIO.setmode(GPIO.BCM) 
    burn_manager = BurnManager(basefile_name, ser, GPIO)
    
def loop():
    handle_termination()

    try:
        burn_manager.start()
        while True:
            # TODO: eventually incorporate other code here.
            continue

    except Exception as e:
        print(f"An error occurred: {e}")
        burn_manager.stop()
        sys.exit(1)

if __name__ == "__main__":
    init()
    loop()