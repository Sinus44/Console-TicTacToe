import threading
import time

class Interval:
	"""Класс цикличного вызова функции в соответветсвии с интервалом"""
	def __init__(self, callback, t=1, daemon=False):
		self.on = False
		self.callback = callback
		self.time = t
		self.thread = threading.Thread(target=self.function, daemon=daemon)

	def start(self):
		self.on = True
		self.thread.start()

	def stop(self):
		self.on = False
	
	def function(self):
		while self.on:
			self.callback()
			time.sleep(self.time)