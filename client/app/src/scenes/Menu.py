# Import ----------------------------------------
from src.properties import *
from Core.core import *	

# Screen ----------------------------------------
screen = Window(int(cfg["MAIN"]["W"]), int(cfg["MAIN"]["H"]))

# Import style ----------------------------------
style = Style()
style.importFromConfig(cfg)

# GUI Callback ----------------------------------
# Create Game Button Click
def createGameB_click(obj):
	Scene.set("Create")

# Connect Button Click
def connectB_click(obj):
	Scene.set("Connect")

# Settings Button Click
def settingsB_click(obj):
	Scene.set("Settings")

# Exit Button Click
def exitB_click(obj):
	quit()

# GUI -------------------------------------------
## Frame
frame = Frame(screen, style)

## Border
border = Border(screen, style)

## Label
titleL = Label(screen, style, 1, screen.h - 2, "Tic Tac Toe by Sinus44 [21.12.2022]")

## List
elementG = Group(screen, 3, 3)

### Create Game Button
createGameB = Button(screen, style, 0, 0, "[ CREATE GAME ]")
createGameB.click = createGameB_click
elementG.append(createGameB)

### Connect Button
connectB = Button(screen, style, 0, 0, "[ CONNECT ]")
connectB.click = connectB_click
elementG.append(connectB)

### Settings Button
settingsB = Button(screen, style, 0, 0, "[ SETTINGS ]")
settingsB.click = settingsB_click
elementG.append(settingsB)

### Exit Button
exitB = Button(screen, style, 0, 0, "[ EXIT ]")
exitB.click = exitB_click
elementG.append(exitB)

### List Sorting
elementG.sort()

## Logo
logo = Image("./assets/sample.bmp", True)

# Scene -----------------------------------------
class Menu:
	"""Сцена меню"""
	def play():
		for event in Input.getEvents():
			elementG.eventHandler(event)
			if event.type == Input.Types.Mouse:
				if event.mouseType == Input.Mouse.CLICK:
					if event.mouseKey == Input.Mouse.LEFT:
						elementG.click()

		frame.draw()
		border.draw()
		screen.paste(logo, 19, 9)
		elementG.draw()
		titleL.draw()
		screen.draw()