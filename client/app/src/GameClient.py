class GameClient:
    """Класс структура игры для хранения данных текущего сеанса"""
    def init(gameId=0, secretCode=0, symbol="", step="X"):
        GameClient.secretCode = secretCode
        GameClient.gameId = gameId
        GameClient.symbol = symbol
        GameClient.step = step
        GameClient.plane = [
			["","",""],
			["","",""],
			["","",""]
		]
        GameClient.end = False
        GameClient.winner = ""