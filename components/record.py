import tkinter as tk
import time
import threading
import cv2
class record_widget:
  
  def __init__(self, frame, live_frame):
    
    self.frame = tk.Frame(frame)
    self.frame.pack( side = tk.TOP )

    self.live_frame = live_frame
    self.recording = False
    self.start_button = tk.Button(self.frame,text="Start", command=self.start_rec)
    self.stop_button = tk.Button(self.frame,text="Stop", command=self.stop_rec, state="disabled")
    
    self.setup_buttons_pos()

  def setup_buttons_pos(self):
      self.start_button.pack(side = tk.LEFT)
      self.stop_button.pack(side = tk.LEFT)  
      
  
  def stop_rec(self):
      
      stop = time.time()
      self.recording = False
      print(f'Recorded video - > time: {stop-start} frames count {countFrames} fps: {countFrames/(stop-start)}')

      self.start_button.config(state="normal")
      self.stop_button.config(state="disabled")
  
  def start_rec(self):
      
      self.recording = True
      thread = threading.Thread(target=self.start_capture, daemon=True)
      thread.start()
      #update_frame()
  
      self.start_button.config(state="disabled")
      self.stop_button.config(state="normal")
  def start_capture (self):
     global start,countFrames
     start = time.time()
     countFrames =0
     width= 640
     height= 480
     video_writer = cv2.VideoWriter('basicvideo.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 28,frameSize= (width,height))
     
     while self.recording:
        countFrames+=1
        video_writer.write(self.live_frame)

    
     video_writer.release()
