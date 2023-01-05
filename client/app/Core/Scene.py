from Core.Logging import Logging

class Scene:

	list = {}
	selected = ""
	prev = ""

	"""
	def set2(scene):
		if Scene.scene:
			Scene.prevScene = Scene.scene

			if "stop" in Scene.scene.__dict__:
				Logging.log(str(Scene.scene.stop))
				Scene.scene.stop()

		Scene.scene = scene
		if "init" in Scene.scene.__dict__:
			Scene.scene.init()
	"""

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
		#Scene.scene.play()
		Scene.list[Scene.selected].play()