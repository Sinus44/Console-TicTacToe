# Import ----------------------------------------
from src.properties import *
from Engine import *

# Screen ----------------------------------------
screen = Window(int(cfg["MAIN"]["W"]), int(cfg["MAIN"]["H"]))

# Import style ----------------------------------
style = Style()
style.importFromConfig(cfg)

# GUI Callback ----------------------------------
## Sound Checkbox
def soundCb_change(obj):
    pass

## Save Button
def saveB_click(obj):
    cfg["USER"]["nickname"] = nicknameTb.value
    cfg["MAIN"]["sound"] = str(soundCb.checked)
    cfg.write()

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

### Nickname Textbox
nicknameTb = Textbox(screen, style, 0, 0, "Nickname", True, 12, Input.angCaps + Input.ang + Input.numbers)
nicknameTb.value = cfg["USER"]["nickname"]
elementG.append(nicknameTb)

### Sound Checkbox
soundCb = Checkbox(screen, style, 0, 0, "Sound", False)
soundCb.checked = cfg["MAIN"]["sound"].upper() == "TRUE"
soundCb.change = soundCb_change
elementG.append(soundCb)

### Resolution Textbox
resolutionTb = Textbox(screen, style, 0, 0, "Resolution", False, 16)
resolutionTb.value = f"{cfg['MAIN']['W']}x{cfg['MAIN']['H']}"
elementG.append(resolutionTb)

### Save Button
saveB = Button(screen, style, 0, 0, "SAVE", True)
saveB.click = saveB_click
elementG.append(saveB)

### Back Button
backB = Button(screen, style, 0, 0, "BACK")
backB.click = backB_click
elementG.append(backB)

### List Sorting
elementG.sort()

# Scene -----------------------------------------
class Settings:
    """Сцена настроек приложения"""
    def play():
        elementG.eventHandler()
        if Input.eventType == Input.Types.Mouse:
            if Input.mouseType == Input.Mouse.DOWN and not Input.prevMouseState:
                if Input.mouseKey == Input.Mouse.LEFT:
                    elementG.click()

        frame.draw()
        border.draw()
        elementG.draw()
        screen.draw()