from Core.Input import Input
from Core.GUI.Element import Element

class Textbox(Element):
    def __init__(self, screen, style, x, y, text="", enable=True, maxLength=0, alphabet="123457890"):
        super().__init__(screen, style, x, y, text, enable)
        self.value = ""
        self.maxLength = maxLength
        self.selected = False
        self.alphabet = alphabet

    def __str__(self):
        return self.value
        
    def click(self, obj):
        if self.focused:
            self.selected = not(self.selected)
            if self.selected:
                self.select(self)

    def block(self):
        self.focused = False
        self.enable = False
        self.selected = False

    def inputFromEvent(self, event):
        if not(self.selected): return
        if event.type == Input.Types.Keyboard:
            if event.keyboardState == Input.Keyboard.DOWN:
                if event.keyboardCode == Input.Keyboard.Keys.BACKSPACE:
                    self.value = self.value[:-1]

                elif len(self.value) < self.maxLength or self.maxLength == 0:
                    if event.keyboardChar in self.alphabet: # вот это
                        self.value += str(event.keyboardChar) # пофиксить
                        self.change(self)

    def draw(self):
        text = self.text + ": " + self.value
        self.intersectionLen = len(text)

        if self.enable:
            if self.selected:
                self.screen.text(text, self.x, self.y, wordPrefix=self.style["backgroundF"] + self.style["textF"])
            else:
                self.screen.text(text, self.x, self.y, wordPrefix=self.style["background"] + self.style["text"])
        else:
            self.screen.text(text, self.x, self.y, wordPrefix=self.style["disable"] + self.style["text"])