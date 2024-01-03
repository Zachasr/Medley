# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 09:10:30 2023
Last Updated on Wed Jan 03 11:26:30 2024

@author: Alexis.Vivien
Display Mouse Location, Speed, Total Day Distance and Number of Clicks

Able to deploy as an executable from anaconda command prompt : (python39) C:\users\Alexis.Vivien\Documents\Python Scripts\Exercices pyinstaller --onefile MouseDistance.py
"""

import pyautogui, time
import math
import time
import sys
import numpy as np
import win32api
import cv2

running = True
dist = 0
n_clicks = -1
v = np.zeros(10)
ind = 0
dt = 0.01 # seconds
x, y, x_tmp, y_tmp = 0, 0, 0, 0
ds = 51/1920                              # = 0.0265625 cm per pixel  
boolCheck = True                                                              

class Printer():
    """Print things to stdout on one line dinamically"""
    def __init__(self,data):
        sys.stdout.write("\r"+data.__str__()) #\x1b[K
        sys.stdout.flush()

while(running):
    time.sleep(dt)
    
    if win32api.GetKeyState(0x01) < 0 and boolCheck : # Left button down = 0 or 1. Button up = -127 or -128
        n_clicks = n_clicks+2
        boolCheck = False
    if win32api.GetKeyState(0x01) > 0:
        boolCheck = True
        
    x_tmp, y_tmp = pyautogui.position()
    dist = dist + math.sqrt((x_tmp-x)**2 + (y_tmp-y)**2)
    v_inst = math.sqrt((x_tmp-x)**2 + (y_tmp-y)**2)*ds/100 / dt
    v[ind%10] = v_inst 
    output = "Lateral [px]: %d Longitudinal [px]: %d Total Distance [m]: %d Current speed [m/s]: %.2f # of Mouse Clicks [-]: %d " \
    % (x_tmp, y_tmp, int(dist*ds/100), np.mean(v), n_clicks)
    
    Printer(output)
    x, y = x_tmp, y_tmp 
    ind = ind + 1

     
    
