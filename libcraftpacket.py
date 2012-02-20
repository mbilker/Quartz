# -*- coding: utf-8 -*-
import binascii, re
def printopt(string):
	return
	print string
def genmetadata(socket):
	metadata = {}
	x = ord(socket.recv(1))
	while x != 127:
		index = x & 0x1F # Lower 5 bits
		ty    = x >> 5   # Upper 3 bits
		if ty == 0: val = ord(socket.recv(1))
		if ty == 1: val = socket.recv(2)
		if ty == 2: val = socket.recv(4)
		if ty == 3: val = socket.recv(4)
		if ty == 4: val = readstring(socket)
		if ty == 5:
			val = {}
			val["id"]     = socket.recv(2)
			val["count"]  = socket.recv(1)
			val["damage"] = socket.recv(2)
		if ty == 6:
			val = []
			for i in range(3):
				val.append(socket.recv(4))
		metadata[index] = (ty, val)
		x = ord(socket.recv(1))
	return metadata
def readslot(socket):
	item = int(binascii.b2a_hex(socket.recv(2)), 16)
	printopt( "Item Update" )
	if item != 65535:
		count = ord(socket.recv(1))
		damage = int(binascii.b2a_hex(socket.recv(2)),16)
		len = int(binascii.b2a_hex(socket.recv(2)),16)
		while len != 0:
			socket.recv(1)
			len = len - 1
def readstring(socket):
        lent = int(binascii.b2a_hex(socket.recv(1)),16)
        try:
                retn = socket.recv(lent*2)                   
        except:
                return ""
        result=re.sub(r'\xA7\x00..', '', retn)
        return result.decode('utf-16be')
def readstringlong(socket):
        lent = int(binascii.b2a_hex(socket.recv(2)),16)
	try:
		retn = socket.recv(lent*2)
	except:
		return ""
	result=re.sub(r'\xA7\x00..', '', retn)
        return result.decode('utf-16be')
def readpacket(socket):
	id = socket.recv(1)
	#printopt( "Debug: ["+str(ord(id))+"]"
	if id == "\x00":
		printopt( "Possible keepalive!" )
		socket.send("\x00\x00\x00\x00\x00")
	elif id == "\x01":
		printopt( "Login packet ["+str(ord(socket.recv(1)))+"]" )
		socket.recv(4)
		socket.recv(1)
		socket.recv(9)
		readstring(socket)
		socket.recv(4)
		socket.recv(1)
		socket.recv(1)
		socket.recv(1)
		socket.recv(1)
	elif id == "\x02":
		# Handshake
		printopt( "Handshake packet [" + readstringlong (socket) +"]" )
		pass
	elif id == "\x03":
		msg = readstringlong(socket)
		printopt ( "Chat message [" + msg + "]" )
		return "M" + msg
	elif id == "\x04":
		printopt( "Time Packet" )
		socket.recv(8)
	elif id == "\x05":
		printopt( "Entity Equipment" )
		socket.recv(10)
        elif id == "\x06":
		printopt( "Spawn Position [X:"+str(int(binascii.b2a_hex(socket.recv(4)),16))+", Y:"+str(int(binascii.b2a_hex(socket.recv(4)),16))+", Z:"+str(int(binascii.b2a_hex(socket.recv(4)),16))+"]" )
        elif id == "\x08":
		printopt( "Health Update" )
		socket.recv(8)
        elif id == "\x09":
		printopt( "Respawn [Dimension: " + ord(socket.recv(1)) + "]" )
		socket.recv(1)
		socket.recv(1)
		socket.recv(2)
		socket.recv(8) 
		printopt( readstring(socket) )
        elif id == "\x0D":
		printopt( "Player Position & Look" )
		socket.recv(8)
		socket.recv(8)
		socket.recv(8)
		socket.recv(8)
		socket.recv(4)
		socket.recv(4)
		socket.recv(1)
        elif id == "\x11":
		printopt( "Use Bed" )
		socket.recv(4)
		socket.recv(1)
		socket.recv(4)
		socket.recv(1)
		socket.recv(4)
        elif id == "\x12":
		printopt( "Animation" )
		socket.recv(4)
		socket.recv(1)
        elif id == "\x14":
		socket.recv(5)
		printopt( "Player Spawn ["+readstring(socket)+"]" )
		socket.recv(4)
		socket.recv(4)
		socket.recv(4)
		socket.recv(1)
		socket.recv(1)
		socket.recv(2)
	elif id == "\x15":
		printopt( "Pickup Spawn" )
		socket.recv(4)
		socket.recv(2)
		socket.recv(1)
		socket.recv(2)
		socket.recv(4)
		socket.recv(4)
		socket.recv(4)
		socket.recv(1)
		socket.recv(1)
		socket.recv(1)
	elif id == "\x16":
		printopt( "Collect Item" )
		socket.recv(4)
		socket.recv(4)
	elif id == "\x17":
		#assert socket.recv(1) == "\x00"
		printopt( "Add Object/Vehicle" )
		socket.recv(4)
		socket.recv(1)
		socket.recv(4)
		socket.recv(4)
		socket.recv(4)
		if socket.recv(4) != "\x00\x00\x00\x00":
			socket.recv(2)
			socket.recv(2)
			socket.recv(2)
	elif id == "\x18":
		printopt( "Mob Spawn" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
		genmetadata(socket)
        elif id == "\x19":
                socket.recv(4)
                printopt( "Painting [" + readstring(socket) + "]" )
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
        elif id == "\x1A":
                printopt( "Experience Drop" )
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
                socket.recv(2)
        elif id == "\x1C":
                printopt( "Entity Velocity" )
                socket.recv(4)
                socket.recv(2)
                socket.recv(2)
                socket.recv(2)
        elif id == "\x1D":
                printopt( "Destroy Entity" )
                socket.recv(4)
        elif id == "\x1E":
                printopt( "Entity" )
                socket.recv(4)
        elif id == "\x1F":
                printopt( "Entity Relative Move" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
                socket.recv(1)
        elif id == "\x20":
                printopt( "Entity Look" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
        elif id == "\x21":
                printopt( "Entity Look and Relative Move" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
                socket.recv(1)
                socket.recv(1)
                socket.recv(1)
        elif id == "\x22":
                printopt( "Entity Teleport" )
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
        elif id == "\x26":
                printopt( "Entity Status" )
                socket.recv(4)
                socket.recv(1)
        elif id == "\x27":
                printopt( "Entity Attach" )
                socket.recv(4)
                socket.recv(4)
        elif id == "\x28":
                printopt( "Entity Metadata" )
                socket.recv(4)
		genmetadata(socket)
        elif id == "\x29":
                printopt( "Entity Effect" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
                socket.recv(2)
	elif id == "\x2A":
                printopt( "Remove Entity Effect" )
                socket.recv(4)
                socket.recv(1)
        elif id == "\x2B":
                printopt( "Experience Update" )
                socket.recv(4)
                socket.recv(2)
                socket.recv(2)
        elif id == "\x32":
		printopt( "Pre-Chunk Packet" )
                socket.recv(4)
                socket.recv(4)
                socket.recv(1)
        elif id == "\x33":
                socket.recv(4)
                socket.recv(2)
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
                socket.recv(1)
		lent = binascii.b2a_hex(socket.recv(4))
                printopt( "Chunk Update [" + lent +"]" )
		lentt = int(lent, 16)
		while lentt != 0:
			socket.recv(1)
			lentt = lentt - 1
        elif id == "\x34":
                printopt( "Multi Block Change" )
                socket.recv(4)
                socket.recv(4)
                lentk = int(binascii.b2a_hex(socket.recv(2)), 16)
		lent = lentk
		while lent != 0:
			socket.recv(2)
			lent = lent - 1
		lent = lentk
		while lent != 0:
			socket.recv(1)
			lent = lent - 1
		lent = lentk
		while lent != 0:
			socket.recv(1)
			lent = lent - 1
        elif id == "\x35":
                printopt( "Block Change" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
        elif id == "\x36":
                printopt( "Block Action" )
                socket.recv(4)
                socket.recv(2)
                socket.recv(4)
                socket.recv(1)
                socket.recv(1)
        elif id == "\x3C":
                printopt( "Explosion" )
                socket.recv(8) 
                socket.recv(8)
                socket.recv(8)
                socket.recv(4)
                lent = int(binascii.b2a_hex(socket.recv(4)), 16)
		socket.recv(lent)
		socket.recv(lent)
		socket.recv(lent)
        elif id == "\x3D":
                printopt( "Sound/particle effect" )
                socket.recv(4)
                socket.recv(4)
                socket.recv(1)
                socket.recv(4)
                socket.recv(4)
        elif id == "\x46":
                printopt( "New/Invalid State" )
                socket.recv(1)
                socket.recv(1)
        elif id == "\x47":
                printopt( "Thunderbolt" )
                socket.recv(4)
                socket.recv(1)
                socket.recv(4)
                socket.recv(4)
                socket.recv(4)
        elif id == "\x64":
                socket.recv(1)
                socket.recv(1)
                printopt( "Open window [" + readstring(socket) + "]" )
                socket.recv(1)
        elif id == "\x65":
                printopt( "Close Window" )
                socket.recv(1)
        elif id == "\x66":
		pass
        elif id == "\x67":
                socket.recv(3)
		readslot(socket)
        elif id == "\x68":
		socket.recv(1)
		list = int(binascii.b2a_hex(socket.recv(2)), 16)
		while list != 0:
			readslot(socket)
			list = list - 1
        elif id == "\x69":
		pass
        elif id == "\x6A":
		pass
        elif id == "\x6C":
		pass
        elif id == "\x82":
                socket.recv(4)
                socket.recv(2)
                socket.recv(4)
		a=readstringlong(socket)
		b=readstringlong(socket)
		c=readstringlong(socket)
		d=readstringlong(socket)
		printopt( "Update Sign [" + a + ":" + b + ":" + c + ":" + d + "]" )
        elif id == "\x83":
                printopt( "Item Data" )
		socket.recv(2)
		socket.recv(2)
		sz = ord(socket.recv(1))
		socket.recv(sz)
        elif id == "\xC8":
                printopt( "Increment Statistic" )
                socket.recv(4)
                socket.recv(1)
        elif id == "\xC9":
                socket.recv(1)
                printopt( "Player List Item [" + readstring(socket) + "]" )
                socket.recv(1)
                socket.recv(2)
        elif id == "\xFA":
                socket.recv(1)
		printopt( "Plugin message [" + readstring(socket) + "]" )
                sz = int(binascii.b2a_hex(socket.recv(2)), 16)
		while sz != "0":
			socket.recv(sz)
			sz = sz - 1
        elif id == "\xFF":
		printopt( "Disconnected! [" + readstringlong(socket) + "]" )
		#socket.close()
		return "E"
	else:
		printopt( "Unmatched Packet [" + binascii.b2a_hex(id) + "], out of sync?" )
		#return "E"
	return id

