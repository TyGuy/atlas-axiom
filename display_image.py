import pygame
import sys
import serial
import time

# Initialize Pygame
pygame.init()

# Get display information
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Load the image
image_path = '/home/bug/Downloads.jpeg'  # Replace with your image file path
image = pygame.image.load(image_path)

# Scale the image to fit the screen
image = pygame.transform.scale(image, (screen_width, screen_height))

# Configure serial port
serial_port = '/dev/ttyACM0'  # Replace with your serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Main loop
running = True
display_image = False

while running:
    if ser.in_waiting > 0:
        data = ser.read().decode('utf-8')
        if data == '1':
            display_image = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    if display_image:
        screen.blit(image, (0, 0))
        pygame.display.flip()

    # Delay to avoid excessive CPU usage
    time.sleep(0.1)

# Clean up
ser.close()
pygame.quit()
sys.exit()