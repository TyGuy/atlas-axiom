import serial
import time
from simple_stream import remove_comment, remove_eol_chars, wait_for_movement_completion, send_wake_up
# Assuming the existing helper functions (remove_comment, remove_eol_chars, etc.) are included here

class GCodeStreamer:
    def __init__(self, port_path):
        self.ser = serial.Serial(port_path, 115200)
        self.send_wake_up()

    def send_wake_up(self):
        # Wake up the controller
        self.ser.write(str.encode("\r\n\r\n"))
        time.sleep(2)
        self.ser.flushInput()

    def stream_gcode_line(self, line):
        cleaned_line = remove_eol_chars(remove_comment(line))
        if cleaned_line:  # checks if string is empty
            print("Sending gcode:" + str(cleaned_line))
            command = str.encode(cleaned_line + '\n')
            self.ser.write(command)

            # Wait for response
            grbl_out = self.ser.readline()
            print(" : ", grbl_out.strip().decode('utf-8'))

            # Optional: Wait for movement completion if necessary
            wait_for_movement_completion(self.ser, cleaned_line)

    def close(self):
        self.ser.close()

if __name__ == "__main__":
    GRBL_port_path = '/dev/ttyACM0'
    gcode_streamer = GCodeStreamer(GRBL_port_path)

    try:
        while True:
            command = input("Enter G-code command ('exit' to quit): ").strip()
            if command.lower() == 'exit':
                print("Exiting the REPL.")
                break
            gcode_streamer.stream_gcode_line(command)
    except KeyboardInterrupt:
        print("Interrupted! Exiting.")
    finally:
        gcode_streamer.close()
        print('Connection closed.')

