import tkinter
import tkinter.ttk
import ChartMaker
import numpy as np
import csv
import Time_Sort

global s_nex
global s_bef
s_nex = None
s_bef = None

class Sly:
	canvas = None
	def __init__(self,x,y,before=None,next=None):
		self.x = x
		self.y = y
		self.before = before
		self.next = next
		self.id1 = None
		self.id2 = None
		self.id3 = None
		self.id4 = None
		self.l = None
		self.r = None
	def write(self):
		self.id1 = self.canvas.create_rectangle(self.x*40+50,self.y-20,self.x*40+70,self.y+20,fill = 'deep pink',tag = "Slider")
		self.Bind()
		self.canvas.tag_bind(self.id1,'<1>',self.Func)
	
	def Func(self,event):
		if(app.Note == 4 or app.Note == 0):
			self.delete()
		elif(app.Note == 5):
			self.Bind()
		elif(app.Note == 6):
			self.Right()
		elif(app.Note == 7):
			self.Left()

	def Bind(self):
		global s_bef
		global s_nex
		if(s_bef == None):
			s_bef = self
		elif(self.next == None and self.before != None):
			s_nex = self
			self.before.next = self
			point = self.canvas.coords(self.before.id1)
			pointa = self.canvas.coords(self.id1)
			self.id2 = self.canvas.create_line((pointa[0]+pointa[2])//2,(pointa[1]+pointa[3])//2,(point[0]+point[2])//2,(point[1]+point[3])//2,fill = 'deep pink', tag = "other",width = 5)
			s_bef = self
	def reBind(self,nex):
		nex.before = self.before
		if(self.before == None):
			self.canvas.delete(nex.id2)
		else:
			self.before.next = nex
			self.canvas.delete(nex.id2)
			point = self.canvas.coords(self.before.id1)
			pointa= self.canvas.coords(nex.id1)
			nex.id2 = self.canvas.create_line((pointa[0]+pointa[2])//2,(pointa[1]+pointa[3])//2,(point[0]+point[2])//2,(point[1]+point[3])//2,fill = 'deep pink', tag = "other",width = 5)
	def Right(self):
		if(self.next != None):
			self.canvas.delete(self.next.id2)
			self.next.before = None
			self.next = None
		if(self.l != None):
			self.canvas.delete(self.id3)
			self.canvas.delete(self.id4)
			self.l = None
		if(self.r == None):
			self.id3 = self.canvas.create_polygon(75+self.x*40,-20+self.y,85+self.x*40,-20+self.y,90+self.x*40,self.y,85+self.x*40,20+self.y,75+self.x*40,20+self.y,80+self.x*40,self.y,fill = 'deep pink', tag ="other")
			self.id4 = self.canvas.create_polygon(88+self.x*40,-20+self.y,98+self.x*40,-20+self.y,103+self.x*40,self.y,98+self.x*40,20+self.y,88+self.x*40,20+self.y,93+self.x*40,self.y,fill = 'deep pink', tag ="other")
			self.canvas.itemconfig(self.id1,tag ="Right")
			global s_nex
			global s_bef
			s_nex = None
			s_bef = None
			self.r = 1
			
	def Left(self):
		if(self.next != None):
			self.canvas.delete(self.next.id2)
			self.next.before = None
			self.next = None
		if(self.r != None):
			self.canvas.delete(self.id3)
			self.canvas.delete(self.id4)
			self.r = None
		if(self.l == None):
			self.id3 = self.canvas.create_polygon(45+self.x*40,-20+self.y,35+self.x*40,-20+self.y,30+self.x*40,self.y,35+self.x*40,20+self.y,45+self.x*40,20+self.y,40+self.x*40,self.y,fill = 'deep pink', tag ="other")
			self.id4 = self.canvas.create_polygon(32+self.x*40,-20+self.y,22+self.x*40,-20+self.y,17+self.x*40,self.y,22+self.x*40,20+self.y,32+self.x*40,20+self.y,27+self.x*40,self.y,fill = 'deep pink', tag ="other")
			self.canvas.itemconfig(self.id1,tag ="Left")
			global s_nex
			global s_bef
			s_nex = None
			s_bef = None
			
			self.l = 1

	def delete(self):
		self.canvas.delete(self.id1)
		if(self.id2 != None):
			self.canvas.delete(self.id2)
			self.before.next = None
			global s_bef
			s_bef = self.before
		elif(self.next != None):
			self.reBind(self.next)
		if(self.id3 != None):
			self.canvas.delete(self.id3)
			self.canvas.delete(self.id4)
		if(self.before != None):
			self.canvas.itemconfig(self.before.id1,tag ="Slider")
		else:
			s_bef = None
class CanvasOval:
	canvas = None

	def __init__(self,x0,y0,x1,y1,fill=None,tag=None):
		self.id = self.canvas.create_oval(x0,y0,x1,y1,fill=fill,tag=tag)
		self.t =tag
		self.canvas.tag_bind(self.id,'<1>',self.delete)

	def delete(self, event):
		self.canvas.delete(self.id)
		if(self.t =='Hold'):
			app.h = False
			app.h_bef = None

class CanvasRec:
	canvas = None

	def __init__(self,x0,y0,x1,y1,fill=None,tag=None):
		self.id = self.canvas.create_rectangle(x0,y0,x1,y1,fill=fill,tag=tag)
		self.t = tag
		self.canvas.tag_bind(self.id,'<1>',self.delete)

	def delete(self, event):
		self.canvas.delete(self.id)
		if(self.t == 'Long'):
			app.l = False
			app.l_bef = None
class CanvasLong:
	canvas = None

	def __init__(self,x0,y0,x1,y1):
		self.id1 = self.canvas.create_rectangle(x0*40+41,y0-10,x0*40+79,y0+10,fill = 'yellow',tag = "Long")
		self.id2 = self.canvas.create_line(x1,y1,x0*40+60,y0,fill='yellow',width=20,tag="other")
		self.x = x1
		self.y = y1
		self.canvas.tag_bind(self.id1,'<1>',self.delete)
		self.canvas.tag_bind(self.id2,'<1>',self.delete)

	def delete(self, event):
		self.canvas.delete(self.id1)
		self.canvas.delete(self.id2)
		if(app.l_bef == None):
			app.l = False
		else:
			app.l = True
			app.l_bef = [self.x,self.y]
class CanvasHold:
	canvas = None

	def __init__(self,x0,y0,x1,y1):
		self.id1 = self.canvas.create_oval(x0*40+41,y0-15,x0*40+79,y0+15,fill = 'red',tag = "Hold")
		self.id2 = self.canvas.create_line(x1,y1,x0*40+60,y0,fill='red',width=20,tag="other")
		self.x = x1
		self.y = y1
		self.canvas.tag_bind(self.id1,'<1>',self.delete)
		self.canvas.tag_bind(self.id2,'<1>',self.delete)

	def delete(self, event):
		self.canvas.delete(self.id1)
		self.canvas.delete(self.id2)
		if(app.h_bef == None):
			app.h = False
		else:
			app.h = True
			app.h_bef = [self.x,self.y]
class CanvasLine:
	canvas = None

	def __init__(self,x0,y0,x1,y1,**key):
		self.id = self.canvas.create_line(x0,y0,x1,y1,**key)
		self.canvas.tag_bind(self.id,'<1>',self.delete)

	def delete(self, event):
		self.canvas.delete(self.id)
class CanvasWrite:
	canvas = None

	def __init__(self, x, y,s,**key):
		self.id = self.canvas.create_text(x,y,text = s,**key)
		self.canvas.tag_bind(self.id,'<1>',self.delete)

	def delete(self,event):
		self.canvas.delete(self.id)

class Application(tkinter.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.Note = 1
		self.y_bar= 1
		self.l	  = False
		self.l_bef= None
		self.h    = False
		self.h_bef= None
		self.Sly_n= None
		self.bar = 1
		self.bool= True
		self.sign = 4
		self.Chart_info = []
		self.sign_info = []
		self.master.title('tkinter canvas trial')
		self.pack()
		self.create_widgets()
		self.master.bind('<c>', lambda event:self.change(0))
		self.master.bind('<f>', lambda event:self.change(1))
		self.master.bind('<g>', lambda event:self.change(2))
		self.master.bind('<d>', lambda event:self.change(3))
		self.master.bind('<s>', lambda event:self.change(4))
		self.master.bind('<b>', lambda event:self.change(5))
		self.master.bind('<r>', lambda event:self.change(6))
		self.master.bind('<a>', lambda event:self.change(7))
		self.master.bind('<e>', lambda event:self.change(8))
		self.master.bind('<t>', lambda event:self.change(9))
		self.master.bind('<KeyPress-1>', lambda event:self.Beat(8))
		self.master.bind('<KeyPress-2>', lambda event:self.Beat(16))
		self.master.bind('<KeyPress-3>', lambda event:self.Beat(32))
		self.master.bind('<KeyPress-4>', lambda event:self.Beat(64))
		self.master.bind('<KeyPress-5>', lambda event:self.Beat(12))
		self.master.bind('<KeyPress-6>', lambda event:self.Beat(24))
		self.master.bind('<KeyPress-7>', lambda event:self.Beat(48))
		self.master.bind('<Right>', lambda event:self.Next())
		self.master.bind('<Left>' , lambda event:self.Before())
	def create_widgets(self):
		self.now_state = tkinter.StringVar()
		self.now_state_x=tkinter.ttk.Label(self,textvariable=self.now_state)
		self.now_state_x.grid(row=5,column=2)
		self.bind_state = tkinter.StringVar()
		self.bind_state_x=tkinter.ttk.Label(self,textvariable=self.bind_state)
		self.bind_state_x.grid(row=5,column=3)
		self.sign_state = tkinter.StringVar()
		self.sign_state_x=tkinter.ttk.Label(self,textvariable=self.sign_state)
		self.sign_state_x.grid(row=5,column=1)
		self.canvas = tkinter.Canvas(self, bg='black', width=360, height=640, highlightthickness=0)
		CanvasOval.canvas=self.canvas
		CanvasRec.canvas = self.canvas
		CanvasLine.canvas = self.canvas
		CanvasLong.canvas = self.canvas
		CanvasHold.canvas = self.canvas
		Sly.canvas=self.canvas
		CanvasWrite.canvas = self.canvas
		self.canvas.create_line(40,20,320,20,fill = 'white')
		self.canvas.create_line(40,620,320,620,fill = 'white')
		for i in range(8):
			self.canvas.create_line(40*(i+1),0,40*(i+1),640,fill = 'white')
		self.canvas.grid(row=0, column=0, rowspan=10)
		self.canvas.bind('<ButtonPress-1>', self.start_pickup)
		self.music_entry = tkinter.ttk.Entry(self,width =20)
		self.music_text  = tkinter.ttk.Label(self,text="music name")
		self.Delete_button = tkinter.ttk.Button(self, text='delete(c)',command=lambda: self.change(0))	
		self.N1_button = tkinter.ttk.Button(self, text='N1(f)',command=lambda: self.change(1))
		self.N2_button = tkinter.ttk.Button(self, text='N2(g)',command=lambda: self.change(2))
		self.Long_button = tkinter.ttk.Button(self, text='Long(d)',command=lambda: self.change(3))
		self.Slider_button = tkinter.ttk.Button(self, text='Slider(s)',command=lambda: self.change(4))
		self.Slider_end_button = tkinter.ttk.Button(self, text='Bind(b)',command=lambda: self.change(5))
		self.Slider_right = tkinter.ttk.Button(self, text='Slider Right(r)',command=lambda: self.change(6))
		self.Slider_left = tkinter.ttk.Button(self, text='Slider Left(a)',command=lambda: self.change(7))
		self.Bind_end = tkinter.ttk.Button(self, text='Bind end(e)',command=lambda: self.change(8))
		self.Skill_Line = tkinter.ttk.Button(self, text='Skill Line(t)',command=lambda: self.change(9))
		self.bpm_entry = tkinter.ttk.Entry(self,width = 10)
		self.sign_entry = tkinter.ttk.Entry(self,width = 10)
		self.sign_button = tkinter.ttk.Button(self, text='Time Signature', command=lambda: self.change(11))
		self.bpm_button = tkinter.ttk.Button(self, text='BPM', command=lambda: self.change(10))
		self.beat8 = tkinter.ttk.Button(self, text='8beat(1)',command=lambda: self.Beat(8))
		self.beat16 = tkinter.ttk.Button(self, text='16beat(2)',command=lambda: self.Beat(16))
		self.beat32 = tkinter.ttk.Button(self, text='32beat(3)',command=lambda: self.Beat(32))
		self.beat64 = tkinter.ttk.Button(self, text='64beat(4)',command=lambda: self.Beat(64))
		self.beat12 = tkinter.ttk.Button(self, text='12beat(5)',command=lambda: self.Beat(12))
		self.beat24 = tkinter.ttk.Button(self, text='24beat(6)',command=lambda: self.Beat(24))
		self.beat48 = tkinter.ttk.Button(self, text='48beat(7)',command=lambda: self.Beat(48))
		self.next_bar = tkinter.ttk.Button(self, text='next(→)',command=self.Next)
		self.before_bar = tkinter.ttk.Button(self, text='before(←)',command=self.Before)
		self.music_text.grid(row=0,column=1)
		self.music_entry.grid(row=0,column=2)
		self.N1_button.grid(row=1,column=1)
		self.N2_button.grid(row=1,column=2)
		self.Long_button.grid(row=1,column=3)
		self.Slider_button.grid(row=2,column=1)
		self.Slider_end_button.grid(row=2,column=2)
		self.Bind_end.grid(row=2,column=3)
		self.Slider_left.grid(row=3,column=1)
		self.Slider_right.grid(row=3,column=2)
		self.Skill_Line.grid(row=3,column=3)
		self.bpm_button.grid(row=4,column=1)
		self.bpm_entry.grid(row=4,column=2)
		self.sign_button.grid(row=6,column=1)
		self.sign_entry.grid(row=6,column=2)
		self.Delete_button.grid(row=4,column=3)		
		self.beat8.grid(row=7,column=1)	
		self.beat16.grid(row=7,column=2)	
		self.beat32.grid(row=7,column=3)	
		self.beat64.grid(row=8,column=1)	
		self.beat12.grid(row=8,column=2)	
		self.beat24.grid(row=8,column=3)	
		self.beat48.grid(row=9,column=1)
		self.before_bar.grid(row=9,column=2)
		self.next_bar.grid(row=9,column=3)
	def change(self,n):
		self.Note = n
		global s_nex
		global s_bef
		if(self.Note == 8):
			while s_bef.next != None:
				s_bef = s_bef.next
			self.canvas.itemconfig(s_bef.id1,tag ="Slider_End")
			s_nex = None
			s_bef = None
		if(n == 0):
			self.now_state.set('delete')
		elif(n == 1):
			self.now_state.set('Note1')
		elif(n == 2):
			self.now_state.set('Note2')
		elif(n == 3):
			self.now_state.set('Long')
		elif(n == 4):
			self.now_state.set('Slider')
		elif(n == 5):
			self.now_state.set('Bind')
		elif(n == 6):
			self.now_state.set('Slider_Right')
		elif(n == 7):
			self.now_state.set('Slider_Left')
		elif(n == 8):
			self.now_state.set('Bind end')
		elif(n == 9):
			self.now_state.set('Skill Line')
		elif(n == 10):
			self.now_state.set('BPM')
		elif(n == 11):
			try:
				self.sign = int(self.sign_entry.get())
			except:
				self.sign = 4
			self.sign_state.set(str(self.sign)+'/4')
		if(s_bef == None):
			self.bind_state.set('Not Binded')
		else:
			self.bind_state.set('Binded')
	def Beat(self,n):
		self.canvas.delete("Line")
		self.y_bar = (n//4)*self.sign
		for i in range(self.y_bar-1):
			self.canvas.create_line(40,20+600*(i+1)//self.y_bar,320,20+600*(i+1)//self.y_bar,fill='gray',tag="Line")

	def start_pickup(self, event):
		x = int(event.x)//40-1
		y = 20+((int(event.y)-20)*self.y_bar//600)*600//self.y_bar
		if(self.Note == 1):
			self.N1_put(x,y)
		elif(self.Note == 2):
			self.N2_put(x,y)
		elif(self.Note == 3):
			self.Long_put(x,y)
		elif(self.Note == 4):
			self.Slider(x,y)
		elif(self.Note == 9):
			self.Red_Line(y)
		elif(self.Note == 10):
			self.BPM_Line(y)
	def N1_put(self, x, y):
		if(x ==0 or x == 6):
			CanvasOval(x*40+41,y-15,x*40+79,y+15,fill = 'dark orange',tag = "Scrach")
		elif(0 < x < 6):
			CanvasRec(x*40+41,y-10,x*40+79,y+10,fill = 'cyan',tag = "N1")
	def N2_put(self, x, y):
		if(x ==0 or x == 6):
			CanvasOval(x*40+41,y-15,x*40+79,y+15,fill = 'dark orange',tag = "Scrach")
		elif(0 < x < 6):
			CanvasRec(x*40+41,y-10,x*40+79,y+10,fill = 'blue',tag = "N2")
	def Long_put(self,x,y):
		if(0 < x < 6):
			if(self.l):
				CanvasLong(x,y,self.l_bef[0],self.l_bef[1])
				self.l = False
			else:
				CanvasRec(x*40+41,y-10,x*40+79,y+10,fill = 'yellow',tag = "Long")
				self.l = True
				if(self.Note != 0):
					self.l_bef = [x*40+60,y]
		if(x == 0 or x == 6):
			if(self.h):
				CanvasHold(x,y,self.h_bef[0],self.h_bef[1])
				self.h = False
			else:
				CanvasOval(x*40+41,y-15,x*40+79,y+15,fill = 'red',tag = "Hold")
				self.h = True
				if(self.Note != 0):
					self.h_bef = [x*40+60,y]
	def Slider(self,x,y):
		s = Sly(x,y,before=s_bef)
		s.write()
		self.bind_state.set("Binded")
	def Red_Line(self,y):
		CanvasLine(40,y,320,y,fill='red',tag="Skill")
	def BPM_Line(self,y):
		CanvasWrite(20,y,self.bpm_entry.get(),fill = 'white',tag ="BPM")
	def Next(self):
		Chart_info_bar = []
		sign_info_bar = self.sign
		note_type = ["Skill","N1","N2","Scrach","Slider","Slider_End","Right","Left","Long","Hold"]
		for id in self.canvas.find_all():
			tag = self.canvas.itemcget(id,'tags')
			for i in range(len(note_type)):
				if(tag == note_type[i]):
					point = self.canvas.coords(id)
					x = (point[0]+point[2])/2
					y = (point[1]+point[3])/2
					x_line = (x-40)//40
					y_line = (620-y)//(75/24)/24
					if(0 <= y_line < 8):
						Chart_info_bar += [[i,x_line,y_line]]
					self.canvas.move(id,0,600)
			if(tag == "other"):
				self.canvas.move(id,0,600)
			if(tag == "BPM"):
				point = self.canvas.coords(id)
				y = point[1]
				y_line = (620-y)//(75/24)/24
				if(0 <= y_line < 8):
					Chart_info_bar += [[float(self.bpm_entry.get()),0,y_line]]
				self.canvas.move(id,0,600)
		if(self.l_bef != None):
			self.l_bef[1] = self.l_bef[1]+600
		if(self.h_bef != None):
			self.h_bef[1] = self.h_bef[1]+600

		if(len(self.Chart_info) < self.bar):
			self.Chart_info += [Chart_info_bar]
			self.sign_info += [sign_info_bar]
			self.bar += 1
		else:
			self.Chart_info[self.bar-1] = Chart_info_bar
			self.sign_info[self.bar-1] = sign_info_bar
			self.bar += 1
		sorted_info = Time_Sort.T_Sort(self.Chart_info)
		ChartMaker.Make_Chart(sorted_info,len(self.Chart_info),'./データ/Chart/'+self.music_entry.get(),sign=self.sign_info)
		with open('./データ/Chart/'+self.music_entry.get()+'.csv','w') as f:
			writer = csv.writer(f)
			writer.writerows(sorted_info)
		with open('./データ/Chart/'+self.music_entry.get()+'_signature.csv','w') as f:
			writer = csv.writer(f)
			writer.writerow(self.sign_info)
	def Before(self):
		note_type = ["Skill","N1","N2","Scrach","Slider","Slider_End","Right","Left","Long","Hold","other","BPM","Sign"]
		for id in self.canvas.find_all():
			tag = self.canvas.itemcget(id,'tags')
			if(tag in note_type):
				self.canvas.move(id,0,-600)
		try:
			self.sign = self.sign_info[self.bar-2]
		except:
			self.sign = 4
		self.bar -= 1
		if(self.l_bef != None):
			self.l_bef[1] = self.l_bef[1]-600
		if(self.h_bef != None):
			self.h_bef[1] = self.h_bef[1]-600
	
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
