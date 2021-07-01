# MAIN CODE FOR VIDEO CAPTURE

# next steps:
# use file as a module and make class for camera control
# make a GUI that has viewfinder display and buttons

import cv2
import tkinter
import datetime

# capture from 4 connected webcams
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
#cap3 = cv2.VideoCapture(3)
#cap3 = cv2.VideoCapture(4)

# # Check if the webcam is opened correctly
# if not cap1.isOpened() or not cap2.isOpened():
#     raise IOError("Cannot open webcams")

# infinite display loop - try better control structure
while True:
    ret, frame1 = cap1.read()
    frame1 = cv2.resize(frame1, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame1)

    ret, frame2 = cap2.read()
    frame2 = cv2.resize(frame2, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input2', frame2)

    # ret, frame3 = cap3.read()
    # frame3 = cv2.resize(frame3, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    # cv2.imshow('Input3', frame3)

    c = cv2.waitKey(1)

    # on spacebar (ASCII 32) take an image from webcams and save to directory
    # would be smart to add a real file path and folder based on datetime for organization
    if c == 32:
        cv2.imwrite('frame1.png', frame1)
        cv2.imwrite('frame2.png', frame2)
        # cv2.imwrite('frame1.png', frame3)
        # cv2.imwrite('frame1.png', frame4)

    # break loop on escape - janky and crashes program, find a better way to do it
    if c == 27:
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()