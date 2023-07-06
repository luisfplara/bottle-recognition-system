import tkinter as tk

class PositionControlPanel:




    def __init__(self, frame, row) -> None:
        self.frameStart = self.pref.get('frameStart')
        self.frameSize = self.pref.get('frameSize')
        self.frame = frame
        self.row = row
        self.cameraPositionControlFrame()
        
    def cameraPositionControlFrame(self):
        
        configLabel = tk.Label(self.frame, text="Camera Frame Configure")
        configLabel.grid(row = self.row,column = 0,)

        controlFrame = tk.Frame(self.frame)
        controlFrame.grid(row=self.row+1, column=0)

        start_inc_button = tk.Button(controlFrame,height=1, width=6,text="Start+", command=self.start_inc)
        start_dec_button = tk.Button(controlFrame,height=1, width=6,text="Start-", command=self.start_dec)

        size_inc_button = tk.Button(controlFrame,height=1, width=6,text="Size+", command=self.size_inc)
        size_dec_button = tk.Button(controlFrame,height=1, width=6,text="Size-", command=self.size_dec)
        
        start_inc_button.grid(row=0, column=0)
        start_dec_button.grid(row=1, column=0)

        size_inc_button.grid(row=0, column=1)
        size_dec_button.grid(row=1, column=1)
        
    
    def start_inc(self):
        if self.frameSize>self.frameStart:
            self.frameStart+=10
            self.pref.update_preferences({'frameStart': self.frameStart})

    def start_dec(self):
        if self.frameStart>=10:
            self.frameStart-=10
            self.pref.update_preferences({'frameStart': self.frameStart})
    def size_inc(self):
        self.frameSize += 10
        self.pref.update_preferences({'frameSize': self.frameSize})
    def size_dec(self):
        if self.frameSize>10:
            self.frameSize -= 10
            self.pref.update_preferences({'frameSize': self.frameSize})

    
    #def __init__(frame) -> None:
        #cameraPositionControlFrame(frame)
        

