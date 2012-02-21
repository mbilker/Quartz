# -*- coding: utf-8 -*-
sockssupport = False
stopmii = True
debug=False
localThread=False
onlyLocal = False
import libicraft, sys, random, time, socks, socket, threading, struct, binascii, re, string, libcraftpacket, os, KThreads
timesleep=0
exitApp=False
proxiesk = []
proxies = ["config:mii"]
proxies=open("proxies.txt").readlines()
exitApp=False
strtosay = ""
def threadEntry(proxied,pnick,action,joinaction, target, x):
	while True:
		choosenproxy="127.0.0.1"
		prox = ""
		laststr = ""
		if proxied == "True":
		 while True:
			action(None)
			if stopmii == False:
			    return
			action(None)
			choosenproxy=random.choice(proxies).replace("\n","")
			prox=libicraft.parse_ip(choosenproxy)
			ret = None
			try:
				s = socks.socksocket()
				s.settimeout(1)
	        		s.setproxy(socks.PROXY_TYPE_HTTP, prox['ip'], prox['port'])
				s.connect((target['ip'], target['port']))
				didConnect = True
				prox['type'] = socks.PROXY_TYPE_HTTP
				ret=libicraft.get_info(s)
			except:
				if sockssupport == False:
					continue
				try:
					s.close()
					s = socks.socksocket()
					s.settimeout(1)
		        		s.setproxy(socks.PROXY_TYPE_SOCKS4, prox['ip'], prox['port'])
					s.connect((target['ip'], target['port']))
					didConnect = True
					prox['type'] = socks.PROXY_TYPE_SOCKS4
					ret=libicraft.get_info(s)
				except:
					try:
						s.close()
						s = socks.socksocket()
						s.settimeout(1)
			        		s.setproxy(socks.PROXY_TYPE_SOCKS5, prox['ip'], prox['port'])
						s.connect((target['ip'], target['port']))
						didConnect = True
						prox['type'] = socks.PROXY_TYPE_SOCKS5
						ret=libicraft.get_info(s)
					except:
						continue
			s.close()
			s = None
			if ret != None:
				break
		while True:
			if exitApp:
				return
			try:
				sk = None
				sk = socks.socksocket()
				sk.settimeout(1)
				if proxied == "True":
		        		sk.setproxy(prox['type'], prox['ip'], prox['port'])
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
			t=KThreads.KThread(target=threadRespawn, args=("True", pnick,action,joinaction, target, kact, kact))
			t.start()
		else:
			t=KThreads.KThread(target=threadEntry, args=("False",pnick,action,joinaction, target,""))
			t.start()
