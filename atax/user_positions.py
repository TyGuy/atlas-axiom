import json
import os
import random

class UserPositions:
    def __init__(self, user_positions_file="user_positions.json", mode="centered_ring"):
        self.user_positions_file = user_positions_file
        self.mode = mode
        self.remaining_positions = self.initialize_user_positions()
    
    def initialize_user_positions(self):
        # Try to read the positions from the file
        positions = self.read_from_file()
        if positions:
            # If positions are found in the file, shuffle and return them
            return positions
        else:
            # If no positions are found, generate new ones, write to the file, and return them
            positions = self.generate_new_positions(self.mode)
            self.write_to_file(positions)
            return positions
    
    def mark_position_processed(self):
        # Remove the first position in the list (assume it's processed)
        if self.remaining_positions:
            self.remaining_positions.pop(0)
            # Update the file with the remaining positions
            self.write_to_file(self.remaining_positions)

    def read_from_file(self):
        # Check if the file exists
        if os.path.exists(self.user_positions_file):
            with open(self.user_positions_file, 'r') as file:
                positions = json.load(file)
                return positions
        return None
    
    def generate_new_positions(self, mode):
        # Generate a new list of positions based on the mode
        positions = get_positions(mode)
        random.shuffle(positions)
        return positions
    
    def write_to_file(self, positions):
        # Write the current positions list to the file
        with open(self.user_positions_file, 'w') as file:
            json.dump(positions, file, indent=4)

# Function to get the positions based on a valid name
def get_positions(name):
    if name == "centered_ring":
        return positions_centered_ring
    elif name == "around_the_edge":
        return positions_around_the_edge
    elif name == "all_above":
        return positions_all_above
    else:
        return None

# Predefined positions for different modes
positions_centered_ring = [
    # comment this back in once the board actually has wood there.
    # {"posName": 1, "x": 90.4, "y": 137.4},
    # {"posName": 2, "x": 111.7, "y": 128.2},
    # {"posName": 3, "x": 128.2, "y": 111.7},
    # {"posName": 4, "x": 137.4, "y": 90.4},
    # {"posName": 5, "x": 137.4, "y": 66.6},
    # {"posName": 6, "x": 128.2, "y": 44.6},
    # {"posName": 7, "x": 111.7, "y": 28.2},
    # {"posName": 8, "x": 90.4, "y": 19.6},
    {"posName": 9, "x": 65.4, "y": 19.6},
    {"posName": 10, "x": 44.6, "y": 27.6},
    {"posName": 11, "x": 27.6, "y": 44.6},
    {"posName": 12, "x": 17.8, "y": 66.6},
    {"posName": 13, "x": 17.8, "y": 90.4},
    {"posName": 14, "x": 27.6, "y": 111.7},
    {"posName": 15, "x": 44.6, "y": 128.2},
    {"posName": 16, "x": 65.4, "y": 137.4}
]

positions_around_the_edge = [
    {"posName": 1, "x": 2.3, "y": 155.3},
    {"posName": 2, "x": 32.9, "y": 155.3},
    {"posName": 3, "x": 63.5, "y": 155.3},
    {"posName": 4, "x": 94.1, "y": 155.3},
    {"posName": 5, "x": 124.7, "y": 155.3},
    {"posName": 6, "x": 155.3, "y": 155.3},
    {"posName": 7, "x": 155.3, "y": 124.7},
    {"posName": 8, "x": 155.3, "y": 94.1},
    {"posName": 9, "x": 155.3, "y": 63.5},
    {"posName": 10, "x": 155.3, "y": 32.9},
    {"posName": 11, "x": 155.3, "y": 2.3},
    {"posName": 12, "x": 124.7, "y": 2.3},
    {"posName": 13, "x": 94.1, "y": 2.3},
    {"posName": 14, "x": 63.5, "y": 2.3},
    {"posName": 15, "x": 32.9, "y": 2.3},
    {"posName": 16, "x": 2.3, "y": 2.3},
    {"posName": 17, "x": 2.3, "y": 32.9},
    {"posName": 18, "x": 2.3, "y": 63.5},
    {"posName": 19, "x": 2.3, "y": 94.1},
    {"posName": 20, "x": 2.3, "y": 124.7}
]

positions_all_above = [
    {"posName": 1, "x": 2.3, "y": 155.3},
    {"posName": 2, "x": 32.9, "y": 155.3},
    {"posName": 3, "x": 63.5, "y": 155.3},
    {"posName": 4, "x": 94.1, "y": 155.3},
    {"posName": 5, "x": 124.7, "y": 155.3},
    {"posName": 6, "x": 155.3, "y": 155.3},
    {"posName": 7, "x": 14.8, "y": 135.5},
    {"posName": 8, "x": 45.4, "y": 135.5},
    {"posName": 9, "x": 76.0, "y": 135.5},
    {"posName": 10, "x": 106.6, "y": 135.5},
    {"posName": 11, "x": 137.2, "y": 135.5},
    {"posName": 12, "x": 61.7, "y": 117.8},
    {"posName": 13, "x": 92.3, "y": 117.8}
]