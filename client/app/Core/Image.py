import PIL.Image
from Core.Mmath import Mmath
from Core.Color import Color

class Image:
	"""Импорт картинок пригодных для вставки в Window"""
	def __init__(self, path, alpha=False):
		self.file = PIL.Image.open(path)
		self.img = self.file.load()

		self.w = self.file.size[0]
		self.h = self.file.size[1]
		self.alpha = alpha

		self.createBuffer()

	def createBuffer(self):
		self.buffer = []

		for y in range(self.h):
			self.buffer.append([])
			for x in range(self.w):
				color = self.img[x, y] # Получаем цвет пикселя в оригинальном изо
				self.buffer[y].append(self.getColor(color)) # прибавляем к строке соответсвующий символ

	def getColor(self, color):
		if self.alpha:
			if not(color[0]) and not(color[2]) and not(color[2]):
				return 0

		return Color.Background.rgb(color[0], color[1], color[2]) + " "