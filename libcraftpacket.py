# -*- coding: utf-8 -*-
import binascii, re, struct
def readbyte(socket,len):
	ret = ""
	while len != 0:
		ret += socket.recv(1)
		len -= 1
	return ret
def printopt(string):
	#print string
	pass
def genmetadata(socket):
	metadata = {}
	x = ord(readbyte(socket, 1))
	while x != 127:
		index = x & 0x1F # Lower 5 bits
		ty    = x >> 5   # Upper 3 bits
		if ty == 0: val = ord(readbyte(socket, 1))
		if ty == 1: val = readbyte(socket, 2)
		if ty == 2: val = readbyte(socket, 4)
		if ty == 3: val = readbyte(socket, 4)
		if ty == 4: val = readstring(socket)
		if ty == 5:
			val = {}
			val["id"]     = readbyte(socket, 2)
			val["count"]  = readbyte(socket, 1)
			val["damage"] = readbyte(socket, 2)
		if ty == 6:
			val = []
			for i in range(3):
				val.append(readbyte(socket, 4))
		metadata[index] = (ty, val)
		x = ord(readbyte(socket, 1))
	return metadata
def readslot(socket):
	item = int(binascii.b2a_hex(readbyte(socket, 2)), 16)
	printopt( "Item Update" )
	if item != 65535:
		count = ord(readbyte(socket, 1))
		damage = int(binascii.b2a_hex(readbyte(socket, 2)),16)
		len = int(binascii.b2a_hex(readbyte(socket, 2)),16)
		while len != 0:
			readbyte(socket, 1)
			len = len - 1
def readstring(socket):
        lent = int(binascii.b2a_hex(readbyte(socket, 1)),16)
        try:
                retn = readbyte(socket, lent*2)                   
        except:
                return ""
        result=re.sub(r'\xA7\x00..', '', retn)
        return result.decode('utf-16be')
def readstringlong(socket):
        lent = int(binascii.b2a_hex(readbyte(socket, 2)),16)
	try:
		retn = readbyte(socket, lent*2)
	except:
		return ""
	result=re.sub(r'\xA7\x00..', '', retn)
        return result.decode('utf-16be')
def readpacket(socket):
	id = readbyte(socket, 1)
	#printopt( "Debug: ["+str(ord(id))+"]"
	if id == "\x00":
		printopt ( "Ping" )
		socket.send("\x00" + readbyte(socket, 4) )
	elif id == "\x01":
		printopt( "Login packet ["+str(ord(readbyte(socket, 1)))+"]" )
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 9)
		readstring(socket)
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 1)
		readbyte(socket, 1)
		readbyte(socket, 1)
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
		readbyte(socket, 8)
	elif id == "\x05":
		printopt( "Entity Equipment" )
		readbyte(socket, 10)
        elif id == "\x06":
		printopt( "Spawn Position [X:"+str(int(binascii.b2a_hex(readbyte(socket, 4)),16))+", Y:"+str(int(binascii.b2a_hex(readbyte(socket, 4)),16))+", Z:"+str(int(binascii.b2a_hex(readbyte(socket, 4)),16))+"]" )
        elif id == "\x08":
		printopt( "Health Update" )
		readbyte(socket, 2)
		readbyte(socket, 2)
		readbyte(socket, 4)
        elif id == "\x09":
		printopt( "Respawn [Dimension: " + ord(readbyte(socket, 1)) + "]" )
		readbyte(socket, 1)
		readbyte(socket, 1)
		readbyte(socket, 2)
		readbyte(socket, 8) 
		printopt( readstring(socket) )
        elif id == "\x0D":
		printopt( "Player Position & Look" )
		readbyte(socket, 8)
		readbyte(socket, 8)
		readbyte(socket, 8)
		readbyte(socket, 8)
		readbyte(socket, 4)
		readbyte(socket, 4)
		readbyte(socket, 1)
        elif id == "\x11":
		printopt( "Use Bed" )
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 4)
        elif id == "\x12":
		printopt( "Animation" )
		readbyte(socket, 4)
		readbyte(socket, 1)
        elif id == "\x14":
		readbyte(socket, 5)
		printopt( "Player Spawn ["+readstring(socket)+"]" )
		readbyte(socket, 4)
		readbyte(socket, 4)
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 1)
		readbyte(socket, 2)
	elif id == "\x15":
		printopt( "Pickup Spawn" )
		readbyte(socket, 4)
		readbyte(socket, 2)
		readbyte(socket, 1)
		readbyte(socket, 2)
		readbyte(socket, 4)
		readbyte(socket, 4)
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 1)
		readbyte(socket, 1)
	elif id == "\x16":
		printopt( "Collect Item" )
		readbyte(socket, 4)
		readbyte(socket, 4)
	elif id == "\x17":
		#assert readbyte(socket, 1) == "\x00"
		readbyte(socket, 4)
		readbyte(socket, 1)
		readbyte(socket, 4)
		readbyte(socket, 4)
		readbyte(socket, 4)
		lolz = "Normal"
		if readbyte(socket, 4) != "\x00\x00\x00\x00":
			lolz = "Fireball"
			readbyte(socket, 2)
			readbyte(socket, 2)
			readbyte(socket, 2)

		printopt( "Add Object/Vehicle [" + lolz + "]" )
	elif id == "\x18":
		printopt( "Mob Spawn" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
		genmetadata(socket)
        elif id == "\x19":
                readbyte(socket, 4)
                printopt( "Painting [" + readstringlong(socket) + "]" )
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
        elif id == "\x1A":
                printopt( "Experience Drop" )
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 2)
        elif id == "\x1C":
                printopt( "Entity Velocity" )
                readbyte(socket, 4)
                readbyte(socket, 2)
                readbyte(socket, 2)
                readbyte(socket, 2)
        elif id == "\x1D":
                printopt( "Destroy Entity" )
                readbyte(socket, 4)
        elif id == "\x1E":
                printopt( "Entity" )
                readbyte(socket, 4)
        elif id == "\x1F":
                printopt( "Entity Relative Move" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x20":
                printopt( "Entity Look" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x21":
                printopt( "Entity Look and Relative Move" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
                readbyte(socket, 1)
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x22":
                printopt( "Entity Teleport" )
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x26":
                printopt( "Entity Status" )
                readbyte(socket, 4)
                readbyte(socket, 1)
        elif id == "\x27":
                printopt( "Entity Attach" )
                readbyte(socket, 4)
                readbyte(socket, 4)
        elif id == "\x28":
                printopt( "Entity Metadata" )
                readbyte(socket, 4)
		genmetadata(socket)
        elif id == "\x29":
                printopt( "Entity Effect" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
                readbyte(socket, 2)
	elif id == "\x2A":
                printopt( "Remove Entity Effect" )
                readbyte(socket, 4)
                readbyte(socket, 1)
        elif id == "\x2B":
                printopt( "Experience Update" )
                readbyte(socket, 4)
                readbyte(socket, 2)
                readbyte(socket, 2)
        elif id == "\x32":
		printopt( "Pre-Chunk Packet" )
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 1)
        elif id == "\x33":
                readbyte(socket, 4)
                readbyte(socket, 2)
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
                readbyte(socket, 1)
		lent = struct.unpack('>I', readbyte(socket, 4))[0]
                printopt( "Chunk Update [" + str(lent) +"]" )
		readbyte(socket, lent)
        elif id == "\x34":
                printopt( "Multi Block Change" )
                readbyte(socket, 4)
                readbyte(socket, 4)
                lentk = int(binascii.b2a_hex(readbyte(socket, 2)), 16)
		lent = lentk
		while lent != 0:
			readbyte(socket, 2)
			lent = lent - 1
		lent = lentk
		while lent != 0:
			readbyte(socket, 1)
			lent = lent - 1
		lent = lentk
		while lent != 0:
			readbyte(socket, 1)
			lent = lent - 1
        elif id == "\x35":
                printopt( "Block Change" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x36":
                printopt( "Block Action" )
                readbyte(socket, 4)
                readbyte(socket, 2)
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x3C":
                printopt( "Explosion" )
                readbyte(socket, 8) 
                readbyte(socket, 8)
                readbyte(socket, 8)
                readbyte(socket, 4)
                lent = int(binascii.b2a_hex(readbyte(socket, 4)), 16)
		readbyte(socket, lent)
		readbyte(socket, lent)
		readbyte(socket, lent)
        elif id == "\x3D":
                printopt( "Sound/particle effect" )
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 4)
                readbyte(socket, 4)
        elif id == "\x46":
                printopt( "New/Invalid State" )
                readbyte(socket, 1)
                readbyte(socket, 1)
        elif id == "\x47":
                printopt( "Thunderbolt" )
                readbyte(socket, 4)
                readbyte(socket, 1)
                readbyte(socket, 4)
                readbyte(socket, 4)
                readbyte(socket, 4)
        elif id == "\x64":
                readbyte(socket, 1)
                readbyte(socket, 1)
                printopt( "Open window [" + readstring(socket) + "]" )
                readbyte(socket, 1)
        elif id == "\x65":
                printopt( "Close Window" )
                readbyte(socket, 1)
        elif id == "\x66":
		pass
        elif id == "\x67":
                readbyte(socket, 3)
		readslot(socket)
        elif id == "\x68":
		readbyte(socket, 1)
		list = int(binascii.b2a_hex(readbyte(socket, 2)), 16)
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
                readbyte(socket, 4)
                readbyte(socket, 2)
                readbyte(socket, 4)
		a=readstringlong(socket)
		b=readstringlong(socket)
		c=readstringlong(socket)
		d=readstringlong(socket)
		printopt( "Update Sign [" + a + ":" + b + ":" + c + ":" + d + "]" )
        elif id == "\x83":
                printopt( "Item Data" )
		readbyte(socket, 2)
		readbyte(socket, 2)
		sz = ord(readbyte(socket, 1))
		readbyte(socket, sz)
        elif id == "\xC8":
                printopt( "Increment Statistic" )
                readbyte(socket, 4)
                readbyte(socket, 1)
        elif id == "\xC9":
                readbyte(socket, 1)
                printopt( "Player List Item [" + readstring(socket) + "]" )
                readbyte(socket, 1)
                readbyte(socket, 2)
        elif id == "\xFA":
                readbyte(socket, 1)
		printopt( "Plugin message [" + readstring(socket) + "]" )
                sz = int(binascii.b2a_hex(readbyte(socket, 2)), 16)
		while sz != "0":
			readbyte(socket, sz)
			sz = sz - 1
        elif id == "\xFF":
		print( "Disconnected! [" + readstringlong(socket) + "]" )
		socket.close()
		return "E"
	elif id == "":
		print( "Connection Error! :(")
		return "E"
	else:
		print( "Unmatched Packet [" + binascii.b2a_hex(id) + "], out of sync?" )
		#return "E"
	return id

