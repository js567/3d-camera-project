# DRAFT FOR CROPPING AND JOINING IMAGES - WILL BE INCORPORATED INTO MAIN FILE

import cv2
import mediapipe
import os
import shutil

# Test path for initial testing, later will be cwd
sub_parent = os.path.join(os.getcwd(), "2021.09.15_21.04.19")
print(sub_parent)
os.chdir(sub_parent)

crop_path = os.path.join(os.getcwd(), "crop_files")
cv_path = os.path.join(os.getcwd(), "cv_files")

# Remove existing crop files if they exist (mainly for testing)
if os.path.exists("crop_files"):
    shutil.rmtree(crop_path)

# Make new crop_files directory and save its path
os.mkdir("crop_files")
path = os.path.join(sub_parent, "crop_files")

# Remove existing CV files if they exist (mainly for testing)
if os.path.exists("cv_files"):
    shutil.rmtree(cv_path)

# Make new cv_files directory and save its path
os.mkdir("cv_files")
cv_path = os.path.join(sub_parent, "cv_files")

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
            crop_image = image.copy()
            os.chdir(path)
            crop_name = filename[:6] + "_crop" + filename[6:]
            cv2.imwrite(crop_name, crop_image)
            results = face.process(cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB))

            if results.multi_face_landmarks:

                for result in results.multi_face_landmarks:

                    for id, lm in enumerate(result.landmark):

                        h, w, c = crop_image.shape

                        if id == 1:
                            #print(id, lm)
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            print(filename, cx, cy)
                            print(w, h)
                            x_dict[crop_name] = cx
                            y_dict[crop_name] = cy

                    drawingModule.draw_landmarks(crop_image, result, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                                                 lineDrawingSpec)

                    cv_name = filename[:6] + "_cv" + filename[6:]
                    os.chdir(cv_path)
                    cv2.imwrite(cv_name, crop_image)

                    # cv2.imshow('Computer Vision Processing', image_cropped)
                    # cv2.waitKey(1)
                    # cv2.destroyWindow('Computer Vision Processing')

                    # plt.title('COMPUTER VISION PROCESSING')
                    # plt.imshow(image)

# Sort x and y dictionaries by value to find shortest distance to each edge for cropping
x_dict_sorted = dict(sorted(x_dict.items(), key=lambda x: x[1]))
y_dict_sorted = dict(sorted(y_dict.items(), key=lambda x: x[1]))

# print(x_dict_sorted)
# print(y_dict_sorted)

# Get name of files with tightest borders
smallest_x = list(x_dict_sorted.keys())[0]
smallest_y = list(y_dict_sorted.keys())[0]
largest_x = list(x_dict_sorted.keys())[2]
largest_y = list(y_dict_sorted.keys())[2]

# print(smallest_x, largest_x)
# print(smallest_y, largest_y)

x_l = x_dict_sorted[smallest_x]
x_r = w - x_dict_sorted[largest_x]
y_t = y_dict_sorted[smallest_y]
y_b = h - y_dict_sorted[largest_y]

print(x_l, x_r, y_t, y_b)

os.chdir(path)

# Calculate crop operations and perform unique operations on each file
for crop_filename in os.listdir(path):
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

