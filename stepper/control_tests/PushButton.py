import signal
import sys
import RPi.GPIO as GPIO


class PushButton:
    bounce_time = 100  # 100ms debounce

    def __init__(self, gpio_pin, button_pressed_callback=None, button_released_callback=None):
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # add button pressed event if passed in:
        if button_pressed_callback is not None:
            self.button_pressed_callback = button_pressed_callback
            try:
                GPIO.add_event_detect(self.gpio_pin, GPIO.FALLING,
                                      callback=self.button_pressed_callback, bouncetime=self.bounce_time)
            except RuntimeError as e:
                print(f"Failed to add button pressed event: {e}")

        # add button released event if passed in:
        if button_released_callback is not None:
            self.button_released_callback = button_released_callback
            try:
                GPIO.add_event_detect(self.gpio_pin, GPIO.RISING,
                                      callback=self.button_released_callback, bouncetime=self.bounce_time)
            except RuntimeError as e:
                print(f"Failed to add button released event: {e}")

    def cleanup(self):
        GPIO.cleanup()

# test code:
BUTTON_GPIO = 16

def cleanup_handler(signal, frame):
    push_button.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    print("Button pressed!")

if __name__ == '__main__':
    push_button = PushButton(BUTTON_GPIO, button_pressed_callback, None)
    
    signal.signal(signal.SIGINT, cleanup_handler)
    print("Waiting for button press...")
    signal.pause()