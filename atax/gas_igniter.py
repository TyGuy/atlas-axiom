import time

DEFAULT_GAS_PIN = 27
DEFAULT_IGNITER_PIN = 17

class GasIgniter:
    def __init__(self, gpio, gas_pin = DEFAULT_GAS_PIN, igniter_pin = DEFAULT_IGNITER_PIN):
        """
        Initialize the GasIgniterController with the GPIO pins for the gas and igniter.

        :param gas_pin: GPIO pin number for the gas control.
        :param igniter_pin: GPIO pin number for the igniter control.
        :param gpio: GPIO module to use. This class assumes GPIO has been set up, but the pins have not.
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
        self._turn_on_igniter()
        time.sleep(duration)
        self._turn_off_igniter()
    

    # main thing to use:
    def turn_on(self, gas_duration = 2, igniter_duration=3):
        """
        Sequence to turn on gas, ignite it, and then turn it off.

        :param duration: Duration (in seconds) to keep the igniter on.
        """
        self._turn_on_gas()
        time.sleep(gas_duration)
        self._ignite_gas(igniter_duration)
        print("FLAME SHOULD BE ON! If not, stop this script and light the flame.")
    
    def turn_off(self):
        """Turn off the gas and igniter."""
        self._turn_off_gas()
        self._turn_off_igniter()

if __name__ == "__main__":
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM


    # Create an instance of the GasIgniterController
    # (Optionally, can override pins)
    gas_igniter = GasIgniter(GPIO)

    # Example usage
    gas_igniter.turn_on()
    time.sleep(10)
    gas_igniter.turn_off()