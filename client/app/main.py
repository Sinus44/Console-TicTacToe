from Core.core import *
from src.properties import *
from src.scenes.scenes import *

# Output configurate
Output.init()
Output.title("Tic Tac Toe")
Output.resize(cfg["MAIN"]["W"], cfg["MAIN"]["H"])
Output.mode(5)

# Imput configurate
Input.init()
Input.mode(
	useHotkey = True,
	mouseEvents = True,
	resizeEvents = True,
	extended = True
)

# Scenes configurate
scenes = {
	"Connect": Connect,
	"Create": Create,
	"Game": Game,
	"Loading": Loading,
	"Menu": Menu,
	"Settings": Settings
}

Scene.addFromDict(scenes)
Scene.set("Menu")

func = lambda: (Input.tick() is None) & (Scene.play() is None)

fpsCounter = cfg["TESTING"]["fpscheck"].upper() == "TRUE"

if fpsCounter:
	while True:
		time = Performance.function(func)[0]
		Logging.log(f"\nFrametime: {time}\nFramerate: {1/time}")
else:
	while True:
		func()

# 0 < Логгинг < 800 (fps)
# 50K < Инпут < 500K (fps)