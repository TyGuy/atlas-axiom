import serial
import RPi.GPIO as GPIO
from burn_manager import BurnManager
    

GRBL_port_path = '/dev/ttyACM0' # change port here if needed
basefile_name = 'B1_heart_gear'
BAUD_RATE = 115200

def init():
    ser = serial.Serial(GRBL_port_path, BAUD_RATE)
    GPIO.setmode(GPIO.BCM) 
    burn_manager = BurnManager(basefile_name, ser, GPIO)
    