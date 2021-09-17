# MAIN CODE FOR VIDEO CAPTURE
# Jack Stevenson 2021

# standardization:
# connect webcams left to right 0 to 2

# next steps:
# gif construction
# gif playback speed and boomerang

# future ideas:
# add gridlines and all control info (timer, spacebar instructions, etc.) onto viewfinder photo
# strategy for multiple people
# email product to people
# watermark on gifs
# style/filter effects
# write in C++ (likely not worth the time)
# how well will it work with masks?
# launch some functions for simplicity with if name main

import cv2
import os
import time
from mediapipe import solutions
import shutil
from PIL import Image
import glob
import numpy
import datetime
import threading

# capture from 3 connected webcams - adjust resolution to 1080p - MIGHT NEED TO CHANGE ORDER/WEBCAM NUMBER
cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cap3 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Check if the webcam is opened correctly
if not cap1.isOpened() or not cap2.isOpened() or not cap3.isOpened():
    raise IOError("Cannot open webcams")

# Display and image processing loop
while True:

    ret, frame1 = cap1.read()
    frame1_r = cv2.resize(frame1, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame1_r)

    ret, frame2 = cap2.read()
    frame2_r = cv2.resize(frame2, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input2', frame2_r)

    ret, frame3 = cap3.read()
    frame3_r = cv2.resize(frame3, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input3', frame3_r)

    c = cv2.waitKey(1)

    # Spacebar (ASCII 32) takes an image from webcams and save to directory
    if c == 32:

        print("Processing photos")
        initial = time.time()

        # Create a new directory with a timestamp to save the photos
        new_dir = str(time.strftime("%Y.%m.%d_%H.%M.%S"))
        parent = os.getcwd()
        path = os.path.join(parent, new_dir)
        os.mkdir(path)
        os.chdir(path)

        cv2.imwrite('frame1.png', frame1)
        cv2.imwrite('frame2.png', frame2)
        cv2.imwrite('frame3.png', frame3)

        # Create two new paths for crop and CV files
        crop_path = os.path.join(os.getcwd(), "crop_files")
        cv_path = os.path.join(os.getcwd(), "cv_files")

        # Remove existing crop files if they exist (mainly for testing)
        if os.path.exists("crop_files"):
            shutil.rmtree(crop_path)

        # Make new crop_files directory and save its path
        os.mkdir("crop_files")
        crop_path = os.path.join(path, "crop_files")

        # Remove existing CV files if they exist (mainly for testing)
        if os.path.exists("cv_files"):
            shutil.rmtree(cv_path)

        # Make new cv_files directory and save its path
        os.mkdir("cv_files")
        cv_path = os.path.join(path, "cv_files")

        # MediaPipe computer vision modules
        drawingModule = solutions.drawing_utils
        faceModule = solutions.face_mesh

        # Color and shape options for face mesh
        circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
        lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(255, 0, 0))

        x_dict = {}
        y_dict = {}

        # Find nose in each photo and save coordinates to dictionary
        for filename in os.listdir(path):

            if os.getcwd() != path:
                os.chdir(path)

            if filename.endswith(".png"):

                with faceModule.FaceMesh(static_image_mode=True) as face:
                    image = cv2.imread(filename)
                    crop_image = image.copy()
                    os.chdir(crop_path)
                    crop_name = filename[:6] + "_crop" + filename[6:]
                    cv2.imwrite(crop_name, crop_image)
                    results = face.process(cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB))

                    if results.multi_face_landmarks:

                        for result in results.multi_face_landmarks:

                            for id, lm in enumerate(result.landmark):
                                h, w, c = crop_image.shape

                                if id == 1:
                                    cx, cy = int(lm.x * w), int(lm.y * h)
                                    print(filename, cx, cy)
                                    print(w, h)
                                    x_dict[crop_name] = cx
                                    y_dict[crop_name] = cy

                            drawingModule.draw_landmarks(crop_image, result, faceModule.FACEMESH_CONTOURS,
                                                         circleDrawingSpec,
                                                         lineDrawingSpec)
                            cv_name = filename[:6] + "_cv" + filename[6:]
                            os.chdir(cv_path)
                            cv2.imwrite(cv_name, crop_image)

                            # cv2.imshow('Computer Vision Processing', image_cropped)
                            # cv2.waitKey(1)
                            # cv2.destroyWindow('Computer Vision Processing')

                            # plt.title('COMPUTER VISION PROCESSING')
                            # plt.imshow(image)

        # Create CV image to display
        os.chdir(cv_path)
        cv_1 = cv2.imread('frame1_cv.png')
        cv_1 = cv2.resize(cv_1, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        cv_2 = cv2.imread('frame2_cv.png')
        cv_2 = cv2.resize(cv_2, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        cv_3 = cv2.imread('frame3_cv.png')
        cv_3 = cv2.resize(cv_3, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
        landscape = numpy.concatenate((cv_1, cv_2, cv_3), axis=1)

        # Sort x and y dictionaries by value to find shortest distance to each edge for cropping
        x_dict_sorted = dict(sorted(x_dict.items(), key=lambda x: x[1]))
        y_dict_sorted = dict(sorted(y_dict.items(), key=lambda x: x[1]))

        # Get name of files with tightest borders
        smallest_x = list(x_dict_sorted.keys())[0]
        smallest_y = list(y_dict_sorted.keys())[0]
        largest_x = list(x_dict_sorted.keys())[2]
        largest_y = list(y_dict_sorted.keys())[2]

        x_l = x_dict_sorted[smallest_x]
        x_r = w - x_dict_sorted[largest_x]
        y_t = y_dict_sorted[smallest_y]
        y_b = h - y_dict_sorted[largest_y]

        print(x_l, x_r, y_t, y_b)

        os.chdir(crop_path)

        # Calculate crop operations and perform unique operations on each file
        for crop_filename in os.listdir(crop_path):

            if crop_filename.endswith(".png"):
                crop_file = cv2.imread(crop_filename)
                print(crop_filename)

                if crop_filename != smallest_x:
                    crop_file = cv2.imread(crop_filename)
                    left_crop = x_dict_sorted[crop_filename] - x_l
                    cropped = crop_file[:, left_crop:]
                    cv2.imwrite(crop_filename, cropped)

                if crop_filename != largest_x:
                    crop_file = cv2.imread(crop_filename)
                    right_crop = x_dict_sorted[crop_filename] + x_r - (x_dict_sorted[crop_filename] - x_l)
                    cropped = crop_file[:, :right_crop]
                    cv2.imwrite(crop_filename, cropped)

                if crop_filename != smallest_y:
                    crop_file = cv2.imread(crop_filename)
                    top_crop = y_dict_sorted[crop_filename] - y_t
                    cropped = crop_file[top_crop:, :]
                    cv2.imwrite(crop_filename, cropped)

                if crop_filename != largest_y:
                    crop_file = cv2.imread(crop_filename)
                    bottom_crop = y_dict_sorted[crop_filename] + y_b - (y_dict_sorted[crop_filename] - y_t)
                    cropped = crop_file[:bottom_crop, :]
                    cv2.imwrite(crop_filename, cropped)

                print(cropped.shape)

        # Code to 'boomerang' each GIF by adding middle frame to end of crop_files
        frame4 = cv2.imread('frame2_crop.png')
        cv2.imwrite('frame4_crop.png', frame4)

        # Create the frames
        frames = []
        imgs = glob.glob("*.png")
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)

        # Save into a GIF file that loops forever
        frames[0].save('gif.gif', format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=230, loop=0)

        # Show GIF image
        os.startfile('gif.gif')

        final = time.time()
        elapsed = str(final - initial)
        print("Done processing: " + elapsed)

        cv_window_name = "Computer Vision"
        cv2.imshow(cv_window_name, landscape)
        cv2.waitKey(0)
        cv2.destroyWindow(cv_window_name)

    # Escape key (ASCII 27) stops program
    if c == 27:
        cap1.release()
        cap2.release()
        cap3.release()
        cv2.destroyAllWindows()
        break

print("Program ended")
