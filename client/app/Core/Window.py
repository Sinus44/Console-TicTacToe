import ctypes
from Core.Color import Color

class Window:
	"""Окно - Класс окна для отрисовки ИЗО в консоли"""

	def __init__(self, w=10, h=10):
		self.w = w
		self.h = h

	def draw(self):
		"""Вывод буффера в консоль"""
		s = ""
		for i in range(self.h - 1):
			s += "".join(self.buffer[i])

		s += "".join(self.buffer[self.h - 1])
		ctypes.windll.kernel32.WriteConsoleW(ctypes.windll.kernel32.GetStdHandle(-11), s, len(s))

	def clear(self, fast=True):
		"""Отчистка вывода в консоль"""
		if fast: print("\033[J")
		else: os.system("cls")

	def fill(self, symbol=" "):
		"""Заливка всего буффера"""
		self.buffer = []
		for i in range(self.h):
			self.buffer.append([])
			for j in range(self.w):
				self.buffer[i].append(symbol)

	def point(self, x=0, y=0, symbol="*"):
		"""Установка символа в буффер по координатам"""
		if (0 <= x < self.w) and (0 <= y < self.h):
				self.buffer[y][x] = symbol
		else: print("ERROR")

	def rectFill(self, x=0, y=0, w=1, h=1, symbol="*"):
		"""Заполненный прямоугольник в буффер"""
		for i in range(h):
			for j in range(w):
				self.buffer[i+y][j+x] = symbol

	def rect(self, x=0, y=0, w=1, h=1, symbol="*"):
		"""Пустотелый прямоугольник в буффер"""
		for i in range(h):
			for j in range(w):
				if i == 0 or i == h-1 or j == 0 or j == w - 1:
					self.point(j + x, i + y, symbol)

	def circleFill(self, x=0, y=0, r=1, symbol="*"):
		"""Залитый круг в буффер"""
		for i in range(self.h):
			for j in range(self.w):
				if (i - y) ** 2 + (j - x) **2  <= r ** 2:
					self.buffer[i][j] = symbol

	def circle(self, x=0, y=0, r=1, symbol="*"):
		"""Пустотелый круг в буффер"""
		disp_x = x
		disp_y = y
		x = 0
		y = r
		delta = (1 - 2 * r)
		error = 0
		while y >= 0:
			self.point(disp_x + x, disp_y + y, symbol)
			self.point(disp_x + x, disp_y - y, symbol)
			self.point(disp_x - x, disp_y + y, symbol)
			self.point(disp_x - x, disp_y - y, symbol)

			error = 2 * (delta + y) - 1
			if ((delta < 0) and (error <=0)):
				x+=1
				delta = delta + (2*x+1)
				continue
			error = 2 * (delta - x) - 1
			if ((delta > 0) and (error > 0)):
				y -= 1
				delta = delta + (1 - 2 * y)
				continue
			x += 1
			delta = delta + (2 * (x - y))
			y -= 1

	def line(self, x1=0, y1=0, x2=0, y2=0, symbol="*"):
		"""Линия по координатам"""
		delX = abs(x2 - x1)
		delY = abs(y2 - y1)

		signX, signY = 0, 0

		if x1 < x2: signX = 1
		else: signX = -1

		if y1 < y2: signY = 1
		else: signY = -1

		error = delX - delY
		self.point(x2, y2, symbol)

		while (x1 != x2 or y1 != y2): 
			self.point(x1, y1, symbol)
			error_2 = error * 2
		
			if error_2 > -delY: 
				error -= delY
				x1 += signX
		
			if error_2 < delX:
				error += delX
				y1 += signY

	def paste(self, frame, x=0, y=0):
		"""Вставка буффера другого объекта в текущий"""
		if x + frame.w > self.w or y + frame.h > self.h:
			print("ERROR")
			return

		for i in range(len(frame.buffer)):
			for j in range(len(frame.buffer[0])):
				if frame.buffer[i][j] == 0:
					continue
				self.buffer[i+y][j+x] = frame.buffer[i][j]

	def text(self, text="TEXT", x=0, y=0, wordPrefix="", symbolPrefix="", wordPostfix="", symbolPostfix=""):
		"""Текст"""
		if (x < 0 or y < 0) or (x + len(text) > self.w):
			print("ERROR")
			return

		for i in range(len(text)):
			self.buffer[y][x+i] = (wordPrefix if i == 0 else "") + symbolPrefix + text[i] + symbolPostfix + (wordPostfix if i == len(text) - 1 else "")