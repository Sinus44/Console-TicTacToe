# Import ----------------------------------------
from Core.core import *
from src.properties import *
from src.Client import *
from src.GameClient import *

# GUI -------------------------------------------
## Screen
screen = Window(int(cfg["MAIN"]["W"]), int(cfg["MAIN"]["H"]))

## Style
style = Style()
style.importFromConfig(cfg)

## Frame
frame = Frame(screen, style)

## Border
border = Border(screen, style)

## Grid
grid = Grid(screen, 0, 0, screen.w - 1, screen.h - 1, 3, 3, style)

# Cross
cross = Window(grid.cellW, grid.cellH)
cross.fill()
cross.line(0, 0, cross.w - 1, cross.h - 1)
cross.line(cross.w - 1, 0 , 0, cross.h - 1)

# Zero
zero = Window(grid.cellW, grid.cellH)
zero.fill()
centerX = zero.w // 2
centerY = zero.h // 2
rad = min(centerX, centerY)
zero.circle(centerX, centerY, rad)

# Scene
class Game:
    """Сцена самой игры"""
    def play():

        for event in Input.getEvents():
            if event.type == Input.Types.Mouse:
                if event.mouseType == Input.Mouse.CLICK:
                    if event.mouseKey == Input.Mouse.LEFT:
                        coords = grid.intersection(event.mouseX, event.mouseY)
                        request = {
                            "command":"set_symbol",
                            "args": {
                                "game_id": GameClient.gameId,
                                "secret_code": GameClient.secretCode,
                                "x": coords[0],
                                "y": coords[1]
                            }
                        }

                        response = Client.send(request)
                        if response["status"] == "ok":
                            GameClient.plane = response["args"]["plane"]
                            GameClient.step = response["args"]["step"]

        frame.draw()
        border.draw()
        grid.draw()

        for i in range(len(GameClient.plane)):
            for j in range(len(GameClient.plane[i])):
                symbol = GameClient.plane[i][j]
                if symbol == "X":
                    screen.paste(cross, i * grid.cellW + 1, j * grid.cellH + 1)
                
                elif symbol == "0":
                    screen.paste(zero, i * grid.cellW + 1, j * grid.cellH + 1)

        screen.draw()

        request = {
            "command":"await_change",
            "args": {
                "game_id": GameClient.gameId,
                "secret_code": GameClient.secretCode
            }
        }
        
        Output.title("Наш ход")
        if GameClient.step != GameClient.symbol:
            Output.title("Ждём ход соперника")
            
            Input.stop()
            response = Client.send(request)
            if response["status"] == "ok":
                GameClient.plane = response["args"]["plane"]
                GameClient.step = response["args"]["step"]
            Input.start()