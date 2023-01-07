class Scene:
	"""Класс для управления отображаемыми сценами"""

	list = {}
	selected = ""
	prev = ""

	def set(name):
		"""Установка сцены по имени"""
		Scene.prev = Scene.selected
		Scene.selected = name

	def add(name, scene):
		"""Добавление сцены"""
		Scene.list[name] = scene

	def addFromDict(scenes):
		"""Импорт сцен из объекта формата { name:scene }"""
		for scene in scenes:
			Scene.add(scene, scenes[scene])

	def play():
		"""Воспроизведение сцены"""
		Scene.list[Scene.selected].play()