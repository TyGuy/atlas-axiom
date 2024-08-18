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
# these files need to be stored in a folder called for_display
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
        return base_image
    
    combined = base_image.copy()
    combined.blit(overlay_image, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return combined

def save_selections(selections):
    """Save the last two selected image numbers to a text file with spaces separating the numbers and a zero at the end."""
    # Keep only the last two selections
    last_two_selections = selections[-2:]
    
    # Convert selections to string with spaces separating them
    selections_str = ' '.join(map(str, last_two_selections)) + ' 0'
    
    # Define the path to the file
    file_path = 'selections.txt'
    
    # Write to the file
    with open(file_path, 'w') as file:
        file.write(selections_str + '\n')


    # image pi credentials:
    #source_ip = '10.0.0.190'
    #source_user = 'bug'
    #source_pass = 'bugcat'
    # sshpass -p raspberry scp user_selections.txt pi@10.0.0.63:/home/pi/depthai-python/atax/atax_v1/user_selections.txt

   # Define the target machine's IP, target_user, and destination path
    target_ip = '10.0.0.63'
    target_user = 'pi'
    target_pass = 'raspberry'
    destination_path = f'/home/{target_user}/atlas/state/selections.txt'

    # SCP command
    scp_command = [
        'sshpass', '-p', target_pass, 'scp', file_path, f'{target_user}@{target_ip}:{destination_path}'
    ]
    
    # Run the SCP command and check if it was successful
    try:
        result = subprocess.run(scp_command, capture_output=True, text=True)
        if result.returncode == 0:
            print("File transfer successful.")
            # Wait until the target machine processes and deletes the file
            wait_for_no_file_on_target()
            # Remove the file from the host machine after successful transfer
            os.remove(file_path)
            print("File removed from the host machine.")
        else:
            print("File transfer failed.")
            print(result.stderr)
    except Exception as e:
        print(f"Error occurred during file transfer: {e}")

    # Notify that the file is ready
    ser.write(b'ready\n')

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

# Load special images
start_image = load_image("Start.png")
selected_overlay = load_image("Selected.png")

# Main loop
running = True

while running:
    # Poll for file absence before processing serial input
    wait_for_no_file_on_target()

    if ser.in_waiting > 0:
        try:
            data = ser.read().decode('utf-8').strip()
            if data == 'reset':
                current_image = None
                screen.fill((0, 0, 0))  # Fill the screen with black for "reset"
                last_two_images = [None, None]  # Clear the image history
                selected_images = []  # Clear selected images
            elif data == 'start':
                current_image = start_image
                last_two_images = [None, None]  # Clear the image history
                selected_images = []  # Clear selected images
            elif data == 'submit':
                if current_image and selected_overlay:
                    current_image = overlay_images(current_image, selected_overlay)
                # Save selected images to file
                save_selections(selected_images)
                ser.write(b'lockout\n')
                # Wait until the target machine processes and deletes the file
                wait_for_no_file_on_target()
            elif data.isdigit():
                image_key = int(data)
                if image_key in image_files:
                    if image_key not in selected_images:
                        selected_images.append(image_key)  # Add to selected images
                    
                    new_image = load_image(image_files[image_key])
                    
                    # Update image history
                    last_two_images[0] = last_two_images[1]
                    last_two_images[1] = new_image
                    
                    # Determine the combined image
                    if last_two_images[0] and last_two_images[1]:
                        current_image = overlay_images(last_two_images[0], last_two_images[1])
                    else:
                        current_image = last_two_images[1]
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

    # Clear the screen or display the current image
    screen.fill((0, 0, 0))  # Start with a blank screen
    if current_image:
        screen.blit(current_image, (0, 0))

    pygame.display.flip()
    time.sleep(0.1)

# Clean up
if ser.is_open:
    ser.close()
pygame.quit()
sys.exit()
