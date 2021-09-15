# MAIN CODE FOR VIDEO CAPTURE

# next steps:

# use file as a module and make class for camera control
# make a GUI that has viewfinder display and buttons

import cv2
import os
import time
import mediapipe
import glob
import tkinter
import datetime
import threading

# capture from 3 connected webcams - adjust resolution to 1080p
cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)
cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# # Check if the webcam is opened correctly
# if not cap1.isOpened() or not cap2.isOpened():
#     raise IOError("Cannot open webcams")

# infinite display loop - try better control structure
while True:
    ret, frame1 = cap1.read()
    frame1 = cv2.resize(frame1, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame1)

    ret, frame2 = cap2.read()
    # frame2 = cv2.resize(frame2, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input2', frame2)
    # cap2.release()


    ret, frame3 = cap3.read()
    # frame3 = cv2.resize(frame3, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input3', frame3)
    # cap3.release()

    c = cv2.waitKey(1)

    # on spacebar (ASCII 32) take an image from webcams and save to directory
    # would be smart to add a real file path and folder based on datetime for organization
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

                            #drawingModule.draw_landmarks(image, result, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                            #                             lineDrawingSpec)
                            #cv2.imshow('Computer Vision Processing', image)
                            #cv2.waitKey(10000)
                            #cv2.destroyWindow('Computer Vision Processing')

        print(x_dict, y_dict)

        os.chdir(parent)

        final = time.time()
        elapsed = str(final - initial)

        print("Done processing: " + elapsed)

    if c == 27:
        cap1.release()
        cap2.release()
        cap3.release()

        cv2.destroyAllWindows()

        break

print("Finished")
