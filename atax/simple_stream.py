"""
This is a simple script that attempts to connect to the GRBL controller at 
> /dev/tty.usbserial-A906L14X
It then reads the grbl_test.gcode and sends it to the controller

The script waits for the completion of the sent line of gcode before moving onto the next line

tested on
> MacOs Monterey arm64
> Python 3.9.5 | packaged by conda-forge | (default, Jun 19 2021, 00:24:55) 
[Clang 11.1.0 ] on darwin
> Vscode 1.62.3
> Openbuilds BlackBox GRBL controller
> GRBL 1.1

"""

import time
from threading import Event

def remove_comment(string):
    cleaned = string
    if (cleaned.find(';') != -1):
        cleaned = cleaned[:cleaned.index(';')]
    if (cleaned.find('(') != -1):
        cleaned = cleaned[:cleaned.index('(')]
    return cleaned
        

def remove_eol_chars(string):
    # removed \n or traling spaces
    return string.strip()


# NOTE: not sure if this is necessary, and incurs a slight delay.
def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)   # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input

def wait_for_movement_completion(ser,cleaned_line = None):

    # Event().wait(0.1)

    if cleaned_line != '$X' or '$$':

        idle_counter = 0

        while True:

            # Event().wait(0.02)
            ser.reset_input_buffer()
            command = str.encode('?' + '\n')
            ser.write(command)
            grbl_out = ser.readline() 
            grbl_response = grbl_out.strip().decode('utf-8')

            if grbl_response != 'ok':

                if grbl_response.find('Idle') > 0:
                    idle_counter += 1

            if idle_counter >= 2:
                break
    return

def go_to_origin(ser):
    # Go to origin
    command = ['G0 X0 Y0\n']
    stream_gcode_lines(ser, command)

def go_to_position(ser, x, y):
    command = ['G0 X' + str(x) + ' Y' + str(y) + '\n']
    stream_gcode_lines(ser, command)


def draw_file_at_position(ser, gcode_path, x=0, y=0, end_at_zero = False):
    with open(gcode_path, "r") as file:
        startup_lines = f"""
        G54
        G0 X{x} Y{y}
        G10 L20 P2 X0 Y0
        G55
        """

        ending_lines = [
        "G54"
        ]
        if (end_at_zero):
            ending_lines += ["G0 X0 Y0"]

        lines = startup_lines.split('\n') + file.readlines() + ending_lines
        stream_gcode_lines(ser, lines)

def stream_gcode(ser,gcode_path, send_reset_first = True):
    draw_gcode_file(ser,gcode_path, send_reset_first)

def draw_gcode_file(ser,gcode_path, send_reset_first = True):
    # with contect opens file/connection and closes it if function(with) scope is left
    with open(gcode_path, "r") as file:
        startup_lines = """
        $RST=#
        G10 P1 L20 X0 Y0
        """ if send_reset_first else ""

        lines = startup_lines.split('\n') + file.readlines()
        stream_gcode_lines(ser, lines)


def stream_gcode_lines(ser, lines):
    send_wake_up(ser)

    batch_size = 5
    cur_line_num = 0

    for line in lines:
        # cleaning up gcode from file
        cleaned_line = remove_eol_chars(remove_comment(line))
        if cleaned_line:  # checks if string is empty
            cur_line_num += 1
            print("Sending gcode:" + str(cleaned_line))
            # converts string to byte encoded string and append newline
            command = str.encode(line + '\n')
            ser.write(command)  # Send g-code

            grbl_out = ser.readline()  # Wait for response with carriage return
            print(" : " , grbl_out.strip().decode('utf-8'))

            if cur_line_num % batch_size == 0 or cur_line_num == len(lines):
                wait_for_movement_completion(ser,cleaned_line)
        
    print('End of gcode')

if __name__ == "__main__":

    GRBL_port_path = '/dev/ttyACM0'
    #GRBL_port_path = 'COM1'
    gcode_path = 'grbl_test.gcode'

    print("USB Port: ", GRBL_port_path)
    print("Gcode file: ", gcode_path)
    stream_gcode(GRBL_port_path,gcode_path)

    print('EOF')
