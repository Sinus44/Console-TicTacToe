import socket
import json

class Client:
	"""Класс для работы с сервером"""

	def init(address, port):
		Client.address = address
		Client.port = port
		Client.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		Client.maxData = 1024
		Client.connected = False

	def connect():
		try:
			Client.socket.connect((Client.address, Client.port))
			Client.connected = True
		except:
			Client.connected = False

	def send(request):
		if not Client.connected: return

		code = Client.encode(request)
		byteRequest = bytes(code, "utf-8")

		Client.socket.sendall(byteRequest)
		res = Client.socket.recv(Client.maxData)
		decodeRes = Client.decode(res.decode("UTF-8"))

		Client.debugFunc(f"\nREQUEST: {str(request)}\nRESPONSE: {str(decodeRes)}")
		return decodeRes

	def debugFunc(data):
		pass

	def encode(obj):
		return json.dumps(obj)

	def decode(str):
		return json.loads(str)

	def close():
		Client.connected = False
		Client.socket.close()