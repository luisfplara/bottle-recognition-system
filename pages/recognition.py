from decimal import ROUND_DOWN, Decimal
import tkinter as tk

import cv2

from PIL import Image, ImageTk
import numpy as np

from keras.preprocessing import image
from components.get_background import get_background
from keras.utils import load_img,img_to_array
from keras.models import load_model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
import time
from tkinter import ttk
import threading

class recognition(tk.Frame):
  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.captured_frames=[]


        self.left_frame = tk.Frame(self, bg='blue',height = 1280, width = 720)
        self.left_frame.pack(side = tk.LEFT)
        self.classes = ['A','B','C','D','H','I', 'J']
        self.bottle_counter = [0,0,0,0,0,0,0,0,0,0]
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side = tk.RIGHT)

        self.camera1 = tk.Label(self.left_frame)
        self.camera1.pack(side = tk.TOP)

        

        self.start_reco_btn = tk.Button(self.right_frame, text='Start', command= self.start_recognition, background='green' )
        self.start_reco_btn.pack(side= tk.TOP)

        self.capture_list = tk.Listbox(self.right_frame)
        self.capture_list.pack(side = tk.TOP)

        button_frame = tk.Frame(self.right_frame)
        self.progress_bar = ttk.Progressbar(button_frame, orient='horizontal',mode='indeterminate',length=100)
        #self.progress_bar.grid(column=0, row=0)
        button_frame.pack(side= tk.TOP)

        self.preview_frame = tk.Frame(self.right_frame)

        self.captured_label = tk.Label(self.preview_frame, text='Captured')
        self.captured_label.pack(side = tk.TOP)
        self.captured_img = tk.Label(self.preview_frame)
        self.captured_img.pack(side = tk.TOP)

        self.response_label = tk.Label(self.preview_frame, text='Detected')
        self.response_label.pack(side = tk.TOP)
        self.response_img = tk.Label(self.preview_frame)
        self.response_img.pack(side = tk.TOP)

        self.star_time = 0
        self.finish_time = 0


        self.back_ground = get_background("basicvideo.mp4")

        self.start_reco = False
       
        self.opened = False
        self.dimension = (600,400)
        
        self.showCamera()
    def start_recognition (self):

        self.start_reco = not self.start_reco 
        if(self.start_reco):
            self.start_reco_btn['text'] = 'Stop'
            self.start_reco_btn['background'] = 'red'
        else:
            self.start_reco_btn['text'] = 'Start'
            self.start_reco_btn['background'] = 'green'
    
            pass
    def open_camera(self):
        if(not self.opened):
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.capWidth = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.capHeight = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.opened = True  



    def showCamera(self):

        global frame_original
        rect_x = 640
        if(self.controller.actual_frame==self.__class__):
            self.open_camera()
            is_open,frame_original = self.cap.read()

            frame_grey = cv2.cvtColor(frame_original[105:350, 0:640], cv2.COLOR_BGR2GRAY)
            background_grey = cv2.cvtColor(self.back_ground[105:350, 0:640], cv2.COLOR_BGR2GRAY)
            frame_diff = cv2.absdiff(frame_grey, background_grey)
    
            ret, thres = cv2.threshold(frame_diff, 80, 255, cv2.THRESH_BINARY)

            dilate_frame = cv2.dilate(thres, None, iterations=3)

            frame_filtered = frame_original[105:350, 0:640].copy()

            contours, hierarchy = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
           
            for i, cnt in enumerate(contours):
              
              if cv2.contourArea(cnt) > 7000:
                #cv2.drawContours(frame_filtered, contours, i, (0, 0, 255), 3)

                (x, y, w, h) = cv2.boundingRect(cnt)

                cv2.rectangle(frame_filtered, (x, y), (x+w, y+h), (0, 255, 0), 2)
                rect_x = x

            
            
            cv2.line(frame_filtered, (100, 0), (100, 245),(255, 0, 0 ),3)
  
            
            if rect_x <100 and self.start_reco:
                
                print("Reconhendo.....")

                self.progress_bar.grid(column=0, row=0)
                self.start_reco = False
                self.progress_bar.start()
                self.star_time = time.time()
                reco_thread = threading.Thread(target=self.recognize,args=(frame_original,), daemon=True)
                reco_thread.start()

                time.sleep(2)
                
        
            frame_filtered = cv2.resize(frame_filtered, self.dimension)
            prevImg = Image.fromarray(frame_filtered)
            imgtk = ImageTk.PhotoImage(image=prevImg)
            self.camera1.imgtk = imgtk
            self.camera1.configure(image=imgtk)


        if(self.opened and self.controller.actual_frame!=self.__class__):
            self.opened = False
            self.cap.release()
        self.camera1.after(10, self.showCamera)
    
    

    def predict(self,model, img):
       

        x = img_to_array(img)
        x = img
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        return preds[0]
    


    def recognize(self, frame_in):
        model = load_model('MobileNetV2.model')

        frame = np.asanyarray(frame_in[105:350, 0:640])

        
        cv2.imwrite('teste.png',frame)
    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #img = load_img('teste.png', target_size=(245, 649))
       


        preds = self.predict(model, frame)

        preds = preds*100

        self.bottle_counter[preds.argmax()]+=1
        self.capture_list.delete(0,tk.END)
        for idx,a in enumerate(preds):
            self.capture_list.insert("end", f'{self.classes[idx]} : {self.bottle_counter[idx]}')
            print(f'{self.classes[idx]}: {a}')
        
        self.start_reco = not self.start_reco
        print(f'pos: {preds.argmax()} label: {self.classes[preds.argmax()]}')

        self.progress_bar.stop()
        self.progress_bar.grid_forget()

        aux = '{0:.2f}'.format(preds[preds.argmax()])
        self.response_label['text'] = f'Detected {self.classes[preds.argmax()]} precisão: {aux}'
        img_load = cv2.imread(f'dataset/{self.classes[preds.argmax()]}/{self.classes[preds.argmax()]}_30.png')
        img_load = cv2.cvtColor(img_load, cv2.COLOR_BGR2RGB)
        img_load = cv2.resize(img_load,(130,50))
        prevImg = Image.fromarray(img_load)
        imgtk = ImageTk.PhotoImage(image=prevImg)
        self.response_img.imgtk = imgtk
        self.response_img.configure(image=imgtk)
        


        img_load = cv2.resize(frame,(130,50))
        prevImg = Image.fromarray(img_load)
        imgtk = ImageTk.PhotoImage(image=prevImg)
        self.captured_img.imgtk = imgtk
        self.captured_img.configure(image=imgtk)

        self.preview_frame.pack(side=tk.TOP)
        self.finish_time = time.time()

        print(f'PROCESSSS time: {self.finish_time - self.star_time}')

    

    def delete_captures(self):
        self.captured_frames.clear()
        self.captured_list.delete(0, tk.END)
        self.bottle_name.config(state= "normal")


