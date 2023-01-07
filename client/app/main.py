# -----------------------------------------------------------
# (C) 2022 Sinus44, Kostroma, Russia
# Released under MIT LICENSE
# Email sekrets808@gmail.com
# ----------------------------------------------------------

# Imports ---------------------------------------
from Core.core import *
from src.Client import *
from src.properties import *

# Debug Configurate -----------------------
fpsCounter = cfg["DEBUG"]["fpscheck"].upper() == "TRUE"
networkRequest = cfg["DEBUG"]["networkrequest"].upper() == "TRUE"

# Client - Server Configurate -------------------
if networkRequest:
	Client.debugFunc = Logging.log
Client.init(cfg["SERVER"]["ip"], int(cfg["SERVER"]["port"]))
Client.connect()

# Проверка версии на соответсвие (запросы в разных версиях могут отличаться)
request = {
	"command": "check_version",
	"args": {
		"client_version": int(cfg["OTHER"]["version"])
	}
}

response = Client.send(request)

if not(response is None) and response["status"] != "ok":
	Logging.log(f"Bad server version. Update client. Required version: {response['args']['required_version']}")
	Client.close()

# Output Configurate ----------------------------
Output.init()
Output.title("Masya - Tic Tac Toe")
Output.resize(cfg["MAIN"]["W"], cfg["MAIN"]["H"])
Output.mode(5)

# Imput Configurate -----------------------------
Input.init()
Input.mode(
	useHotkey = True,
	mouseEvents = True,
	resizeEvents = True,
	extended = True
)

# Scene import ----------------------------------
from src.scenes.scenes import *

# Scenes configurate ----------------------------
scenes = {
	"Connect": Connect,
	"Create": Create,
	"Game": Game,
	"Waiting": Waiting,
	"Menu": Menu,
	"Settings": Settings
}

Scene.addFromDict(scenes)
Scene.set("Menu")

# Iteration -------------------------------------
func = lambda: (Scene.play() is None) & (Input.tick() is None)


# Loop ------------------------------------------
if fpsCounter:
	while True:
		time = Performance.function(func)[0]
		Logging.log(f"\nFrametime: {time}\nFramerate: {1/time}")
else:
	while True:
		func()