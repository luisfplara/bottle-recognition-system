from tkinter import *
from pages.dataset import dataset
from pages.recognition import recognition
from pages.training import training

class App(Tk):
	def __init__(self, *args, **kwargs):
		self.title = {'BRS'}
		Tk.__init__(self, *args, **kwargs)
	

		#Setup Frame
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		self.StartPage = StartPage
		self.actual_frame = None

		for F in (StartPage,dataset, training,recognition):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)	

	def show_frame(self, context):
		self.actual_frame = context
		frame = self.frames[context]
		frame.tkraise()

	def caller(self,frame_to_call, args):
		self.args = args
		self.show_frame(frame_to_call)
		

class StartPage(Frame):
	def __init__(self, parent, controller):

		Frame.__init__(self, parent)
	
		label = Label(self, text="Bottle Recognition System",font='Helvetica 16 bold')
		label.pack(padx=10, pady=10)
		page_one = Button(self, text="Dataset", command=lambda:controller.show_frame(dataset),height = 3, width = 15)
		page_one.pack()
		page_two = Button(self, text="Training", command=lambda:controller.caller(training, args = "Texxxxxte"),height = 3, width = 15)
		page_two.pack()
		page_two = Button(self, text="Recognition", command=lambda:controller.show_frame(recognition),height = 3, width = 15)
		page_two.pack()


class PageTwo(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = Label(self, text="Page Two")
		label.pack(padx=10, pady=10)
		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
		start_page.pack()
		#page_one = Button(self, text="Page One", command=lambda:controller.show_frame(PageOne))
		#page_one.pack()



app = App()
app.mainloop()