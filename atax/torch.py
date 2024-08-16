import RPi.GPIO as GPIO
from gas_igniter import GasIgniter

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM) 
    gas_igniter = GasIgniter()

    while True:
        command = input("Enter command ('on'/'off'/'exit'): ").strip().lower()

        if command == "on":
            gas_igniter.turn_on()
        elif command == "off":
            gas_igniter.turn_off()
        elif command == "exit":
            print("Exiting the REPL.")
            break
        else:
            print("Invalid command. Please enter 'on', 'off', or 'exit'.")