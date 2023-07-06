import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
import threading
import time
import numpy as np


class dataset(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.captured_frames=[]


        self.left_frame = tk.Frame(self, bg='blue',height = 1280, width = 720)
        self.left_frame.pack(side = tk.LEFT)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side = tk.RIGHT)

        self.camera1 = tk.Label(self.left_frame)
        self.camera1.pack(side = tk.TOP)

        self.bottle_name_label = tk.Label(self.right_frame,text ="Bottle Name")
        self.bottle_name_label.pack(side = tk.TOP)

        self.bottle_name = tk.Entry(self.right_frame, width = 20)
        self.bottle_name.pack(side = tk.TOP)  

        self.capture = tk.Button(self.right_frame,text="Capture",command=self.capture_frame)
        self.capture.pack(side = tk.TOP)

        self.captured_list = tk.Listbox(self.right_frame)
        self.captured_list.pack(side = tk.TOP)

        self.save_delete_frame = tk.Frame(self.right_frame)
        self.save_delete_frame.pack(side = tk.TOP)

        self.save = tk.Button(self.save_delete_frame,text="Save",command=self.save_training)
        self.save.pack(side = tk.LEFT)

        self.save = tk.Button(self.save_delete_frame,text="Save for test",command=self.save_test)
        self.save.pack(side = tk.LEFT)


        self.delete = tk.Button(self.save_delete_frame,text="Delete",command=self.delete_captures)
        self.delete.pack(side = tk.LEFT)

        self.delete = tk.Button(self.right_frame,text="Menu",command=lambda:controller.show_frame(controller.StartPage))
        self.delete.pack(side = tk.TOP)

        #thread = threading.Thread(target=self.open_camera, daemon=True)
        #thread.start()
        self.image_count = 0
        self.opened = False
        self.dimension = (600,400)
        
        self.showCamera()
    def open_camera(self):
        if(not self.opened):
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.capWidth = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.capHeight = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.opened = True
        

    def showCamera(self):

        global frame_original
        if(self.controller.actual_frame==self.__class__):
            self.open_camera()
            is_open,frame_original = self.cap.read()
            cv2.rectangle(frame_original, (0, 105), (640, 350), (0, 255, 0), 2)

            cv2image = cv2.cvtColor(frame_original , cv2.COLOR_BGR2RGBA)
            prevImg = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=prevImg)
            self.camera1.imgtk = imgtk
            self.camera1.configure(image=imgtk)
        if(self.opened and self.controller.actual_frame!=self.__class__):
            self.opened = False
            self.cap.release()
        self.camera1.after(10, self.showCamera)
    
    def check_qtd_images(self):
        dir_name = f'dataset/{self.bottle_name.get()}'
        for element in os.listdir(dir_name):
            self.image_count+=1
            
        print(self.image_count)


    def capture_frame(self):
        self.bottle_name.config(state= "disabled")
        
        name = f'{self.bottle_name.get()}_{len(self.captured_frames)}.png'
        self.captured_frames.append(frame_original)
        self.captured_list.insert(tk.END,name)
        print(np.asarray(self.captured_frames).shape)

    def delete_captures(self):
        self.captured_frames.clear()
        self.captured_list.delete(0, tk.END)
        self.bottle_name.config(state= "normal")

    def save_training(self):
        
        if(len(self.captured_frames)>0):
            images_count = 0;    
            dir_name = f'dataset/{self.bottle_name.get()}'
            
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
                
            else :
                self.check_qtd_images()
            for idx,frames in enumerate(self.captured_frames):
                name = f'{dir_name}/{self.bottle_name.get()}_{self.image_count+idx}.png'
            
                cv2.imwrite(name, frames[105:350, 0:640])
                
                print(name)
                print(f'frame {idx}: {np.asarray(frames).shape}')
            self.image_count =0
            self.captured_frames.clear()
            self.captured_list.delete(0, tk.END)
            self.bottle_name.config(state= "normal")
    def save_test(self):
        
        if(len(self.captured_frames)>0):
            images_count = 0;    
            dir_name = f'dataset_test/{self.bottle_name.get()}'
            
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
                
            else :
                self.check_qtd_images()
            for idx,frames in enumerate(self.captured_frames):
                name = f'{dir_name}/{self.bottle_name.get()}_{self.image_count+idx}.png'
            
                cv2.imwrite(name, frames[105:350, 0:640])
                
                print(name)
                print(f'frame {idx}: {np.asarray(frames).shape}')
            self.image_count =0
            self.captured_frames.clear()
            self.captured_list.delete(0, tk.END)
            self.bottle_name.config(state= "normal")

