import json
import os
import random

from user_positions import CENTERED_RING, ALL_ABOVE, AROUND_THE_EDGE, get_user_positions

class StateManager:

    base_image_modes = {
       "B1_heart_gear": CENTERED_RING,
    }

    def __init__(self, basefile_name):
        self.basefile_name = basefile_name
        self.image_mode = self.base_image_modes[basefile_name]
        # All state files will be kept in "state" -- removing the files effectively clears the state.
        self.state_folder = "state/"

        # File for keeping track of the base image segements; which have been burned ("burned"),
        # and which haven't ("to_burn"):
        self.base_image_state_file = os.path.join(self.state_folder, "base_image_state.json")
        self.base_image_state = None

        # File for keeping track of which user positions are still remaining for burning
        # the user-selected images:
        self.user_positions_file = os.path.join(self.state_folder, "user_positions.json")
        self.user_positions_state = []

        # File for keeping track of the sequence of user images that are to be burned on the
        # next "user image" burn cycle:
        self.user_image_sequence_file = os.path.join(self.state_folder, "user_sequence.txt")

        self.load_state()

    def load_state(self):
        if not os.path.exists(self.base_image_state_file):
            self.initialize_base_image_state()
        else:
            self.load_base_image_state()

        self.initialize_user_positions()

    ### Base images state:
    def initialize_base_image_state(self):
        if not os.path.exists(self.base_image_state_file):
            # Get filenames from the folder "images/base/{basefile_name}/", and initialize
            # the state with all files in "to_burn" and none in "burned":
            base_image_folder = os.path.join("images/base", self.basefile_name)
            base_image_files = os.listdir(base_image_folder)
            random.shuffle(base_image_files)
            self.base_image_state = {
                "to_burn": base_image_files,
                "burned": []
            }
        else:
            # Load state from file:
            with open(self.base_image_state_file, 'r') as file:
                self.base_image_state = json.load(file)

        # Write the initial state to the file:
        with open(self.base_image_state_file, 'w') as file:
            json.dump(self.base_image_state, file, indent=4)
        
    def get_to_burn_list(self):
        return self.base_image_state["to_burn"]
    
    def mark_base_image_segement_burned(self, filename):
        self.base_image_state["to_burn"].remove(filename)
        self.base_image_state["burned"].append(filename)
        with open(self.base_image_state_file, 'w') as file:
            json.dump(self.base_image_state, file, indent=4)

    ### User image positions state:
    def initialize_user_positions(self):
        # Try to read the positions from the file
        positions = self.read_from_file()
        if positions:
            # If positions are found in the file, shuffle and return them
            self.user_positions_state = positions
        else:
            # If no positions are found, generate new ones, write to the file, and return them
            positions = self.generate_new_positions(self.image_mode)
            self.write_user_positions_to_file(positions)
            self.user_positions_state = positions
    
    def get_next_user_position(self):
        # Return the first position in the list
        return self.user_positions_state[0]
    
    def mark_position_processed(self):
        # Remove the first position in the list (assume it's processed)
        if self.user_positions_state:
            self.user_positions_state.pop(0)
            # Update the file with the remaining positions
            self.write_user_positions_to_file(self.user_positions_state)

            if not (self.user_positions_state):
                # write a user sequence file with value = DONE,
                # which is a special value. It tells other devices looking for the file
                # presence that they should lock out user controls, but it tells this process
                # that it has completed all positions so there are no more user images 
                # that can be burned.
                with open(self.user_image_sequence_file, "w") as file:
                    file.write(f"DONE\n")


    def read_from_file(self):
        # Check if the file exists
        if os.path.exists(self.user_positions_file):
            with open(self.user_positions_file, 'r') as file:
                positions = json.load(file)
                return positions
        return None
    
    def generate_new_positions(self, mode):
        # Generate a new list of positions based on the mode
        positions = get_user_positions(mode)
        random.shuffle(positions)
        return positions
    
    def write_user_positions_to_file(self, positions):
        # Write the current positions list to the file
        with open(self.user_positions_file, 'w') as file:
            json.dump(positions, file, indent=4)


    ### User image sequence state:
    def is_user_image_waiting(self):
        # If the user_positions_state is empty, then there are no more user images to burn,
        # so return False.
        if self.user_positions_state:
            # Otherwise, check if the user image sequence file exists
            return os.path.exists(self.user_image_sequence_file)
    
    def get_next_image_in_user_sequence(self):
        user_images = self._get_images_in_user_sequence()
        return user_images[0]

    def _get_images_in_user_sequence(self):
        with open(self.user_image_sequence_file, "r") as file:
            user_images = [line.strip() for line in file.readlines()]
            return user_images
    
    def mark_user_image_processed(self, user_image):
        user_images = self._get_images_in_user_sequence()
        # remove the matching value in the array, and write to file:
        user_images.remove(user_image)

        if not user_images:
            self.clear_user_sequence()
        else:
            with open(self.user_image_sequence_file, "w") as file:
                for image in user_images:
                    file.write(f"{image}\n")


    def clear_user_sequence(self):
        os.remove(self.user_image_sequence_file)