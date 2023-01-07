import ctypes
import os

class Output:
	"""Класс для настройки выходного буффера окна консоли"""
	handle = None

	def init():
		Output.handle = ctypes.windll.kernel32.GetStdHandle(-11)

	def mode(mode=5):
		ctypes.windll.kernel32.SetConsoleMode(Output.handle, mode)
	
	def getTitle():
		out = (ctypes.c_char * 256)()
		ctypes.windll.kernel32.GetConsoleTitleW(ctypes.byref(out), ctypes.wintypes.DWORD(256))
		return str(bytes(out), encoding="utf-8")

	def title(title="Console Engine by Sinus"):
		ctypes.windll.kernel32.SetConsoleTitleW(title)
	
	def resize(w=60, h=40):
		os.system(f'mode con cols={w} lines={h}')
