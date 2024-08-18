import pygame
import sys
import serial
import time
import subprocess
import os

# Initialize Pygame
pygame.init()

# Get display information
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Define the mapping of serial commands to image files
image_files = {
    1: "Gear.png",
    2: "Boat.png",
    3: "House.png",
    4: "Clock.png",
    5: "Shield.png",
    6: "Mountain.png",
    7: "Leaf.png",
    8: "Skull.png",
    9: "Cat.png",
    10: "Wave.png",
    11: "Spider.png",
    12: "Sunset.png",
    13: "Eyeball.png",
    14: "Heart.png",
    15: "Peace.png",
    16: "Scale.png",
}

# Configure serial port
serial_port = '/dev/ttyACM0'  # Replace with your serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Initialize variables
last_two_images = [None, None]
current_image = None
selected_images = []

# To track the last command and its timestamp
last_command = None
last_command_time = 0

def load_image(image_name):
    """Load an image and scale it to fit the screen."""
    try:
        image_path = f'for_display/{image_name}'
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (screen_width, screen_height))
        return image
    except pygame.error as e:
        print(f"Error loading image {image_name}: {e}")
        return None

def overlay_images(base_image, overlay_image):
    """Overlay one image on top of another."""
    if base_image is None or overlay_image is None:
        return overlay_image  # Return the overlay if base is None, or return None if both are None
    
    combined = base_image.copy()
    combined.blit(overlay_image, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return combined

def save_selections(selections):
    """Save the last two selected image numbers to a text file with spaces separating the numbers and a zero at the end."""
    last_two_selections = selections[-2:]
    selections_str = ' '.join(map(str, last_two_selections)) + ' 0'
    file_path = 'selections.txt'
    with open(file_path, 'w') as file:
        file.write(selections_str + '\n')

    target_ip = '10.0.0.63'
    target_user = 'pi'
    target_pass = 'raspberry'
    destination_path = f'/home/{target_user}/atlas/state/selections.txt'

    scp_command = [
        'sshpass', '-p', target_pass, 'scp', file_path, f'{target_user}@{target_ip}:{destination_path}'
    ]
    
    try:
        result = subprocess.run(scp_command, capture_output=True, text=True)
        if result.returncode == 0:
            print("File transfer successful.")
            wait_for_no_file_on_target()
            os.remove(file_path)
            print("File removed from the host machine.")
        else:
            print("File transfer failed.")
            print(result.stderr)
    except Exception as e:
        print(f"Error occurred during file transfer: {e}")



def file_exists_on_target():
    """Check if the selections.txt file exists on the target machine."""
    target_ip = '10.0.0.63'
    target_user = 'pi'
    target_pass = 'raspberry'
    destination_path = f'/home/{target_user}/atlas/state/selections.txt'
    
    check_command = f"sshpass -p {target_pass} ssh {target_user}@{target_ip} 'test -f {destination_path}'"
    result = subprocess.run(check_command, shell=True, capture_output=True)
    
    return result.returncode == 0

def wait_for_no_file_on_target():
    """Poll the target machine until selections.txt is not found."""
    print("Polling for the absence of selections.txt on the target machine...")
    while file_exists_on_target():
        print("File found. Waiting 10 seconds before retrying...")
        time.sleep(10)
    print("No file found. Proceeding with serial data processing.")
    ser.write(b'OPEN\n') #tell GC its ready for user selections

# Load special images
start_image = load_image("Start.png")
selected_overlay = load_image("Selected.png")

# Main loop
running = True

while running:
    wait_for_no_file_on_target()

    if ser.in_waiting > 0:
        try:
            data = ser.read().decode('utf-8').strip()
            current_time = time.time()

            # Check for duplicate command within 50 milliseconds
            if data == last_command and (current_time - last_command_time) < 0.05:
                continue  # Ignore this command if it's a duplicate

            # Update the last command and timestamp
            last_command = data
            last_command_time = current_time

            if data == 'RESET':
                current_image = None
                screen.fill((0, 0, 0))
                last_two_images = [None, None]
                selected_images = []
            elif data == 'START':
                current_image = start_image
                last_two_images = [None, None]
                selected_images = []
            elif data == 'SUBMIT':
                if current_image and selected_overlay:
                    current_image = overlay_images(current_image, selected_overlay)
                save_selections(selected_images)
                ser.write(b'LOCKOUT\n') # issue lock out to GC
                wait_for_no_file_on_target()
            elif data.isdigit():
                image_key = int(data)
                if image_key in image_files:
                    if image_key not in selected_images:
                        selected_images.append(image_key)
                    
                    # Keep only the last two selected images
                    if len(selected_images) > 2:
                        selected_images = selected_images[-2:]
                    
                    # Load the images to overlay
                    last_two_images = [load_image(image_files[selected_images[0]]),
                                       load_image(image_files[selected_images[1]])]
                    
                    # Determine the combined image
                    current_image = overlay_images(last_two_images[0], last_two_images[1])
                else:
                    current_image = None
            else:
                current_image = None

        except ValueError:
            current_image = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill((0, 0, 0))
    if current_image:
        screen.blit(current_image, (0, 0))

    pygame.display.flip()
    time.sleep(0.1)

if ser.is_open:
    ser.close()
pygame.quit()
sys.exit()
