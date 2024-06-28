import RPi.GPIO as GPIO
import time

# GPIO Pin configuration
PUL_PIN = 18  # Pulse pin
DIR_PIN = 23  # Direction pin
ENA_PIN = 24  # Enable pin (optional)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUL_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT)

# Function to enable the motor driver
def enable_driver():
    GPIO.output(ENA_PIN, GPIO.HIGH)  # Enable driver (LOW to enable, HIGH to disable)

# Function to disable the motor driver
def disable_driver():
    GPIO.output(ENA_PIN, GPIO.LOW)  # Disable driver

# Function to set the direction of the motor
def set_direction(direction):
    if direction == "CW":  # Clockwise
        GPIO.output(DIR_PIN, GPIO.HIGH)
    elif direction == "CCW":  # Counter-clockwise
        GPIO.output(DIR_PIN, GPIO.LOW)

# Function to send pulses to the motor driver
def send_pulses(steps, delay):
    for _ in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        print("Pulse high")
        time.sleep(delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        print("Pulse low")
        time.sleep(delay)

# Function to run the motor
def run_motor(steps, speed, direction):
    set_direction(direction)
    delay = 1.0 / (2 * speed)  # Delay between pulses 1 / 200 = 0.005 seconds
    send_pulses(steps, delay)

# Example usage
try:
    GPIO.output(PUL_PIN, GPIO.HIGH)
    GPIO.output(DIR_PIN, GPIO.HIGH)
    GPIO.output(ENA_PIN, GPIO.HIGH)
    time.sleep(1000)

    # enable_driver()
    # while True:
    #     # Run the motor clockwise for 1000 steps at 1000 pulses per second
    #     print("Running motor CW")
    #     run_motor(100, 100, "CW")
    #     print("Sleeping for 10 seconds")
    #     time.sleep(10)  # Wait for 1 second
    #     # Run the motor counter-clockwise for 1000 steps at 1000 pulses per second
    #     print("Running motor CCW")
    #     run_motor(100, 100, "CCW")
    #     print("Sleeping for 10 seconds")
    #     time.sleep(10)  # Wait for 1 second
except KeyboardInterrupt:
    disable_driver()
    GPIO.cleanup()