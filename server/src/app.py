import socket	
import threading	
import pickle
import os

def pack(data):
	return pickle.dumps(data)

def unpack(data):
	return pickle.loads(data)

# Gracze
players = {}

def handle_client(c): # Obsługa klienta asynchronicznie w wątku
	global players
	while(1):
		try:
			data = unpack(c.recv(2048))
			# print(data)
			pid = data['pid']
			players[pid] = data

			if not data:
				print('Client disconnected')
				break

			c.send(pack(players))

		except Exception as e:
			print(e)
			break
		
	c.close()

# Stworzenie socketa
s = socket.socket()
port = os.environ['PORT'] or 3100
s.bind(('0.0.0.0', port))		
print ("Socket bound to port %s" %(port))

s.listen()	

while True:
	c, addr = s.accept()	
	print ('Incoming connection from', addr)
	t1 = threading.Thread(target = handle_client, args=(c, ))
	t1.start()
	