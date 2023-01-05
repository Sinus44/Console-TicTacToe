class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def length(self):
		"""Длина вектора"""
		return (x ** 2 + y ** 2) ** 0.5
	
	def __add__(self, y):
		"""Сложение векторов"""
		if type(y) == type(self):
			self.x += y.x
			self.y += y.y
			return self

		if type(y) == type(0):
			self.x += y
			self.y += y
			return self
		
		return 0