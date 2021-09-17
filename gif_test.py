import os

from PIL import Image
import glob

directory = "C:/Users/jack/PycharmProjects/opencv-recognition-project/2021.09.15_22.15.17/crop_files"
os.chdir(directory)

# Create the frames
frames = []
imgs = glob.glob("*.png")
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save('png_to_gif.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=300, loop=0)