import time
import timeit

class Performance:
	"""Класс оценки производительности, замеров времени выполнения кода, по точкам или функции"""
	startTime = 0
	
	def start():
		Performance.startTime = time.time()
	
	def time():
		return time.time() - Performance.startTime

	def function(f, repeats=1, count=1):
		return timeit.repeat(f, repeat=repeats, number=count)