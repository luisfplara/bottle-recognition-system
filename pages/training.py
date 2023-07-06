import tkinter as tk
import os
import cv2

from PIL import Image, ImageTk

import numpy as np



class training(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.frame = tk.Frame(self)
        self.frame.pack()

        self.training_frame = tk.Frame(self.frame)
        self.training_frame.pack(side=tk.TOP)
        dataset_training_label = tk.Label(self.training_frame,text="Dataset Images")
        dataset_training_label.pack(side = tk.TOP)


        self.labels_training_frame = tk.Frame(self.training_frame)
        self.labels_training_frame.pack(side=tk.LEFT)

        input_training_labels_label = tk.Label(self.labels_training_frame,text="Labels")
        input_training_labels_label.pack(side = tk.TOP)

        self.input_training_label_list = tk.Listbox(self.labels_training_frame,selectmode=tk.SINGLE,exportselection=0)
        self.input_training_label_list.pack(side = tk.TOP)
        self.input_training_label_list.bind('<<ListboxSelect>>', self.onselect_label)

      
        self.images_training_frame = tk.Frame(self.training_frame)
        self.images_training_frame.pack(side=tk.LEFT)

        input_training_images_label = tk.Label(self.images_training_frame,text="Training")
        input_training_images_label.pack(side = tk.TOP)

        self.input_training_images_list = tk.Listbox(self.images_training_frame,selectmode=tk.SINGLE)
        self.input_training_images_list.pack(side = tk.TOP)


        self.images_button_frame = tk.Frame(self.training_frame)
        self.images_button_frame.pack(side=tk.LEFT)

        self.train_button = tk.Button(self.images_button_frame,text="Train",command=None, height=1, width=5)
        self.train_button.pack(side = tk.TOP)

        self.menu = tk.Button(self.frame,text="Menu",command=lambda:controller.show_frame(controller.StartPage))
        self.menu.pack(side = tk.BOTTOM)
        self.update_button = tk.Button(self.frame,text="Delete",command=self.load_labels)
        self.update_button.pack(side = tk.TOP)

        self.load_labels()

    def onselect_label(self,evt):
        selection = evt.widget.curselection()
        if selection:
            index = int(selection[0])
            value = evt.widget.get(index)
            path = f"dataset/{value}"
            dirs = os.listdir( path )
            self.input_training_images_list.delete(0,tk.END)
        
            
            traine_image = []
            teste_image = []

            
            for file in dirs:
                if os.path.isfile(f'{path}/{file}'):
                    self.input_training_images_list.insert(tk.END,file)
                    traine_image.append(file)     

    def load_labels(self):
        self.input_training_label_list.delete(0,tk.END)
        path = "dataset"
        if os.path.isdir(path):
            labels_train = os.listdir( path )

        # This would print all the files and directories
            for train_file in labels_train:
                self.input_training_label_list.insert(tk.END,train_file)

     

    
