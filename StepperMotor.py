import RPi.GPIO as GPIO
import time


class StepperMotor:
    STEPS_PER_REVOLUTION = 400 # controlled by DIP switches
    # Delay between pulses; This will control speed of motor
    # r / s


    def __init__(self, pulse_pin, direction_pin, speed=1):
        # if pulse_pin is None or not between 40, raise:
        if (pulse_pin is None or not (0 <= pulse_pin <= 40)):
            raise ValueError("pulse_pin must be a number between 0 and 40")
        
        self.pulse_pin = pulse_pin
        self.direction_pin = direction_pin
        self.delay = 1 / (self.STEPS_PER_REVOLUTION * speed)
        
        self._initialize_gpio()
        
    def _initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pulse_pin, GPIO.OUT)
        GPIO.output(self.pulse_pin, GPIO.LOW)

        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.output(self.direction_pin, GPIO.LOW)

    def _set_direction(self, direction):
        if direction == "CW":  # Clockwise
            GPIO.output(self.direction_pin, GPIO.HIGH)
        elif direction == "CCW":  # Counter-clockwise
            GPIO.output(self.direction_pin, GPIO.LOW)

    # Function to send pulses to the motor driver
    def _send_pulses(self, steps):
        for _ in range(steps):
            GPIO.output(self.pulse_pin, GPIO.HIGH)
            time.sleep(self.delay / 2.0)
            GPIO.output(self.pulse_pin, GPIO.LOW)
            time.sleep(self.delay / 2.0)

    # Function to run the motor
    def run_motor_steps(self, steps, direction):
        self._set_direction(direction)
        self._send_pulses(steps)
    
    def run_motor_degrees(self, degrees, direction):
        steps = int((degrees / 360) * self.STEPS_PER_REVOLUTION)
        self.run_motor_steps(steps, direction)

        