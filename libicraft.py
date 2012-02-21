import struct, random
ids = [46,49,7,57,322]
def stringify(text):
        msg = "\x00" + "\x00".join(list(text))
	return chr(len(text))+msg

def minemsg(text):
	return "\x03\x00"+stringify(text)

def handshake(nickname):
        return "\x02\x00"+stringify(nickname)

def login(nickname):
	return "\x01\x00\x00\x00\x17\x00"+stringify(nickname)+"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

def join(nickname):
	return handshake(nickname)+login(nickname)

def creativedrop():
	return "\x6B\xFF\xFF" + struct.pack('>h', random.choice(ids)) + "\x40\x00\x00"

def get_info(s):
	s.send('\xfe')
	s.settimeout(10)
	d = s.recv(256)
	assert d[0] == '\xff'
	d = d[3:].decode('utf-16be').split(u'\xa7')
	return {'motd':            d[0],
	        'players':     int(d[1]),
	        'max_players': int(d[2])}

def parse_ip(target, default=25565):
	srv = target.replace("\n","").split(":")
	if len(srv) == 1:
	        prt = default
	else:
	        prt = int(srv[1])
	return {'ip':	srv[0],
		'port':	prt}
	


