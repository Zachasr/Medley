# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 10:16:32 2022

This script is intended to load a dicom file and return frames at given time intervals

@author: Alexis.Vivien
"""
import tkinter
from tkinter import filedialog
import os
from os import listdir
from os.path import isfile, join
import pydicom as py
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import pydicom
import cv2
import os

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

def search_for_file_path ():
    currdir = os.getcwd()
    file_path = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a file')
    if len(file_path) > 0:
        print ("You chose: %s" % file_path)
    return file_path

file_path = search_for_file_path()
dcm_data = py.dcmread(file_path)
data = dcm_data.pixel_array
dim = data.shape
heart_rate = int(dcm_data.HeartRate)
frame_rate = heart_rate/60              # [Hz]
n_frames = dim[0]

frm1, frm2 = 10, 20       # num frames to start picking frames, num image beginning of plateau
dt1, dt2 = 1, 0           # num seconds to skip between each save
timestamp = frm1+np.around(np.array([*range(0,int(round((frm2-frm1)/(frame_rate))),dt1)])*frame_rate)
timestamp = timestamp.astype(int)

file_name = os.path.basename(file_path)[:-4]

if not os.path.isdir(file_name):
    os.mkdir(file_name)   # enlève l'extension .dcm

os.chdir(file_path[:-4])


for frame in timestamp:
    img = data[frame,:,:,:]
    final_img = Image.fromarray(img)

    
    # im = Image.fromarray(img)
    # im.save(os.getcwd() + str(frame) + '.jpg')
    # matplotlib.image.imsave(os.getcwd() + str(frame) + '.tiff',img, cmap='gray')
    # matplotlib.image.imsave(os.getcwd() + str(frame) + '.tiff',img[:,:,0], cmap='YlOrBr_r')
    # matplotlib.image.imsave(os.getcwd() + str(frame) + '.tiff',img @ [0.2989, 0.5870, 0.1140], cmap='gist_heat')
    

    



