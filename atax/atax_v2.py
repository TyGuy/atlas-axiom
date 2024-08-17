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
from burn_manager import BurnManager
from state_manager import StateManager
import RPi.GPIO as GPIO

# Initialize StateManager
#basefile = "path_to_basefile"  # Replace with the actual basefile path
#state_manager = StateManager(basefile)

# Initialize BurnManager
# Port of GRBL device check in dev folder usually /dev/ttyACM0
GRBL_port_path = '/dev/ttyACM0'
#burn_manager = BurnManager(basefile, GRBL_port_path, GPIO)


def play_random_audio(folder_path):
    """Play a random audio file from the given folder in a separate process."""
    def play_audio():
        audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp3', '.wav'))]
        if not audio_files:
            print("No audio files found in the folder.")
            return
        audio_file = random.choice(audio_files)
        print(f"Selected audio file: {audio_file}")
        playsound(os.path.join(folder_path, audio_file))

    # Start a new process for audio playback
    audio_process = multiprocessing.Process(target=play_audio)
    audio_process.start()
    return audio_process


# need a function to set up the burning a multi process task and call that

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

# Pipeline is now finished, and we need to find an available device to run our pipeline
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
    while True:
        # check if selections.txt is avalable in folder 

        # if selections is available burn user generated image and then wait for rest time
        # else burn base file and wait for rest time



        in_rgb = q_rgb.tryGet()
        in_nn = q_nn.tryGet()

        if in_rgb is not None:
            frame = in_rgb.getCvFrame()

        if in_nn is not None:
            detections = in_nn.detections

        if frame is not None:
            # Every 30 seconds check if there are any new arrivals
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

            for detection in detections:
                bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.imshow("preview", frame)

        if cv2.waitKey(1) == ord('q'):
            break
