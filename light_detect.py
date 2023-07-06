import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
from components.cameraPositionControl import PositionControlPanel
from components.record import record_widget
from components.train import train_widget
from components.get_background import get_background
from components.detect import filterFrame
import threading
import time
import numpy as np


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
print(f'Exposure {cv2.CAP_PROP_EXPOSURE}')
#cap.set(cv2.CAP_PROP_EXPOSURE,2000)
print(f'Exposure new {cv2.CAP_PROP_EXPOSURE}')
capWidth = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capHeight = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

success, frame = cap.read()

mainWindow = tk.Tk(screenName="Camera Capture")
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())


#main frames
left_frame = tk.Frame(mainWindow, bg='blue',height = 1280, width = 720)
left_frame.pack(side = tk.LEFT)

right_frame = tk.Frame(mainWindow)
right_frame.pack(side = tk.RIGHT)

#left frame camera
camera1 = tk.Label(left_frame)
camera1.grid(row=0, column=0)

camera2 = tk.Label(left_frame)
camera2.grid(row=0, column=1)

camera3 = tk.Label(left_frame)
camera3.grid(row=1, column=0)

camera4 = tk.Label(left_frame)
camera4.grid(row=1, column=1)

record = record_widget(right_frame,frame)

train = train_widget(right_frame)

framenumber =0
dimension = (600,400)

rect_x = 640
back_ground = get_background("basicvideo.mp4")

cv2.imwrite('background.jpg',back_ground)

frame_to_check_list = [] 

def show_frame():
    global is_open, frame, framenumber
    is_open, frame = cap.read()
    if (record.recording):
        record.live_frame = frame
    framenumber+=1

    if(is_open):
        showCamera_conf_1(frame) 
        if  (len(frame_to_check_list)==5):
            cv2.imwrite('0.jpg', frame_to_check_list[0])
            cv2.imwrite('1.jpg', frame_to_check_list[1])
            cv2.imwrite('2.jpg', frame_to_check_list[2])
            cv2.imwrite('3.jpg', frame_to_check_list[3])
            cv2.imwrite('4.jpg', frame_to_check_list[4])
            classify_images(frame_to_check_list)
        showCamera(frame)
    #show_frame()

def classify_images(images_list):
    
    pass
    
def showCamera_conf_1(frame_in):
    global rect_x
    rect_x = 640
    #print(f"x:{rect_x}")
    
   


    frame_grey = cv2.cvtColor(frame_in[105:350, 0:640], cv2.COLOR_BGR2GRAY)
    background_grey = cv2.cvtColor(back_ground[105:350, 0:640], cv2.COLOR_BGR2GRAY)

    frame_diff = cv2.absdiff(frame_grey, background_grey)
    
    ret, thres = cv2.threshold(frame_diff, 80, 255, cv2.THRESH_BINARY)

    dilate_frame = cv2.dilate(thres, None, iterations=3)

    frame_filtered = frame_in[105:350, 0:640].copy()

    contours, hierarchy = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
      if cv2.contourArea(cnt) > 7000:
        cv2.drawContours(frame_filtered, contours, i, (0, 0, 255), 3)
        
        (x, y, w, h) = cv2.boundingRect(cnt)

        cv2.rectangle(frame_filtered, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rect_x = x

    cv2.line(frame_filtered, (185, 0), (185, 245),(255, 0, 0 ),3)

    if rect_x <185:
    
        if  (len(frame_to_check_list)<=5):
            frame_to_check_list.append(frame_in[105:350, 0:640])
        
    frame_filtered = cv2.resize(frame_filtered, dimension)
    prevImg = Image.fromarray(frame_filtered)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    camera2.imgtk = imgtk
    camera2.configure(image=imgtk)

    #frame_in = cv2.resize(frame_diff, dimension)
    frame_diff = cv2.resize(frame_diff, dimension)
    prevImg = Image.fromarray(frame_diff)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    camera3.imgtk = imgtk
    camera3.configure(image=imgtk)

    thres = cv2.resize(dilate_frame, dimension)
    prevImg = Image.fromarray(thres)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    camera4.imgtk = imgtk
    camera4.configure(image=imgtk)
    #camera2.after(10, show_frame)
            
def showCamera(frame_in):
    frame_original = cv2.resize(frame_in, dimension)
    cv2image = cv2.cvtColor(frame_original , cv2.COLOR_BGR2RGBA)
    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    camera1.imgtk = imgtk
    camera1.configure(image=imgtk)
    camera1.after(10, show_frame)

show_frame()
mainWindow.mainloop()