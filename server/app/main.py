import socket
import json
import threading
import random
import time

version = 1

class Server:
	def __init__(self, handlerClass, port=30120, addr="127.0.0.1", maxConnections=20):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.maxConnections = maxConnections
		self.handlerClass = handlerClass
		self.maxData = 1024
		self.listning = False
		self.conections = []
		self.addr = addr
		self.port = port

	def getLocalIp(self):
		"""Получение локального IP адреса"""
		return socket.gethostbyname(socket.gethostname())

	def dataListner(self, conn):
		"""Слушатель команд для каждого юзера"""
		while True:
			data = conn.recv(self.maxData).decode("UTF-8")

			if not data:
				self.error(conn, "data empty")
				conn.close()
				return

			d = json.loads(data)
			callbackRes = self.handlerClass.__dict__[d["command"]](d["args"])
			callbackResJSON = json.dumps(callbackRes)
			
			self.send(conn, callbackResJSON)

	def start(self):
		"""Начало работы сервера, прослушивание входящих соединений, команд"""
		self.socket.bind((self.addr, self.port))
		self.listning = True
		self.socket.listen(self.maxConnections)

		while self.listning:
			conn, addr = self.socket.accept()

			connect = threading.Thread(target=self.dataListner, args=[conn])
			connect.start()
			self.conections.append(connect)
	
	def error(self, connection, text):
		"""Отправка ошибки клиенту"""
		self.send(connection, '{"status":"bad", "args": {"error":"' + str(text) + '"}')
	
	def send(self, connection, text):
		"""Отправка данных клиенту"""
		connection.sendall(bytes(text, "UTF-8"))

games = []

class Player:
	"""Класс игрока"""
	def __init__(self, nickname, symbol):
		self.nickname = nickname
		self.secretCode = random.randint(100, 999)
		self.symbol = symbol

class Game:
	"""Класс игры"""
	def __init__(self, visible, private, password):
		self.visible = visible
		self.private = private
		self.password = password
		self.plane = [
			["","",""],
			["","",""],
			["","",""]
		]
		self.users = []
		self.started = False
		self.step = "X"
	
	def checkWin(self):
		winCombinations = [
			[
				[1,1,1],
				[0,0,0],
				[0,0,0]
			],
			[
				[0,0,0],
				[1,1,1],
				[0,0,0]
			],
			[
				[0,0,0],
				[0,0,0],
				[1,1,1]
			],
			[
				[1,0,0],
				[1,0,0],
				[1,0,0]
			],
			[
				[0,1,0],
				[0,1,0],
				[0,1,0]
			],
			[
				[0,0,1],
				[0,0,1],
				[0,0,1]
			],
			[
				[1,0,0],
				[0,1,0],
				[0,0,1]
			],
			[
				[0,0,1],
				[0,1,0],
				[1,0,0]
			],
		]
		
	def addUser(self, nickname, symbol):
		"""Добавление нового игрока в список игроков"""
		user = Player(nickname, symbol)
		self.users.append(user)
		return user

class ServerHandler:
	def create_game(args):
		"""Создание игры"""

		gameid = len(games)
		games.append(Game(
			args["visible"],
			args["private"],
			args["password"]
		))

		symbol = random.choice(["X","0"])
		user = games[gameid].addUser(args["nickname"], symbol)

		return {
			"status": "ok",
			"args": {
				"game_id": gameid,
				"secret_code": user.secretCode,
				"symbol": user.symbol,
				"step": games[gameid].step
			}
		}

	def connect_to_game(args):
		"""Подключение к игре"""

		gameid = int(args["game_id"])

		if not (gameid < len(games)):
			return {
				"status": "bad",
				"args": {
					"error":"Game ID incorrect"
				}
			}
		
		if len(games[gameid].users) != 1:
			return {
				"status": "bad",
				"args": {
					"error":"Max players connected"
				}
			}
		
		if games[gameid].users[0].nickname == args["nickname"]:
				return {
					"status": "bad",
					"args": {
						"error": "Nickname used"
					}
				}

		if (games[gameid].private == "True" and games[gameid].password == args["password"]) or games[gameid].private == "False":
			symbol = "0" if games[gameid].users[0].symbol == "X" else "X" 

			user = games[gameid].addUser(args["nickname"], symbol)
			games[gameid].started = True

			return {
				"status": "ok",
				"args": {
					"secret_code": user.secretCode,
					"symbol": symbol,
					"step": games[gameid].step
				}
			}

		return {
			"status": "bad",
			"args": {
				"error": "Password incorrect"
			}
		}

	def check_start_game(args):
		"""Ожидание подключения второго игрока"""

		gameid = int(args["game_id"])
		while not games[gameid].started:
			time.sleep(1)

		return {
			"status": "ok",
			"args": {	
				"game": "started"
			}
		}

	def set_symbol(args):
		"""Внесение изменений в игровое поле"""

		game = games[int(args["game_id"])]
		
		symbol = ""

		if args["secret_code"] == game.users[0].secretCode:
			symbol = game.users[0].symbol

		elif args["secret_code"] == game.users[1].secretCode:
			symbol = game.users[1].symbol
		
		else:
			return {
				"status":"bad",
				"args": {
					"error":"Secret code fail"
				}
			}
		
		if symbol != game.step:
			return {
				"status":"bad",
				"args": {
					"error":"Not your step"
				}
			}

		game.plane[int(args["x"])][int(args["y"])] = symbol
		
		if symbol == "0":
			game.step = "X"

		elif symbol == "X":
			game.step = "0"

		return {
			"status": "ok",
			"args": {
				"plane": game.plane,
				"step": game.step
			}
		}
	
	def await_change(args):
		"""Ожидание изменений на поле"""
		
		user = None
		game = games[int(args["game_id"])]

		if args["secret_code"] == game.users[0].secretCode:
			user = game.users[0]
		
		elif args["secret_code"] == game.users[1].secretCode:
			user = game.users[1]
		
		if user is None:
			return {
				"status": "bad",
				"args": {
					"error": "Secret code incorrect"
				}
			}


		while games[int(args["game_id"])].step != user.symbol:
			pass

		return {
			"status": "ok",
			"args": {
				"plane": games[int(args["game_id"])].plane,
				"step": games[int(args["game_id"])].step
			}
		}
	
	def check_version(args):
		"""Проверка версии клиента"""
		if args["client_version"] != version:
			return {
				"status": "bad",
				"args": {
					"required_version": version,
					"error": "unsupported version"
				}
			}
		else:
			return {
				"status": "ok",
				"args": {
					"version_check": "ok"
				}
			}
	
	#def getPlayerFromSecretCode(gameid, secretcode):
	#	if args["secret_code"] == game.users[0].secretCode:
	#		return game.users[0]
	#	
	#	elif args["secret_code"] == game.users[1].secretCode:
	#		return game.users[1]
	#	
	#	else:
	#		return None

serv = Server(ServerHandler)
serv.addr = serv.getLocalIp()
serv.start()