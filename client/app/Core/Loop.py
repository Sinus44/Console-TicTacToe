import threading
import time

class Loop:
	def __init__(self, callback, t=1, daemon=False):
		self.on = False
		self.callback = callback
		self.time = t
		self.thread = threading.Thread(target=self.f, daemon=daemon)

	def start(self):
		self.on = True
		self.thread.start()
	
	def f(self):
		while self.on:
			self.callback()
			time.sleep(self.time)

	def stop(self):
		self.on = False	