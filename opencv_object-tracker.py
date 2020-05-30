from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import time
import cv2

#construct the argument
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
    help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
    help="opencv object tracker type")
 args = vars(ap.parse_args())
 
    






