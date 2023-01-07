class Frame:
    """Основа кадра и заливка фона"""
    
    def __init__(self, screen, style):
        self.screen = screen
        self.style = style
    
    def draw(self):
        self.screen.fill(self.style["background"] + " ")