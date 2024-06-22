import RPi.GPIO as GPIO
import time
from gpiozero import Button
from signal import pause
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

class MotorController:
    def __init__(self, motor, button1_pin, button2_pin):
        self.motor = motor
        self.state = "stopped"
        self.running = False

        self.button1 = Button(button1_pin)
        self.button2 = Button(button2_pin)

        self.button1.when_released = self.handle_button1_press
        self.button2.when_released = self.handle_button2_press

    def handle_button1_press(self):
        if self.state == "stopped" or self.state == "counterclockwise":
            self.start_motor(clockwise=True)
        elif self.state == "clockwise":
            self.stop_motor()

    def handle_button2_press(self):
        if self.state == "stopped" or self.state == "clockwise":
            self.start_motor(clockwise=False)
        elif self.state == "counterclockwise":
            self.stop_motor()

    def start_motor(self, clockwise):
        direction = "clockwise" if clockwise else "counterclockwise"
        print(f"Starting motor {direction}")
        self.state = direction
        self.running = True
        self.run_motor(clockwise)

    def stop_motor(self):
        print("Stopping motor")
        self.state = "stopped"
        self.running = False

    def run_motor(self, clockwise):
        def rotate():
            while self.running:
                if clockwise:
                    self.motor.rotate_clockwise(22.5, 0.1)
                else:
                    self.motor.rotate_counter_clockwise(22.5, 0.1)
        thread = threading.Thread(target=rotate)
        thread.start()

if __name__ == '__main__':
    motor = StepperMotorVariableSpeed(steps_for_full_rotation=4096, gpio_pins=[17, 18, 27, 22])
    motor_controller = MotorController(motor, button1_pin=16, button2_pin=20)
    
    print("System ready. Press buttons to control the motor.")
    try:
        pause()  # Keep the program running to listen for button presses
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        motor.cleanup()