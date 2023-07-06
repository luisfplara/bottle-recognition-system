import cv2
import argparse
from components.get_background import get_background
def filterFrame(frame,frame_diff_list):
  
  frame_filtered = frame.copy()
  x=640
  contours, hierarchy = cv2.findContours(frame_diff_list, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # draw the contours, not strictly necessary
  for i, cnt in enumerate(contours):
      if cv2.contourArea(cnt) > 7000:
        cv2.drawContours(frame_filtered, contours, i, (0, 0, 255), 3)
        (x, y, w, h) = cv2.boundingRect(cnt)

        cv2.rectangle(frame_filtered, (x, y), (x+w, y+h), (0, 255, 0), 2)
  #for contour in contours:
      # continue through the loop if contour area is less than 500...
      # ... helps in removing noise detection
      #if cv2.contourArea(contour) > 7000:
        


  #cv2.imshow('Detected Objects', orig_frame)
  return (frame_filtered,x)     
         