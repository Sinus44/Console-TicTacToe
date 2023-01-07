class Group:
    """Группа GUI элементов, авто позиционнирование элементов в соответсвии с интервалом и координатами группы"""

    def __init__(self, screen, x, y, interval=1):
        self.screen = screen
        self.x = x
        self.y = y
        self.elements = []
        self.interval = interval
        self.selected = {}

    def append(self, element):
        self.elements.append(element)
    
    def eventHandler(self, event):
        for element in self.elements:
            element.intersectionFromEvent(event)

            if hasattr(element, "inputFromEvent"):
                element.inputFromEvent(event)
    
    def click(self):
        for element in self.elements:
            if element.focused:
                element.click(self)
    
    def sort(self):
        for i in range(len(self.elements)):
            element = self.elements[i]
            element.x = self.x
            element.y = self.y + i * (self.interval + 1)

    def draw(self):
        for element in self.elements:
            element.draw()