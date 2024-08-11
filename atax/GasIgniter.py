import time

class GasIgniter:
    def __init__(self, gas_pin, igniter_pin, gpio):
        """
        Initialize the GasIgniterController with the GPIO pins for the gas and igniter.

        :param gas_pin: GPIO pin number for the gas control.
        :param igniter_pin: GPIO pin number for the igniter control.
        :param gpio: GPIO module to use (optional). If None, assumes GPIO is globally available.
        """
        self.gpio = gpio
        self.gas_pin = gas_pin
        self.igniter_pin = igniter_pin
        self._setup_pins()

    def _setup_pins(self):
        """Set up the GPIO pins as outputs."""
        self.gpio.setup(self.gas_pin, self.gpio.OUT)
        self.gpio.setup(self.igniter_pin, self.gpio.OUT)

    def _turn_on_gas(self):
        """Turn on the gas by setting the gas GPIO pin to HIGH."""
        self.gpio.output(self.gas_pin, self.gpio.HIGH)
    
    def _turn_off_gas(self):
        """Turn off the gas by setting the gas GPIO pin to LOW."""
        self.gpio.output(self.gas_pin, self.gpio.LOW)
    
    def _turn_on_igniter(self):
        """Turn on the igniter by setting the igniter GPIO pin to HIGH."""
        self.gpio.output(self.igniter_pin, self.gpio.HIGH)
    
    def _turn_off_igniter(self):
        """Turn off the igniter by setting the igniter GPIO pin to LOW."""
        self.gpio.output(self.igniter_pin, self.gpio.LOW)

    def _ignite_gas(self, duration=3):
        """
        Ignite the gas by turning on the igniter for a specified duration.

        :param duration: Duration (in seconds) to keep the igniter on.
        """
        self.turn_on_igniter()
        time.sleep(duration)
        self.turn_off_igniter()
    

    # main thing to use:
    def turn_on(self, gas_duration = 5, igniter_duration=3):
        """
        Sequence to turn on gas, ignite it, and then turn it off.

        :param duration: Duration (in seconds) to keep the igniter on.
        """
        self.turn_on_gas()
        time.sleep(gas_duration)
        self.ignite_gas(igniter_duration)
    
    def turn_off(self):
        """Turn off the gas and igniter."""
        self.turn_off_gas()
        self.turn_off_igniter()

if __name__ == "__main__":
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM

    # Define the GPIO pins for gas and igniter
    gas_pin = 17
    igniter_pin = 27

    # Create an instance of the GasIgniterController
    gas_igniter = GasIgniter(gas_pin, igniter_pin, GPIO)

    # Example usage
    gas_igniter.turn_on_gas()  # Turn gas on
    time.sleep(5)  # Wait for 5 seconds
    gas_igniter.ignite_gas()  # Ignite gas for the default duration (3 seconds)
    gas_igniter.turn_off_gas()  # Turn gas off