# DRAFT FOR CROPPING AND JOINING IMAGES - WILL BE INCORPORATED INTO MAIN FILE

import cv2
import mediapipe
import os
import shutil

# Test path for initial testing, later will be cwd
sub_parent = os.path.join(os.getcwd(), "2021.09.15_00.08.53")
print(sub_parent)
os.chdir(sub_parent)
crop_path = os.path.join(os.getcwd(), "crop_files")


# Remove existing crop files if they exist (mainly for testing)
if os.path.exists("crop_files"):
    shutil.rmtree(crop_path)

# Make new crop_files directory and save its path
os.mkdir("crop_files")
path = os.path.join(sub_parent, "crop_files")

# MediaPipe computer vision modules
drawingModule = mediapipe.solutions.drawing_utils
faceModule = mediapipe.solutions.face_mesh

# Color and shape options for face mesh
circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(255, 0, 0))

x_dict = {}
y_dict = {}

for filename in os.listdir(sub_parent):
    if os.getcwd() != sub_parent:
        os.chdir(sub_parent)
    if filename.endswith(".png"):
        with faceModule.FaceMesh(static_image_mode=True) as face:
            image = cv2.imread(filename)
            #print(image)
            #cv2.imshow('test', image)
            #cv2.waitKey(0)
            image_cropped = image.copy()
            os.chdir(path)
            crop_name = filename[:6] + "_crop" + filename[6:]
            cv2.imwrite(crop_name, image_cropped)
            results = face.process(cv2.cvtColor(image_cropped, cv2.COLOR_BGR2RGB))

            if results.multi_face_landmarks:

                for result in results.multi_face_landmarks:

                    for id, lm in enumerate(result.landmark):

                        h, w, c = image_cropped.shape

                        if id == 1:
                            print(h, w)
                            print(id, lm)
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            print(cx, cy)
                            x_dict[crop_name] = cx
                            y_dict[crop_name] = cy

                    # drawingModule.draw_landmarks(image_cropped , result, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                    #                              lineDrawingSpec)

                    #plt.title('COMPUTER VISION PROCESSING')
                    #plt.imshow(image)

                    # cv2.imshow('Computer Vision Processing', image)
                    # cv2.waitKey(0)
                    # cv2.destroyWindow('Computer Vision Processing')

# Sort x and y dictionaries by value to find shortest distance to each edge for cropping
x_dict_sorted = dict(sorted(x_dict.items(), key=lambda x: x[1]))
y_dict_sorted = dict(sorted(y_dict.items(), key=lambda x: x[1]))

# Get name of files with tightest borders
smallest_x = list(x_dict_sorted.keys())[0]
smallest_y = list(y_dict_sorted.keys())[0]
largest_x = list(x_dict_sorted.keys())[2]
largest_y = list(y_dict_sorted.keys())[2]

print('test')
print(smallest_x, largest_x)

for filename in os.listdir(path):
    if filename.endswith(".png"):
        print(filename)
        print(x_dict_sorted[filename])
        print(y_dict_sorted[filename])

        # if filename != smallest_x:
        #     cropped = filename[80:280, 150:330].copy()

