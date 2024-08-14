from pathlib import Path
import cv2
import depthai
import numpy as np
from playsound import playsound
import time
import os
import random
import shutil
from datetime import datetime, timedelta
from burngcodefile import burn_gcode


# camera: people: count (prev & current)
# 


# Directory containing g code files
G_FOLDER = 'todaysgcodefiles'
destination_folder = 'burntfiles'

# port of grbl device check in dev folder usually /dev/ttyACM0
GRBL_port_path = '/dev/ttyACM0'


def get_gcode_files(folder_path):
    """Get a list of all gcode files in the given folder."""
    return [f for f in os.listdir(folder_path) if f.lower().endswith('.gcode')]

g_files = get_gcode_files(G_FOLDER)
if not g_files:
    print("No gcode files found in the directory.")
    return


random.shuffle(g_files)  # Shuffle the list to randomize the order

fcounter = 1  #filecounter for gcodefiles   

# Create the destination folder for burnt files if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

# playsound('/home/pi/depthai-python/atax/test/depthai-tutorials/2-face-detection-retail/audiofiles/bye.mp3')
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
# we are using context manager here that will dispose the device after we stop using it
with depthai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb")
    q_nn = device.getOutputQueue("nn")

    frame = None
    detections = []
    # inititalize previous people to zero
    prevpeople= 0
    nextplaytime=datetime.now()+timedelta(seconds=15)

    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)


    while True:
        in_rgb = q_rgb.tryGet()
        in_nn = q_nn.tryGet()

        if in_rgb is not None:
            frame = in_rgb.getCvFrame()

        if in_nn is not None:
            detections = in_nn.detections

        if frame is not None:
            # every 30 seconds check if there are any new arrivals
            now = datetime.now()
            if now >= nextplaytime:
                nextplaytime=now+timedelta(seconds=15)
                npeople=len(detections)
                if npeople > prevpeople:
                    # say hello by playing wav file and enter state 2 
                    playsound ('audiofiles/hello.mp3')
                    prevpeople = npeople
                    # start burning a file
                    print(f"burning: {g_files[fcounter]}")
                    g_path = os.path.join(G_FOLDER, g_files[fcounter])
                    burn_gcode(GRBL_port_path,g_path)
                    
                    # move file to burnt folder once its burnt
                    destination_file = os.path.join(destination_folder, g_files[fcounter])
                    print(f"done burning: {g_files[fcounter]}")
                    if os.path.isfile(g_path):
                        shutil.move(g_path, destination_file)
                        print(f"Moved '{g_files[fcounter]}' to '{destination_folder}'")
                    else:
                        print(f"'{g_files[fcounter]}' is not a file, skipping.")
                    fcounter += 1 # go to the next file
                    
                elif npeople < prevpeople:
                    # say bye by playing wav file
                    playsound('audiofiles/bye.mp3')
                    prevpeople = npeople
                elif npeople == 0:
                    # stay asleep play snoring noise
                    prevpeople = npeople 
                
            
            for detection in detections:
                bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
            cv2.imshow("preview", frame)
        # begin code
        # 
        
        
        
        if cv2.waitKey(1) == ord('q'):
            break
