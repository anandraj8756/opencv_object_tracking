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

 #OpenCv version info
(major, minor) = cv2.__version__.split(".")[:2]   

 #if we are using opencv 3.2 or before 
 #function to create our object tracker
if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args["tracker"].upper())

  #for opencv 3.3 or newer 
else:
    OPENCV_OBJECT_TRACKERS = {
          "csrt":cv2.TrackerCSRT_create,
          "kcf":cv2.TrackerKCF_create,
          "boosting":cv2.TrackerBoosting_create,
          "mil":cv2.TrackerMIL_create,
          "tld":cv2.TrackerTLD_create,
          "medianflow":cv2.TrackerMedianFlow_create,
          "mosse":cv2.TrackerMOSSE_create,
      }



    

    tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

 #for bounding box cordinates of obj we are going
initBB = None

 #if video path is not pass then open automatic web cam
if not args.get("video", False):
    print("[INFO] starting video stream....")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)

else:
    vs = cv2.VideoCapture(args["video"])
#fps throught estimator
fps = None

#loop over frames from the video stream
while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    #resize the our frame
    #frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]


    #we are curently tracking on object
    if initBB is not None:
        (success, box) = tracker.update(frame)

        #if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #update the fps counter
        fps.update()
        fps.stop()

        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    #show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    #we are selecting the bounding box so press "s" and click enter or space
    #if you want again reselect then press escape
    if key == ord("s"):
        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

        tracker.init(frmae, initBB)
        fps = FPS().start()

    elif key == ord("q"):
        break

if not args.get("video", False):
    vs.stop()


else:
    vs.relase()

cv2.destroyAllWindows()    









