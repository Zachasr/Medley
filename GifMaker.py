# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:27:23 2022

@author: Alexis.Vivien
"""

import glob
from PIL import Image
def make_gif(frame_folder):
    frames = (Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.jpg")))
    frame_one = next(frames)
    frame_one.save(fp="my_awesome.gif", format='GIF', append_images=frames,
               save_all=True,optimize=False, duration=200, loop=0)
    
if __name__ == "__main__":
    make_gif("C:/Users/alexis.vivien/Documents/MATLAB/3Dplot/Gif pictures")