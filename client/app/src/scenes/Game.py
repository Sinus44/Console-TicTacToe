# Import ----------------------------------------
from Core.core import *
from src.properties import *

# Screen ----------------------------------------
screen = Window(int(cfg["MAIN"]["W"]), int(cfg["MAIN"]["H"]))

# Import style ----------------------------------
style = Style()
style.importFromConfig(cfg)

# GUI -------------------------------------------
## Grid
grid = Grid(screen, 0, 0, screen.w - 1, screen.h - 1, 3, 3, style)

# Scene
class Game:
    """Сцена самой игры"""
    def play():
        for event in Input.getEvents():
            if event.type == Input.Types.Mouse:
                if event.mouseType == Input.Mouse.CLICK:
                    if event.mouseKey == Input.Mouse.LEFT:
                        #Logging.log(str(event))
                        coords = grid.intersection(event.mouseX, event.mouseY)
                        Engine.title(str(f"{coords[0]} {coords[1]}"))

        screen.fill()
        screen.paste(gridScreen)
        screen.draw()