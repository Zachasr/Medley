# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:59:18 2021

@author: Alexis.Vivien
"""
import pyautogui, time
time.sleep(5)
pyautogui.click()    # click to put drawing program in focus
distance = 200
while distance > 0:
    pyautogui.dragRel(distance, distance/10, duration=.0001)   # move right
    distance = distance - 5
    pyautogui.dragRel(0, distance, duration=.0001)   # move down
    pyautogui.dragRel(-distance, -distance/10, duration=.0001)  # move left
    distance = distance - 5
    pyautogui.dragRel(0, -distance, duration=.0001)  # move up
       