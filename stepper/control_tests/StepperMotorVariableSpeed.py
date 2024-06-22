import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause
import time
import threading

class StepperMotorVariableSpeed:
    # Step sequence for the stepper motor
    seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    # can update this, but to be safe, don't try to turn the motor too fast:
    min_delay = 0.001 # this is roughly 1000 steps per second, so it takes 4 seconds to do a full rotation @ 4096 steps.
    
    def __init__(self, steps_for_full_rotation=4096, gpio_pins=[17, 18, 27, 22]):
        if len(gpio_pins) != 4 or any(not (0 <= pin <= 40) for pin in gpio_pins):
            raise ValueError("gpio_pins must be an array of exactly 4 numbers between 0 and 40")
        
        self.steps_for_full_rotation = steps_for_full_rotation
        self.gpio_pins = gpio_pins
        self.motor_step_position = 0
        
        self.initialize_gpio()
        
    def initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.gpio_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
    
    def cleanup(self):
        for pin in self.gpio_pins:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
        
    def _set_step(self, w1, w2, w3, w4):
        GPIO.output(self.gpio_pins[0], w1)
        GPIO.output(self.gpio_pins[1], w2)
        GPIO.output(self.gpio_pins[2], w3)
        GPIO.output(self.gpio_pins[3], w4)
    
    def _rotate(self, steps, delay_secs, clockwise=True):
        step_count = len(self.seq)
        step_dir = 1 if clockwise else -1
        
        for step in range(steps):
            self.motor_step_position = (self.motor_step_position + step_dir) % self.steps_for_full_rotation
            seq_index = self.motor_step_position % step_count
            self._set_step(*self.seq[seq_index])
            time.sleep(delay_secs)
    
    def _rotate_degrees(self, degrees, secs, clockwise=True):
        steps = int(degrees / 360 * self.steps_for_full_rotation)
        delay_secs = secs / steps
        if (delay_secs < self.min_delay):
            # warn the user that we are limiting the motor speed:
            print(f"Warning: limiting motor speed to {1/self.min_delay:.2f} steps per second (requested {1/delay_secs:.2f} steps per second)")
            delay_secs = self.min_delay 

        
        start_time = time.time()
        self._rotate(steps, delay_secs, clockwise=clockwise)
        end_time = time.time()
        
        actual_degrees = steps / self.steps_for_full_rotation * 360
        actual_time = end_time - start_time
        
        return steps, actual_degrees, actual_time

    
    def rotate_clockwise(self, degrees, secs):
        return self._rotate_degrees(degrees, secs, clockwise=True)
    
    def rotate_counter_clockwise(self, degrees, secs):
        return self._rotate_degrees(degrees, secs, clockwise=False)

# Example usage
if __name__ == "__main__":
    motor = StepperMotorVariableSpeed()
    try:
        steps, degrees, time_taken = motor.rotate_clockwise(360, 2)
        print(f"Rotated {steps} steps, which is approximately {degrees} degrees clockwise over {time_taken:.2f} seconds.")

        time.sleep(5)
        
        steps, degrees, time_taken = motor.rotate_counter_clockwise(360, 2)
        print(f"Rotated {steps} steps, which is approximately {degrees} degrees counterclockwise over {time_taken:.2f} seconds.")
    finally:
        motor.cleanup()