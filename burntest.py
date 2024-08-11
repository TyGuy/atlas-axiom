from burngcodefile import burn_gcode
from user_positions import UserPositions
from simple_stream import stream_gcode, draw_file_at_position
import serial

GRBL_port_path = '/dev/ttyACM0' # change port here if needed
gcode_path = 'orgtest.ngc' # change file name here
BAUD_RATE = 115200
# gas_pin = 17
# igniter_pin = 27

images_and_modes = {
    "image1": "centered_ring",
    "image2": "around_the_edge",
    "image3": "all_above"
}

# at some point, this will be come along with the initialization of the script.
image = "image1"
mode = images_and_modes[image]
user_positions = UserPositions(mode=mode)
positions = user_positions.remaining_positions
print("Positions: ", positions)

# choose a random position from the list
position = positions[0]
print("Position: ", position)
user_chosen_images = [
    "UGI_01_Skull_x0y0.ngc",
    "UGI_02_Heart_x0y0_0001.ngc",
]
# frame every use image with a circle
user_images_to_draw = user_chosen_images + ["UGI_00_CircleFrame_x0y0.ngc"]
# draw stuff
ser = serial.Serial(GRBL_port_path, BAUD_RATE)

print("Drawing images at position: ", position)

# TODO: need to do the reset before drawing the images.

for user_image in user_images_to_draw:
    draw_file_at_position(ser, user_image, x=position["x"], y=position["y"])

user_positions.mark_position_processed()


# burn_gcode(GRBL_port_path,gcode_path)
