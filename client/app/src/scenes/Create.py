# Import ----------------------------------------
from src.properties import *
from Core.core import *	

# Screen ----------------------------------------
screen = Window(int(cfg["MAIN"]["W"]), int(cfg["MAIN"]["H"]))

# Import style ----------------------------------
style = Style()
style.importFromConfig(cfg)

# GUI Callback ----------------------------------
## Back Button
def backB_click(obj):
    Scene.set(Scene.prev)

## Create Button
def createB_click(obj):
    request = {
        "command": "create_game",
        "args": {
            "visible": str(bool(publicListCb)),
            "private": str(bool(privateGameCb)),
            "password": passwordTb.value if privateGameCb else "",
            "nickname": cfg["USER"]["nickname"]
        }
    }

    #Logging.log(request)

## Password Checkbox Change
def privateGameCb_Change(obj):
    if not obj.checked: passwordTb.block()
    passwordTb.enable = obj.checked

# GUI -------------------------------------------
## Frame
frame = Frame(screen, style)

## Border
border = Border(screen, style)

## List
elementG = Group(screen, int(cfg["MAIN"]["W"]) // 3, 3)

### Show In Public List Checkbox
publicListCb = Checkbox(screen, style, 0, 0, "SHOW IN PUBLIC LIST")
elementG.append(publicListCb)

### Private Game Checkbox
privateGameCb = Checkbox(screen, style, 0, 0, "PRIVATE GAME")
privateGameCb.change = privateGameCb_Change
elementG.append(privateGameCb)

### Password Textbox
passwordTb = Textbox(screen, style, 0, 0, "Password", False, 16, Input.numbers)
elementG.append(passwordTb)

### Create Button
createB = Button(screen, style, 0, 0, "[ CREATE ]")
createB.click = createB_click
elementG.append(createB)

### Back Button
backB = Button(screen, style, 0, 0, "[ BACK ]")
backB.click = backB_click
elementG.append(backB)

### List Sorting
elementG.sort()

# Scene -----------------------------------------
class Create:
    """Сцена создания игры"""
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