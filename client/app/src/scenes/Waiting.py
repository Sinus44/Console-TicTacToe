# Import ----------------------------------------
from src.properties import *
from Engine import *
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

## List
elementG = Group(screen, int(cfg["MAIN"]["W"]) // 3, 3)

### Status Label
gameIdL = Label(screen, style, 0, 0, "GAME ID: ")
elementG.append(gameIdL)

### Status Label
statusL = Label(screen, style, 0, 0, "waiting 2st player")
elementG.append(statusL)

### List Sorting
elementG.sort()

# Scene -----------------------------------------
class Waiting:
    """Сцена ожидания второго игрока"""

    def play():
        gameIdL.text = f"GAME ID: {GameClient.gameId}"
        frame.draw()
        border.draw()
        elementG.draw()
        screen.draw()

        request = {
            "command": "check_start_game",
            "args": {
                "game_id": GameClient.gameId
            }
        }

        try:
            response = Client.send(request)

            if response["status"] == "ok":
                Scene.set("Game")
        
        except:
            Scene.set("Menu")