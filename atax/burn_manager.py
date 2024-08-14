import threading
import time
import os
from state_manager import StateManager
from gas_igniter import GasIgniter
from simple_stream import draw_file_at_position, draw_gcode_file


# TODO: could move user_image stuff to its own file.
user_image_filenames = [
    "UGI_00_CircleFrame_x0y0.ngc",
    "UGI_01_Skull_x0y0.ngc",
    "UGI_02_Heart_x0y0.ngc",
    "UGI_03_Shield_x0y0.ngc",
    "UGI_04_Gear_x0y0.ngc",
    "UGI_05_House_x0y0.ngc",
    "UGI_06_Eyeball_x0y0.ngc",
    "UGI_07_Clock_x0y0.ngc",
    "UGI_08_Spider_x0y0.ngc",
    "UGI_09_Mountain_x0y0.ngc",
    "UGI_10_Boat_x0y0.ngc",
    "UGI_11_Peace_x0y0.ngc",
    "UGI_12_Cat_x0y0.ngc",
    "UGI_13_Wave_x0y0.ngc",
    "UGI_14_Sunset_x0y0.ngc",
    "UGI_15_Leaf_x0y0.ngc",
    "UGI_16_Scales_x0y0.ngc",
]

user_image_path = "images/user/"


class BurnManager:
    def __init__(self, basefile, ser, gpio):
        self.state_manager = StateManager(basefile)
        self.gas_igniter = GasIgniter(gpio)
        self.basefile = basefile
        self.ser = ser
        self.lock = threading.Lock()

        self.is_running = False  # Controls whether the manager is active
        self.is_burning = False  # Indicates whether an active burn is in progress
        self.user_sequence_waiting = False  # Flag indicating a user sequence is queued
        self.resting = False  # Flag indicating if the machine is in resting mode

        self.burn_thread = threading.Thread(target=self.run_burn_cycle)
        self.monitor_thread = threading.Thread(target=self.monitor_user_input)

    def start(self):
        """Start the burn process and the monitor thread."""
        self.is_running = True
        self.gas_igniter.turn_on()
        self.burn_thread.start()
        self.monitor_thread.start()

    def stop(self):
        """Gracefully stop the burn process."""
        self.is_running = False
        self.gas_igniter.turn_off()
        if self.burn_thread.is_alive():
            self.burn_thread.join()
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()

    def run_burn_cycle(self):
        """Main loop for handling the burning process."""
        while self.is_running:
            with self.lock:
                if self.resting or self.is_burning:
                    continue

                if self.user_sequence_waiting:
                    self.is_burning = True
                    self.process_user_sequence()
                else:
                    self.is_burning = True
                    self.process_base_image_segment()

                self.is_burning = False  # Burn completed
                self.resting = True  # Enter rest period

            self.handle_rest_period()

    def monitor_user_input(self):
        """Continuously monitor for user input indicating a new user sequence."""
        while self.is_running:
            if self.state_manager.is_user_image_waiting() and not self.user_sequence_waiting:
                with self.lock:
                    self.user_sequence_waiting = True
            time.sleep(1)  # Polling interval

    def process_base_image_segment(self):
        """Process the next base image segment."""
        to_burn_list = self.state_manager.get_to_burn_list()

        if to_burn_list:
            next_file = to_burn_list[0]
            print(f"Burning base image segment: {next_file}")
            # draw_gcode_file(self.ser, next_file)
            time.sleep(10)
            print(f"Base image segment burned: {next_file}; marking as processed.")
            self.state_manager.mark_base_image_segement_burned(next_file)

    def process_user_sequence(self):
        """Process the user-generated image sequence."""
        user_position = self.state_manager.get_next_user_position()
        # get pos_name, x, y from user_position
        pos_name = user_position["pos_name"]
        x = user_position["x"]
        y = user_position["y"]
        print(f"Burning user images: at position {pos_name} ({x}, {y})")

        with open(self.state_manager.user_image_sequence_file, "r") as file:
            user_images = [line.strip() for line in file.readlines()]

        for image_num in user_images:
            image_file = os.path.join(user_image_path, user_image_filenames[int(image_num)])
            print(f"\tBurning user image: {image_file}")
            # draw_file_at_position(self.ser, image_file, x, y)
            time.sleep(10)
            # this also handles removing the file if we've processed the last thing.
            self.state_manager.mark_user_image_processed(image_num)

        # After burning, clear the user sequence and reset the waiting flag
        print("User image sequence completed. Marking position processed.")
        self.state_manager.mark_position_processed()
        self.user_sequence_waiting = False

    def handle_rest_period(self):
        """Handle the cooldown period between burns."""
        print("Entering rest period. Turning off solenoid...")
        self.gas_igniter.turn_off()
        print("Solenoid turned off. Resting for 30 seconds...")
        time.sleep(30)
        print("Rest period completed. Turning on solenoid and igniter...")
        self.gas_igniter.turn_on()
        print("It's lit.")
        with self.lock:
            self.resting = False  # End rest period, ready to burn again