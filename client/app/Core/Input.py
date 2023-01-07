import ctypes
from ctypes.wintypes import *
from Core.Logging import Logging

# CTYPES ADAPTATE -------------------------------

#KEYBOARD
class CHAR_UNION(ctypes.Union):
    _fields_ = [("UnicodeChar", WCHAR),
                ("AsciiChar", CHAR)]

class KEY_EVENT_RECORD(ctypes.Structure):
    _fields_ = [("bKeyDown", BYTE),
                ("pad2", BYTE),
                ('pad1', SHORT),
                ("wRepeatCount", SHORT),
                ("wVirtualKeyCode", SHORT),
                ("wVirtualScanCode", SHORT),
                ("uChar", CHAR_UNION),
                ("dwControlKeyState", INT)]

#MOUSE
class MOUSE_EVENT_RECORD(ctypes.Structure):
    _fields_ = [("dwMousePosition", ctypes.wintypes._COORD),
                ("dwButtonState", INT),
                ("dwControlKeyState", INT),
                ("dwEventFlags", INT)]

#WINDOW BUFFER SIZE
class WINDOW_BUFFER_SIZE_RECORD(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.wintypes._COORD)]

#MENU
class MENU_EVENT_RECORD(ctypes.Structure):
    _fields_ = [("dwCommandId", UINT)]

#FOCUS
class FOCUS_EVENT_RECORD(ctypes.Structure):
    _fields_ = [("bSetFocus", BYTE)]

#UNION
class INPUT_UNION(ctypes.Union):
    _fields_ = [("KeyEvent", KEY_EVENT_RECORD),
                ("MouseEvent", MOUSE_EVENT_RECORD),
                ("WindowBufferSizeEvent", WINDOW_BUFFER_SIZE_RECORD),
                ("MenuEvent", MENU_EVENT_RECORD),
                ("FocusEvent", FOCUS_EVENT_RECORD)]

#RECORD
class INPUT_RECORD(ctypes.Structure):
    _fields_ = [("EventType", SHORT),
                ("Event", INPUT_UNION)]

#RECORDS ARRAY
class INPUT_RECORD_ARRAY(ctypes.Structure):
	_fields_ = [("Records", INPUT_RECORD * 64)]

# -----------------------------------------------

class Input:
	"""Класс для получения входных ивентов консоли"""

	EVENTS = []

	spec = " _+=-!@#$%^&*()<>.,~`|/\{}[];:'"
	numbers = "1234567890"
	
	angCaps = "QWERTYUIOPASDFGHJKLZXCVBNM"
	ang = angCaps.lower()

	ruCaps = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
	ru = ruCaps.lower()

	listning = True

	class Types:
		Keyboard = 1
		Mouse = 2
		Window = 4
		Menu = 8
		Focus = 16

	class Mouse:
		#Mouse type:
		CLICK = 0
		MOVE = 1
		DOUBLECLICK = 2
		WHEELV = 4
		WHEELH = 8

		#Mouse key:
		NULL = 0
		LEFT = 1
		RIGHT = 2

	class Keyboard:
		class Keys:
			F1 = 112
			F2 = 113
			F3 = 114
			F4 = 115
			F5 = 116
			F6 = 117
			F7 = 118
			F8 = 119
			F9 = 120
			F10 = 121
			F11 = 122
			F12 = 123

			SPACE = 32
			BACKSPACE = 8
			TAB = 9
			ENTER = 13
			SHIFT = 16
			CTRL = 17
			ALT = 18
			CAPS = 20
			ESC = 27
			INSERT = 45
			PAGEUP = 33
			PAGEDOWN = 34
			END = 35
			HOME = 36
			DELETE = 46
			PRTSC = 44
			SCROLLLOCK = 145

			WINL = 91
			WINR = 92

			LEFT = 37
			UP = 38
			RIGHT = 39
			DOWN = 40

		DOWN = 1
		UP = 0

	class Window:
		pass

	class Menu:
		pass

	class Focus:
		pass

	class Event:
		def __init__(self, type=-1, mouseKey=-1, mouseX=-1, mouseY=-1, mouseType=-1, keyboardCode=-1, keyboardChar=-1, keyboardState=-1):
			self.type = type

			self.mouseType = mouseType
			self.mouseKey = mouseKey
			self.mouseX = mouseX
			self.mouseY = mouseY

			self.keyboardCode = keyboardCode
			self.keyboardChar = keyboardChar
			self.keyboardState = keyboardState

		def __str__(self):
			return f"Type: {self.type}\nmouseType: {self.mouseType}\nMouseKey: {self.mouseKey}\nMouseX: {self.mouseX}\nMouseY: {self.mouseY}\nKeyboardCode: {self.keyboardCode}\nKeyboardChar: {self.keyboardChar}\nKeyboardState: {self.keyboardState}\n"

	def init():
		Input.handle = ctypes.windll.kernel32.GetStdHandle(-10)
		Input.events = ctypes.wintypes.DWORD()
		Input.InputRecord = INPUT_RECORD()

	def start():
		Input.listning = True

	def stop():
		Input.listning = False

	def mode(useHotkey=False, lineInput=False, echo=False, resizeEvents=False, mouseEvents=False, insert=False, quickEdit=False, extended=False):
		out = 0x0

		if useHotkey: out += 0x1
		if lineInput: out += 0x2
		if echo: out += 0x4
		if resizeEvents: out += 0x8
		if mouseEvents: out += 0x10
		if insert: out += 0x20
		if quickEdit: out += 0x40
		if extended: out += 0x80

		ctypes.windll.kernel32.SetConsoleMode(Input.handle, out)

	def tick():
		if not Input.listning: return

		ctypes.windll.kernel32.ReadConsoleInputW(Input.handle, ctypes.byref(Input.InputRecord), 1, ctypes.byref(Input.events))

		record = Input.InputRecord

		event = record.Event
		eventType = record.EventType

		mouseX = event.MouseEvent.dwMousePosition.X # X
		mouseY = event.MouseEvent.dwMousePosition.Y # Y
		mouseKey = event.MouseEvent.dwButtonState # какая кнопка клавиатуры нажата
		mouseType = event.MouseEvent.dwEventFlags # колесо / нажатие / движение / двойное нажатие

		keyboardCode = event.KeyEvent.wVirtualKeyCode # Код кнопки клавиатуры
		keyboardChar = event.KeyEvent.uChar.UnicodeChar # Символ клавиши
		keyboardState = event.KeyEvent.bKeyDown # Состояние кнопки

		event = Input.Event(type=eventType, mouseType=mouseType, mouseKey=mouseKey, mouseX=mouseX, mouseY=mouseY, keyboardCode=keyboardCode, keyboardChar=keyboardChar, keyboardState=keyboardState)
		Input.EVENTS.append(event)

	def clearEvents():
		Input.EVENTS = []

	def getEvents(tick=False):
		if tick: Input.tick()

		for event in Input.EVENTS:
			if len(Input.EVENTS):
				event = Input.EVENTS.pop()
				yield event
			else:
				return []