from Core.GUI.Element import Element

class Button(Element):
    """GUI - элемент Кнопка"""
    
    def draw(self):
        text = f"[ {self.text} ]"
        self.intersectionLen = len(text)

        if self.enable:
            if self.focused:
                self.screen.text(text, self.x, self.y, wordPrefix=self.style["backgroundF"] + self.style["textF"])
            else:
                self.screen.text(text, self.x, self.y, wordPrefix=self.style["background"] + self.style["text"])
        else:
            self.screen.text(text, self.x, self.y, wordPrefix=self.style["disable"] + self.style["text"])