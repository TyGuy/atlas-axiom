import RPi.GPIO as GPIO
import time

BUTTON_GPIO = 16

def button_pressed_callback(channel):
    print("Button pressed!")


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("Button initialized")
time.sleep(5)

# Add event detect for button press
GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_pressed_callback)
# GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_pressed_callback, bouncetime=100)

print("Waiting for button press... (Press Ctrl+C to exit)")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()