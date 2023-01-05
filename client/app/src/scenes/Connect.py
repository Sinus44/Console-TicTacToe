# Import ----------------------------------------
from src.properties import *
from Core.core import *

# Screen ----------------------------------------
screen = Window(int(cfg["MAIN"]["W"]), int(cfg["MAIN"]["H"]))

# Import style ----------------------------------
style = Style()
style.importFromConfig(cfg)

# GUI Callback ----------------------------------
## GameID Textbox Select
def gameIdTb_select(obj):
    passwordTb.selected = False

## Password Checkbox Change
def privateGameCb_Change(obj):
    if not obj.checked: passwordTb.block()
    passwordTb.enable = obj.checked

## Password Textbox Select
def passwordTb_select(obj):
    gameIdTb.selected = False

## Connect Button
def connectB_click(obj):
    if not str(gameIdTb): return

    request = {
        "command": "connect_to_game",
        "args": {
            "game_id": gameIdTb.value,
            "private": str(bool(privateGameCb)),
            "password": passwordTb.value if privateGameCb else "",
            "nickname": cfg["USER"]["nickname"]
        }
    }

    #Logging.log(request)

## Back Button
def backB_click(obj):
    Scene.set(Scene.prev)

# GUI -------------------------------------------
## Frame
frame = Frame(screen, style)

## Border
border = Border(screen, style)

## List
elementG = Group(screen, int(cfg["MAIN"]["W"]) // 3, 3)

### Textbox
gameIdTb = Textbox(screen, style, 0, 0, "Game ID", True, 3, Input.numbers)
gameIdTb.select = gameIdTb_select
elementG.append(gameIdTb)

### Private Game Checkbox
privateGameCb = Checkbox(screen, style, 0, 0, "PRIVATE GAME")
privateGameCb.change = privateGameCb_Change
elementG.append(privateGameCb)

### Password Textbox
passwordTb = Textbox(screen, style, 0, 0, "Password", False, 16, Input.numbers)
passwordTb.select = passwordTb_select
elementG.append(passwordTb)

### Connect Button
connectB = Button(screen, style, 0, 0, "[ CONNECT ]")
connectB.click = connectB_click
elementG.append(connectB)

### Back Button
backB = Button(screen, style, 0, 0, "[ BACK ]")
backB.click = backB_click
elementG.append(backB)

### Status Label
statusL = Label(screen, style)
elementG.append(statusL)

### List Sorting
elementG.sort()

# Scene -----------------------------------------
class Connect:
    """Сцена подключения к игре"""
    def play():
        for event in Input.getEvents():
            elementG.eventHandler(event)
            if event.type == Input.Types.Mouse:
                if event.mouseType == Input.Mouse.CLICK:
                    if event.mouseKey == Input.Mouse.LEFT:
                        elementG.click()

        frame.draw()
        border.draw()
        elementG.draw()
        screen.draw()

