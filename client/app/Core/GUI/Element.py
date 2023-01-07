from Core.Input import Input
from Core.GUI.Events import Events

class Element(Events):
    """Мульти класс для большенства GUI элементов"""
    
    def __init__(self, screen, style, x=0, y=0, text="", enable=True, visible=True):
        self.screen = screen
        self.style = style
        self.x = x
        self.y = y
        self.text = text
        self.focused = False
        self.intersectionLen = len(text)
        self.enable = enable
        self.visible = visible

    def block(self):
        self.focused = False
        self.enable = False

    def intersectionFromEvent(self, event):
        if self.enable:
            if event.type == Input.Types.Mouse:
                if event.mouseType == Input.Mouse.MOVE:
                    self.intersection(event.mouseX, event.mouseY)

    def intersection(self, x, y):
        if self.enable:
            if (self.x <= x < self.x + self.intersectionLen) and (self.y == y):
                self.focused = True
                self.focus(self)
            else:
                self.focused = False
