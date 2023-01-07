from Core.GUI.Style import Style

class Border:
    """Рамка для окна"""
    
    def __init__(self, screen, style):
        self.screen = screen
        self.style = style
        
    def draw(self):
        self.screen.rect(0, 0, self.screen.w, self.screen.h, self.style["text"] + self.style["background"] + "*")