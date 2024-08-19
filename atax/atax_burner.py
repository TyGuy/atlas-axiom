from pathlib import Path
import cv2
import depthai
import numpy as np
from playsound import playsound
import time
import os
import random
import shutil
import multiprocessing
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import pygame
import threading
#
import argparse
import serial
import signal
import sys
import RPi.GPIO as GPIO
from burn_manager import BurnManager
from simple_stream import go_to_position, tell_machine_its_at_origin
from base_image import base_image_modes


# tylers inits here
valid_basefiles = list(base_image_modes.keys())
    
# Global variables
GRBL_port_path = '/dev/ttyACM0' # change port here if needed
BAUD_RATE = 115200
# lights gpio
UPPER_LIGHTS_PIN = 26
LOWER_LIGHTS_PIN = 16

X_MACHINE_OFFSET = 1
Y_MACHINE_OFFSET = 3.5

burn_manager = None
ser = None

cleanup_started = False


# sandeeps stuff here

def play_random_audio(folder_path):
    """Play a random audio file from the given folder in a separate thread."""
    
    def play_audio():
        try:
            # Initialize pygame mixer
            pygame.mixer.init()
            print("pygame mixer initialized.")
            
            # List all audio files in the folder
            audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp3', '.wav'))]
            if not audio_files:
                print("No audio files found in the folder.")
                return
            
            # Select a random audio file
            audio_file = random.choice(audio_files)
            print(f"Selected audio file: {audio_file}")

            # Load and play the selected audio file
            pygame.mixer.music.load(os.path.join(folder_path, audio_file))
            pygame.mixer.music.play()
            
            # Wait until the audio is done playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        except pygame.error as e:
            print(f"Pygame error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            # Clean up the mixer
            pygame.mixer.quit()
            print("pygame mixer quit.")

    # Start a new thread for audio playback
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
    return audio_thread

# sandeeps inits here
# setting up oak-d camera
pipeline = depthai.Pipeline()

cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(300, 300)
cam_rgb.setInterleaved(False)

detection_nn = pipeline.createMobileNetDetectionNetwork()
detection_nn.setBlobPath(str((Path(__file__).parent / Path('face-detection-retail-0004.blob')).resolve().absolute()))
detection_nn.setConfidenceThreshold(0.5)
cam_rgb.preview.link(detection_nn.input)

xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

xout_nn = pipeline.createXLinkOut()
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)

# tylers functions here

def handle_termination(burn_manager, ser):
    """Handle termination signals gracefully."""
    def signal_handler(sig, frame):
        global cleanup_started
        if cleanup_started:
            print("Received second termination signal. Exiting immediately.")
            sys.exit(1)
        else:
            cleanup_started = True
            print("Received termination signal. Shutting down gracefully...")
            go_to_position(ser, X_MACHINE_OFFSET * -1, Y_MACHINE_OFFSET * -1, 0)
            tell_machine_its_at_origin(ser)
            burn_manager.stop()
            sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def validate_basefile(basefile, valid_basefiles):
    if basefile not in valid_basefiles:
        raise argparse.ArgumentTypeError(f"Invalid basefile: '{basefile}'. Must be one of {valid_basefiles}.")
    return basefile

def init(basefile_name):
    global burn_manager, ser
    ser = serial.Serial(GRBL_port_path, BAUD_RATE)
    GPIO.setmode(GPIO.BCM) 
    burn_manager = BurnManager(basefile_name, ser, GPIO)
    # move to the origin:
    go_to_position(ser, X_MACHINE_OFFSET, Y_MACHINE_OFFSET)
    tell_machine_its_at_origin(ser)
    

# Pipeline is now finished, and we need to find an available device to run our pipeline
def loop():
    with depthai.Device(pipeline) as device:
        q_rgb = device.getOutputQueue("rgb", maxSize=4, blocking=False)
        q_nn = device.getOutputQueue("nn", maxSize=4, blocking=False)
        frame = None
        detections = []
        prevpeople = 0
        nextplaytime = datetime.now() + timedelta(seconds=15)

        def frameNorm(frame, bbox):
            normVals = np.full(len(bbox), frame.shape[0])
            normVals[::2] = frame.shape[1]
            return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)
        

        # tyler loop 
        global burn_manager, ser
        handle_termination(burn_manager, ser)

        try:
            burn_manager.start()
            while True:
                # TODO: eventually incorporate other code here.
                in_rgb = q_rgb.tryGet()
                in_nn = q_nn.tryGet()

                if in_rgb is not None:
                    frame = in_rgb.getCvFrame()

                if in_nn is not None:
                    detections = in_nn.detections

                if frame is not None:
                    # Every 15 seconds check if there are any new arrivals
                    now = datetime.now()
                    if now >= nextplaytime:
                        nextplaytime = now + timedelta(seconds=15)
                        npeople = len(detections)
                        if npeople > prevpeople:
                            # Play random hello audio
                            print("play from folder hello")
                            audio_process = play_random_audio('audiofiles/hello')
                            prevpeople = npeople
                            
                        elif npeople < prevpeople:
                            # Play random bye audio
                            audio_process = play_random_audio('audiofiles/bye')
                            print("play from folder bye")
                            prevpeople = npeople
                        elif npeople == 0:
                            # Stay asleep play snoring noise
                            prevpeople = npeople 
                    # commenting out as video rendering is not needed
                    # for detection in detections:
                    #     bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                    #     cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                    # cv2.imshow("preview", frame)
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            go_to_position(ser, X_MACHINE_OFFSET * -1, Y_MACHINE_OFFSET * -1, 0)
            tell_machine_its_at_origin(ser)
            burn_manager.stop()
            sys.exit(1)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The main burn loop for the amazing Atlas machine.")
    parser.add_argument('--basefile', type=lambda b: validate_basefile(b, valid_basefiles), 
                        help=f"The basefile to use. Must be one of {', '.join(valid_basefiles)}.", default=None)
    args = parser.parse_args()

    init(args.basefile)
    loop()