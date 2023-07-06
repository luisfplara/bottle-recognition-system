import tkinter as tk
import time
import threading
import cv2
class train_widget:
  
    def __init__(self, frame):
        self.train_button = tk.Button(frame,text="Add dataset", command=self.elements_window)
        self.train_button.pack(side = tk.TOP)
        self.frame = frame
        

        self.show_elements = False
        


        
     
    def create_elements(self):
        
        objetc_name_label = tk.Label(self.train_frame_elements,text ="Name")
        objetc_name_label.pack(side = tk.TOP)

        self.objetc_name_entry = tk.Entry(self.train_frame_elements, width = 20)
        self.objetc_name_entry.pack(side = tk.TOP)  

        frame1 = tk.Frame(self.train_frame_elements)
        frame1.pack( side = tk.TOP )

        self.shot_button = tk.Button(frame1,text="Capture")
        self.shot_button.pack(side = tk.LEFT)

        self.data_augmentation_button = tk.Button(frame1,text="DA")
        self.data_augmentation_button.pack(side = tk.LEFT)

        self.capture_count_label = tk.Label(self.train_frame_elements,text ="Capture count: 0")
        self.capture_count_label.pack(side = tk.TOP)

        self.captured_list = tk.Listbox(self.train_frame_elements)
        self.captured_list.pack(side = tk.TOP)

    def elements_window(self):
        self.train_frame_elements = tk.Toplevel(self.frame)
        self.train_frame_elements.geometry('150x150')
        self.create_elements()
        pass   
    #def show_hide_elements(self):
    #    self.show_elements = not(self.show_elements)
    #    if(self.show_elements):
    #        self.train_frame_elements.( side = tk.TOP )
    #    else:
    #        self.train_frame_elements.pack_forget()
        


        
          
        






    
