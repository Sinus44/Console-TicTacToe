# Import ----------------------------------------
from Engine import *	
from src.Client import * 
from src.properties import *

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

def checkConnectB_click(obj):
	if not Client.connected:
		Client.init(cfg["SERVER"]["ip"], int(cfg["SERVER"]["port"]))
		Client.connect()

	if Client.connected:
		createGameB.enable = True
		connectB.enable = True

# Settings Button Click
def settingsB_click(obj):
	Scene.set("Settings")

# Exit Button Click
def exitB_click(obj):
	Client.close()
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
createGameB = Button(screen, style, 0, 0, "CREATE GAME", Client.connected)
createGameB.click = createGameB_click
elementG.append(createGameB)

### Connect Button
connectB = Button(screen, style, 0, 0, "CONNECT", Client.connected)
connectB.click = connectB_click
elementG.append(connectB)

### Check Connect Button
checkConnectB = Button(screen, style, 0, 0, "CHECK CONNECT")
checkConnectB.click = checkConnectB_click
elementG.append(checkConnectB)

### Settings Button
settingsB = Button(screen, style, 0, 0, "SETTINGS")
settingsB.click = settingsB_click
elementG.append(settingsB)

### Exit Button
exitB = Button(screen, style, 0, 0, "EXIT")
exitB.click = exitB_click
elementG.append(exitB)

### List Sorting
elementG.sort()

## Logo
logo = ImageBMP("./assets/Logo.bmp", True)

# Scene -----------------------------------------
class Menu:
	"""Сцена меню"""
	
	def play():
		elementG.eventHandler()
		if Input.eventType == Input.Types.Mouse:
			if Input.mouseType == Input.Mouse.DOWN and not Input.prevMouseState:
				if Input.mouseKey == Input.Mouse.LEFT:
					elementG.click()

		frame.draw()
		border.draw()
		screen.paste(logo, 19, 9)
		elementG.draw()
		titleL.draw()
		screen.draw()