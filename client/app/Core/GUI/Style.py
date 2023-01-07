from Core.core import Color

class Style(dict):
    """Стиль - настройки цветов и прочего для GUI элементов"""
    def __init__(self):
        super().__init__({
			"text": Color.BLACK,
			"textF": Color.WHITE,

			"background": Color.Background.WHITE,
			"backgroundF": Color.Background.BLACK,

            "disable": Color.Background.BLACK 
		})

    def importFromConfig(self, cfg):
        for param in ["text", "textF"]:
            rgb = cfg["STYLE"][param].split(" ")
            self[param] = Color.rgb(rgb[0], rgb[1], rgb[2])

        for param in ["background", "backgroundF", "disable"]:
            rgb = cfg["STYLE"][param].split(" ")
            self[param] = Color.Background.rgb(rgb[0], rgb[1], rgb[2])
