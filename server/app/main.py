import socket
import json
import threading
import random
import time

from Engine import *

version = 1

class Server:
	def __init__(self, handlerClass, port, addr="127.0.0.1", maxConnections=20):
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
		enable = True
		while enable:
			try:
				data = conn.recv(self.maxData).decode("UTF-8")

				if not data:
					self.error(conn, "data empty")
					conn.close()
					return

				d = json.loads(data)
				callbackRes = self.handlerClass.__dict__[d["command"]](d["args"])
				callbackResJSON = json.dumps(callbackRes)
				
				self.send(conn, callbackResJSON)
			
			except:
				self.debug("Произошла неизвестная ошибка или пользователь отключился")
				enable = False

	def start(self):
		"""Начало работы сервера, прослушивание входящих соединений, команд"""
		self.socket.bind((self.addr, self.port))
		self.listning = True
		self.socket.listen(self.maxConnections)

		while self.listning:
			conn, addr = self.socket.accept()
			self.debug(f"Подключен новый пользовательm IP:{addr}")

			connect = threading.Thread(target=self.dataListner, args=[conn])
			connect.start()
			self.conections.append(connect)
	
	def error(self, connection, text):
		"""Отправка ошибки клиенту"""
		self.debug(text)
		self.send(connection, '{"status":"bad", "args": {"error":"' + str(text) + '"}')
	
	def send(self, connection, text):
		"""Отправка данных клиенту"""
		connection.sendall(bytes(text, "UTF-8"))

	def debug(text):
		pass

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
		self.end = False
		self.winner = ""
	
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

		for user in self.users:
			userPlane = []
			for i in range(len(self.plane)):
				userPlane.append([])
				for j in range(len(self.plane[i])):
					userPlane[i].append(1 if self.plane[i][j] == user.symbol else 0)

			if userPlane in winCombinations:
				self.end = True
				self.winner = user.nickname

	def checkFree(self):
		emptyCells = 0
		for i in range(len(self.plane)):
				for j in range(len(self.plane[i])):
					emptyCells += 1 if self.plane[i][j] == "" else 0

		if not emptyCells:
			self.end = True
			self.winner = "Ничья"
		
	def addUser(self, nickname, symbol):
		"""Добавление нового игрока в список игроков"""
		user = Player(nickname, symbol)
		self.users.append(user)
		return user

class ServerHandler:
	def debug(text):
		pass

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
		Logging.print(f"{args['nickname']} создал игру ID: {gameid}")

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

		if game.end:
			return {
				"status":"bad",
				"args": {
					"error":"Game End"
				}
			}

		if game.plane[int(args["x"])][int(args["y"])] != "":
			return {
				"status": "bad",
				"args": {
					"error": "Cell pointed"
				}
			}
		
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
		game.checkWin()
		game.checkFree()

		if symbol == "0":
			game.step = "X"

		elif symbol == "X":
			game.step = "0"

		return {
			"status": "ok",
			"args": {
				"plane": game.plane,
				"step": game.step,
				"end": game.end,
				"winner": game.winner
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
				"step": games[int(args["game_id"])].step,
				"end": games[int(args["game_id"])].end,
				"winner": games[int(args["game_id"])].winner
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

# Config import
cfg = Config("config.cfg", False)
cfg.read()

# Var's init
port = int(cfg["MAIN"]["port"])
maxConnections = int(cfg["MAIN"]["maxconnections"])
version = int(cfg["MAIN"]["version"])
defaultIP = "127.0.0.1"

#
Output.title(f"Tic Tac Toe Server")

# Logging
Logging.print(f"Запуск сервера...")
Logging.print(f"Версия протокола: {version}")
Logging.print(f"Сетевой порт: {port}")
Logging.print(f"Максимум подключений: {maxConnections}")
Logging.print(f"Стандартный IP: {defaultIP}")

# Server creating
serv = Server(ServerHandler, port, defaultIP, maxConnections)
serv.addr = serv.getLocalIp()
serv.debug = Logging.print

Logging.print("=" * 20)
Logging.print("Сервер запущен")
Logging.print(f"Текущий IP: {serv.addr}")
try:
	serv.start()
except:
	Logging.print("Ошибка запуска")