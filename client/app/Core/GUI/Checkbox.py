from Core.GUI.Element import Element

class Checkbox(Element):
    """GUI - элемент чек бокс"""
    
    def __init__(self, screen, style, x=0, y=0, text="", enable=True, checked=False):
        super().__init__(screen, style, x, y, text, enable)
        self.checked = checked

    def __bool__(self):
        return self.checked

    def click(self, obj):
        self.checked = not(self.checked)
        self.change(self)

    def draw(self):
        text = ("[X] " if self.checked else "[ ] ") + self.text
        self.intersectionLen = len(text)

        if self.enable:
            if self.focused:
                self.screen.text(text, self.x, self.y, wordPrefix=self.style["backgroundF"] + self.style["textF"])
            else:
                self.screen.text(text, self.x, self.y, wordPrefix=self.style["background"] + self.style["text"])
        else:
            self.screen.text(text, self.x, self.y, wordPrefix=self.style["disable"] + self.style["text"])