# 3d-camera-project

## A project to replicate the effects of the Nishika N8000 3D film camera using webcams and digital image processing

This project uses three webcams to create a GIF with the 3D effect of rotating around the subject. Three identical 1080p webcams
(the ones I used were low-end, around $5 each but worked well) are placed on the screen of a laptop or on a monitor. All three are
plugged into USB ports on the computer.

(NOTE: this project can be extended to include more cameras, assuming you have more than three USB ports, which would make a better GIF. 
I couldn't get OpenCV to read multiple cameras over the same USB-C hub, even with threading, so I was stuck with three. 
If you figure out a way around it, let me know!)

When the script is run, all three cameras start capturing video. When the spacebar is pressed, a snapshot is taken from each camera
and saved to a new directory. These photos are then copied and processed using MediaPipe to landmark the position of the tip of the
nose of the subject. The photos are then cropped so that the tip of the nose is in the same location for each photo. They are
combined into a GIF, which is saved.

More functionality will likely be added to this program soon, so stay alert! Also, don't hesitate to fork the repo or email me if you have 
an idea for a feature.

Dependency list:
OpenCV (pip install opencv-python)
MediaPipe (pip install mediapipe)
os
time
shutil
