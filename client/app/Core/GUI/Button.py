from Core.GUI.Element import Element

class Button(Element):
	def draw(self):
		if self.focused:
			self.screen.text(self.text, self.x, self.y, wordPrefix = self.style["backgroundF"] + self.style["textF"])
		else:
			self.screen.text(self.text, self.x, self.y, wordPrefix = self.style["background"] + self.style["text"])