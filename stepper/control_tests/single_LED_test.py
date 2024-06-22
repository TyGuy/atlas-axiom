import RPi.GPIO as GPIO
import time

# Define GPIO pin
TEST_PIN = 17

# Set up GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(TEST_PIN, GPIO.OUT)

# Turn on the GPIO pin
try:
    GPIO.output(TEST_PIN, GPIO.HIGH)
    print(f"GPIO {TEST_PIN} HIGH")
    time.sleep(5)  # Keep the LED on for 5 seconds
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.output(TEST_PIN, GPIO.LOW)  # Ensure the pin is low before cleanup
    GPIO.cleanup()