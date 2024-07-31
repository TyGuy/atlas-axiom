import RPi.GPIO as GPIO
import time
from StepperMotor import StepperMotor

# GPIO Pin configuration
PUL_PIN = 18  # Pulse pin
DIR_PIN = 23  # Direction pin
# ENA_PIN = 24  # Enable pin (optional)

# # Function to enable the motor driver
# def enable_driver():
#     GPIO.output(ENA_PIN, GPIO.HIGH)  # Enable driver (LOW to enable, HIGH to disable)

# # Function to disable the motor driver
# def disable_driver():
#     GPIO.output(ENA_PIN, GPIO.LOW)  # Disable driver

# # Function to set the direction of the motor
# def set_direction(direction):
#     if direction == "CW":  # Clockwise
#         GPIO.output(DIR_PIN, GPIO.HIGH)
#     elif direction == "CCW":  # Counter-clockwise
#         GPIO.output(DIR_PIN, GPIO.LOW)

# # Function to send pulses to the motor driver
# def send_pulses(steps, delay):
#     for _ in range(steps):
#         GPIO.output(PUL_PIN, GPIO.HIGH)
#         # print("Pulse high")
#         time.sleep(delay)
#         GPIO.output(PUL_PIN, GPIO.LOW)
#         # print("Pulse low")
#         time.sleep(delay)

# # Function to run the motor
# def run_motor(steps, delay, direction):
#     set_direction(direction)
#     send_pulses(steps, delay)

# Example usage
try:
    stepper_motor = StepperMotor(PUL_PIN, DIR_PIN, speed=2)

    while True:
        print("Running motor CW")
        stepper_motor.run_motor_degrees(360 * 2, "CW")
        print("Sleeping for 2 seconds")
        time.sleep(2)

        print("Running motor CCW")
        stepper_motor.run_motor_degrees(360 * 2, "CCW")
        print("Sleeping for 2 seconds")
        time.sleep(2)

except KeyboardInterrupt:
    # disable_driver()
    GPIO.cleanup()
