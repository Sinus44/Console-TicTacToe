import socket
import json
from Core.core import *

class Client:
	def __init__(self, address, port):
		self.address = address
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.address, self.port))

	def send(self, data):
		self.socket.sendall(data)
		res = self.socket.recv(1024)

		if not res:
			return ""

		return res.decode("UTF-8")

	def startLisningAsync(self, callback):
		pass

	def stop(self):
		self.socket.close()

#k = c.send(b"stopgame")
#print(k)

#c.stop()
#c.lisningSync()

