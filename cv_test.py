# MAIN CODE FOR VIDEO CAPTURE
# Jack Stevenson 2021


# standardization:
# connect webcams left to right 0 to 2

# next steps:
# new 1080p capture for testing
# cropping method
# check that photos are all the same size and landmarks are in the same place for each photo
# gif construction
# gif playback speed and boomerang

# future ideas:
# add gridlines and all control info (timer, spacebar instructions, etc.) onto viewfinder photo
# strategy for multiple people
# email product to people
# watermark on gifs
# style/filter effects
# write in C++ (likely not worth the time)

import cv2
import os
import time
import mediapipe
import shutil
import matplotlib as plt
import glob
import tkinter
import datetime
import threading

# capture from 3 connected webcams - adjust resolution to 1080p - MIGHT NEED TO CHANGE ORDER/WEBCAM NUMBER
cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap3 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Check if the webcam is opened correctly
if not cap1.isOpened() or not cap2.isOpened() or not cap3.isOpened():
    raise IOError("Cannot open webcams")

# Display and image processing loop
while True:

    ret, frame1 = cap1.read()
    frame1_r = cv2.resize(frame1, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame1_r)

    ret, frame2 = cap2.read()
    frame2_r = cv2.resize(frame2, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input2', frame2_r)

    ret, frame3 = cap3.read()
    frame3_r = cv2.resize(frame3, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input3', frame3_r)

    c = cv2.waitKey(0)

    # Spacebar (ASCII 32) takes an image from webcams and save to directory
    if c == 32:

        print("Processing photos")
        initial = time.time()

        new_dir = str(time.strftime("%Y.%m.%d_%H.%M.%S"))
        parent = os.getcwd()

        path = os.path.join(parent, new_dir)
        os.mkdir(path)
        os.chdir(path)

        cv2.imwrite('frame1.png', frame1)
        cv2.imwrite('frame2.png', frame2)
        cv2.imwrite('frame3.png', frame3)

        drawingModule = mediapipe.solutions.drawing_utils
        faceModule = mediapipe.solutions.face_mesh

        circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
        lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(255, 0, 0))

        x_dict = {}
        y_dict = {}

        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".png"):
                with faceModule.FaceMesh(static_image_mode=True) as face:
                    image = cv2.imread(os.path.join(path, filename))
                    results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    if results.multi_face_landmarks:
                        for result in results.multi_face_landmarks:
                            for id, lm in enumerate(result.landmark):
                                h, w, c = image.shape

                                if id == 1:
                                    print(h, w)
                                    print(id, lm)
                                    cx, cy = int(lm.x * w), int(lm.y * h)
                                    print(cx, cy)
                                    x_dict[filename] = cx
                                    y_dict[filename] = cy

                            drawingModule.draw_landmarks(image, result, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                                                         lineDrawingSpec)

                            #plt.title('COMPUTER VISION PROCESSING')
                            #plt.imshow(image)

                            #cv2.imshow('Computer Vision Processing', image)
                            #cv2.waitKey(10000)
                            #cv2.destroyWindow('Computer Vision Processing')

        print(x_dict, y_dict)

        os.chdir(parent)

        final = time.time()
        elapsed = str(final - initial)

        print("Done processing: " + elapsed)

    # Escape key (ASCII 27) stops program
    if c == 27:
        cap1.release()
        cap2.release()
        cap3.release()
        cv2.destroyAllWindows()
        break

print("Program ended")
