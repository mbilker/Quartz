# -*- coding: utf-8 -*-
stopmii = True
debug=False
localThread=False
onlyLocal = False
import libicraft, sys, random, time, socks, socket, threading, struct, binascii, re, string, libcraftpacket, os, KThreads
prepend="Qtz_"
timesleep=0
exitApp=False
proxies=open("proxies.txt").readlines()
exitApp=False
strtosay = ""
def threadEntry(proxied,pnick,action,joinaction, target, x):
	while True:
		laststr = ""
		choosenproxy="127.0.0.1"
		prox = ""
		tries = 30
		while proxied == "True":
			action(None)
			if stopmii == False:
			    return
			if tries == 0:
				return
			tries = tries - 1
			if exitApp:
				return
			action(None)
			choosenproxy=random.choice(proxies).replace("\n","")
			prox=libicraft.parse_ip(choosenproxy)
			break
			try:
			        s = socks.socksocket()
			except:
				continue
        		s.setproxy(socks.PROXY_TYPE_HTTP, prox['ip'], prox['port'])
			s.settimeout(3)
			didConnect = False
			try:
				s.connect((target['ip'], target['port']))
				didConnect = True
				ret=libicraft.get_info(s)
			except:
				ret=""
				s.close()
			if ret:
				break
			else:
				continue
		while True:
			if exitApp:
				return
			try:
				sk = ""
				sk = socks.socksocket()
				if proxied == "True":
					sk.setproxy(socks.PROXY_TYPE_HTTP, prox['ip'], prox['port'])
					pass
				sk.connect((target['ip'], target['port']))
				nick=pnick()
				action(None)
				if localThread == False:
					print("[+] Connected! [" + choosenproxy + "||"+nick+"]")
				action(None)
				sk.send(libicraft.join(nick))
				action(None)
				sk.send(libicraft.minemsg("/register omfg1336"))
				sk.send(libicraft.minemsg("/login omfg1336"))
				joinaction(sk)
				x="lol"
				while x:
				 try:
					if stopmii == False:
					   return
					#x=sk.recv(256)
					#sk.send("\x00\x00\x00\x00\x00")
					x=libcraftpacket.readpacket(sk)
					if x == "E":
						break
					if x.startswith("M"): 
						if proxied == "False":
							print x[1:]
					if strtosay != laststr:
						sk.send(libicraft.minemsg(strtosay))
						laststr = strtosay
					action(sk)
					time.sleep(timesleep)
				 except:
					if debug:
						raise
				 	pass
			except:
				if debug:
					raise
				break
print("[i] Welcome to Quartz")
print("[i] Quartz was made by qwertyoruiop to benchmark Minecraft servers")
print("[i] Please don't abuse it!")
def threadRespawn(a,pnick,action,joinaction, target, kact, b):
		while True:
			if stopmii == False:
				return
			t=KThreads.KThread(target=threadEntry, args=("True", pnick,action,joinaction, target, None))
			t.start()
			kact()
def start(pnick, action, joinaction, target, kact):
	target = libicraft.parse_ip(target)
	if localThread:
		KThreads.KThread(target=threadEntry, args=("False",pnick,action,joinaction, target,"")).start()
	else:
		if onlyLocal == False:
			t=KThreads.KThread(target=threadRespawn, args=("LOL", pnick,action,joinaction, target, kact, kact))
			t.start()
		else:
			t=KThreads.KThread(target=threadEntry, args=("False",pnick,action,joinaction, target,""))
			t.start()
	while True:
		try:
			strtosay = raw_input()
		except KeyboardInterrupt:
			stopmii = False
			os.kill(os.getpid(), 9)

