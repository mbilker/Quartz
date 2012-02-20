#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import libquartz, libicraft, os, random, string, re, threading
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

prepend = "Qtz"

try:
	nicks=open("nicks.txt").readlines()
except:
	nicks = ""
def joinaction(sk):
	sk.send(libicraft.minemsg("QuartzGUI Alpha Minecraft Tester"))
	pass
def picknickname():
	if nicks != "":
		return random.choice(nicks).replace("\n", "")
        return prepend+"".join(random.choice(string.letters+string.digits) for x in range(random.randint(6-len(prepend),15-len(prepend))))
def action(sk):
	if app.c == True:
		sk.send(libicraft.creativedrop())
	if app.b == True:
		sk.send(libicraft.minemsg("".join(random.choice(string.letters+string.digits) for x in range(random.randint(1,100)))))
	if app.a == True:
		sk.send(libicraft.minemsg("§k"+"".join(random.choice(string.letters+string.digits) for x in range(random.randint(1,50)))))
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
         self.entryWidget["width"] = 20
         self.entryWidget.pack()
         self.buttona = Button(frame, text="Start Creative Drop", fg="red", command=self.cd)
         self.buttona.pack()
         self.buttonb = Button(frame, text="Start Random Flood", fg="red", command=self.rf)
         self.buttonb.pack()
         self.buttonc = Button(frame, text="Start Changing Flood", fg="red", command=self.rd)
         self.buttonc.pack()
         self.button = Button(frame, text="Quit", fg="red", command=self.quit)
         self.button.pack()
         self.hi_there = Button(frame, text="Connect", command=self.start)
         self.hi_there.pack()
	 self.b = False
	 self.a = False
    def rf(self):
	if self.b == False:
		self.b = True
		self.buttonb["text"]="Stop Random Flood"
	else:
		self.b = False
		self.buttonb["text"]="Start Random Flood"
    def rd(self):
	if self.a == False:
		self.a = True
		self.buttonc["text"]="Stop Changing Flood"
	else:
		self.a = False
		self.buttonc["text"]="Start Changing Flood"
    def cd(self):
	togglecd(self)
    def quit(self):
	os.kill(os.getpid(), 9)
    def start(self):
	if self.hi_there['text'] == "Connect":
		self.hi_there['text'] = "Stop and quit"
		self.lbl['text'] = "QuartzGUI - Running!"
		libquartz.start(picknickname, action, joinaction, self.entryWidget.get())
	else:
		os.kill(os.getpid(), 9)
root = Tk()
root.resizable(0,0)
flood=False
randomchangingflood=False
randomflood=False
root.title("QuartzGUI")
app = App(root)
t=threading.Thread(target=root.mainloop(), args=())
