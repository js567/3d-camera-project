# 3d-camera-project

## Replicating the effects of the Nishika N8000 3D film camera using webcams and digital image processing

### Background

<img src="https://user-images.githubusercontent.com/75865953/133840445-2cd9be74-6fbb-4a1a-901d-a964d3512bcc.png" width="500">
credit: https://www.youtube.com/watch?v=mIZ1JmxGOQE

The Nishika N8000 is a lenticular film camera produced in the 1980s. It uses four lenses to take photos from different perspectives
which can then be combined in different ways to produce 3D images. While it was never extremely popular during its production
run, it later gained more attention because it can be used to make GIFs with a 3D effect. 

Examples of GIFs made with the N8000:

<img src="https://user-images.githubusercontent.com/75865953/133842282-cab76bac-8a5b-4f52-b565-2c3ebc718555.gif" width="300"> <img src="https://user-images.githubusercontent.com/75865953/133843048-a6036e94-2912-4aa0-a291-febea2c95065.gif" width="300"> <img src="https://user-images.githubusercontent.com/75865953/133843057-fa6e1e22-856a-45fb-bb88-70d4b83a7ac5.gif" width="275">
https://giphy.com/search/nishika-n8000/

A friend of mine bought one recently, and we all loved the effect. However, the hands-on processing time for making
a GIF was long. The photos had to be developed and scanned, and then processed to line up the photos around a single point, such as
the nose of the person in the foreground. Film also is not as accessible and inexpensive as it used to be. 

Hence, a digital replica of this camera was conceived. 

### Setup

This project uses three webcams to create a GIF with the 3D effect of rotating around the subject. Three identical 1080p webcams
(the ones I used were low-end, around $5 each but worked well) are placed on the screen of a laptop or on a monitor. All three are
plugged into USB ports on the computer.

(NOTE: this project can be extended to include more cameras, assuming you have more than three USB ports, which would make a better GIF. 
I was having issues in OpenCV when I tried to stream multiple cameras over the same USB-C hub, even with threading, so I was stuck with three. 
If you figure out a way around it, let me know!)

When the script is run, all three cameras start capturing video. When the spacebar is pressed, a snapshot is taken from each camera
and saved to a new directory. These photos are then copied and processed using MediaPipe to landmark the position of the tip of the
nose of the subject. The photos are then cropped so that the tip of the nose is in the same location for each photo. They are
combined into a GIF, which is saved.

Python dependency list: OpenCV, MediaPipe, os, time, shutil, PIL Image, glob

### Outcome



The end result of the program is somewhat less smooth than the film camera, but I believe that it is largely due to the number of 
cameras/apertures involved. An interesting follow-up would include using a fourth camera to more closely resemble the output of 
the film camera or even push it farther by using five or six cameras at a desktop.

A friend of mine had the idea of running the system on a Raspberry Pi which would be a lot more portable than the current configuration.
My concern with this is that the image processing might not run fast enough to be useful, but it could always just capture photos to 
be processed later on another device.
