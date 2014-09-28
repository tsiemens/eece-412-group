import tkinter

class MainGui(tkinter.Tk):
	def __init__(self,parent):
		tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		tkinter.Tk.mainloop(self)

	def initialize(self):
		self.grid()
		self.mode = tkinter.IntVar()
		
		self.serverSelect = tkinter.Radiobutton(self, text = "Server", variable = self.mode, value = 1, command = self.OnModeSelect)
		self.serverSelect.grid(column = 0, row = 0, sticky = 'EW')
		
		self.clientSelect = tkinter.Radiobutton(self, text = "Client", variable = self.mode, value = 2, command = self.OnModeSelect)
		self.clientSelect.grid(column = 0, row = 1, sticky = 'EW')
		
		self.labelVariable = tkinter.StringVar()
		label = tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
		label.grid(column=0,row=2,columnspan=2,sticky='EW')
		self.labelVariable.set(u"Hello !")
		
		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,False)
		self.update()
		self.geometry(self.geometry())       

	def OnModeSelect(self):
		print("Hello World!")