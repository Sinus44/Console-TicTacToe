import socket
import random
import json

"""
methods:

start game
move
leave

args:

gameid
secret code


PROTOCOL:

{
	"command": "start" or "commandid": 0 

	"args": {
		"password":"123"
	}
}

{
	"command": ""
}

"""

ADDRESS = "192.168.0.12"
PORT = 3030

class Server:
	def __init__(self, addr, port, maxConnections, handlerClass):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((addr,port))
		self.maxConnections = maxConnections
		self.handlerClass = handlerClass

	def start(self):
		self.socket.listen(self.maxConnections)

		conn, addr = self.socket.accept()

		data = conn.recv(1024)

		if not data:
			self.socket.close()
			print("ERROR RECIVED DATA IS NONE")
			return

		data = data.decode("UTF-8")

		d = json.loads(data)

		conn.sendall(json.dumps(self.handlerClass.__dict__[d["command"]](d["args"])).encode("utf-8"))

		#print(d)

		#if data == "startgame":
		#	conn.sendall(b"OK")

		#elif data == "stopgame":
		#	conn.sendall(b"GAME STOPPED!")

		#self.socket.close()

		"""
		while True:
			data = conn.recv(1024) # Получаем данные из сокета.

			if not data:
				continue

			data = data.decode("UTF-8")

			if data == "startgame":
				conn.sendall(b"OK")
			elif data == "stopgame":
				conn.sendall(b"GAME STOPPED!")

			self.socket.close()
		"""



"""
games = []

class Game:
	def __init__(self, id, password):
		#print(f"Created game\nID: {id}\nPASSWORD: {password}\n")
		self.password = password
		self.id = id
		self.plane = [
			[0,0,0],
			[0,0,0],
			[0,0,0]
		]

	def step(self, symbol, posx, posy):
		self.plane[posy][posx] = symbol

class ServerHandler:
	def createGame(args):
		try:
			gameId = len(games)
			#print(f"ARGS:\n{args}")
			games.append(Game(gameId, args["password"]))
		except:
			return {"status":"bad"}
		return {"status":"ok","args":{"id":gameId}}

	def checkStat(args):
		return {"status": "ok"}

	def connect(args):
		pass

	def step(args):
		pass

serv = Server(ADDRESS, PORT, 1, ServerHandler)
serv.start()
"""