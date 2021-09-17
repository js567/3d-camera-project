# 3d-camera-project

## A project to replicate the effects of the Nishika N8000 3D film camera using webcams and digital image processing

### Background

![image](https://user-images.githubusercontent.com/75865953/133840445-2cd9be74-6fbb-4a1a-901d-a964d3512bcc.png)
credit: https://www.youtube.com/watch?v=mIZ1JmxGOQE

The Nishika N8000 is a lenticular film camera produced in the 1980s. It uses four lenses to take photos from different perspectives
which can then be combined in different ways to produce 3D images. While it was never extremely popular during its production
run, and the company later went out of business due to a profiteering scheme, it gained a lot of attention in the past two decades 
as it can be used to produce GIFs with a 3D effect. 

![n8000](https://user-images.githubusercontent.com/75865953/133842282-cab76bac-8a5b-4f52-b565-2c3ebc718555.gif)
<img src="https://user-images.githubusercontent.com/75865953/133842282-cab76bac-8a5b-4f52-b565-2c3ebc718555.gif" width="20">



credit: https://www.psnwa.org/ws/nishika-n8000/

A friend of mine bought one recently, and we all thought that the effect was great. However, the hands-on processing time for making
a GIF was long. The photos had to be developed and scanned, and then processed to line up the photos around a single point, such as
the nose of the person in the foreground. Film also is not as accessible and inexpensive as it used to be. 

Hence, the digital replica of this camera was conceived. 

### Setup

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

Python dependency list: OpenCV (pip install opencv-python), MediaPipe (pip install mediapipe), os, time, shutil
