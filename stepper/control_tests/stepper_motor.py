import RPi.GPIO as GPIO
import time

# Define GPIO pins
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# initializing
GPIO.output( IN1, GPIO.LOW )
GPIO.output( IN2, GPIO.LOW )
GPIO.output( IN3, GPIO.LOW )
GPIO.output( IN4, GPIO.LOW )

# Define step sequence
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

# Function to set the motor pins
def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)
    print(f"Set step: {w1}, {w2}, {w3}, {w4}")



# Function to rotate the motor
def rotate(steps, delay):
    for i in range(steps):
        for j in range(8):
            set_step(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            time.sleep(delay)

# Main code
try:
    while True:
        steps = int(input("Enter number of steps to rotate: "))
        delay = float(input("Enter delay between steps (e.g., 0.01): "))
        rotate(steps, delay)
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    GPIO.cleanup()
