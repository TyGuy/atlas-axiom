import RPi.GPIO as GPIO
import time

# Define GPIO pins
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Function to toggle GPIO pins
def toggle_pins():
    pins = [IN1, IN2, IN3, IN4]
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
        print(f"GPIO {pin} HIGH")
        time.sleep(1)
        GPIO.output(pin, GPIO.LOW)
        print(f"GPIO {pin} LOW")
        time.sleep(1)

# Main code
try:
    while True:
        toggle_pins()
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.cleanup()