class Config(dict):
	config = None

	def __init__(self, path, autosave=False):
		super().__init__()
		self.path = path
		self.autosave = autosave

	def setSection(self, key, value):
		if value == "":
			self.pop(key)
		else:
			self[key] = value

		if self.autosave: self.write()

	def setParam(self, section, key, value):
		if value == "":
			self[section].pop(key)
		else:
			self[section][key] = value

		if self.autosave: self.write()

	def read(self):
		file = open(self.path, "r")
		string = file.read()

		strings = string.split("\n")
		
		for s in strings:
			if not(len(s)):
				continue

			if s[0] == "[":
				section = str(s[1:-1])
				self[section] = {}
				lastSection = section

			elif s[0] == ";" or s[0] == "#":
				continue
			
			else:
				data = s.split(" = ")

				for i in range(2, len(data)):
					data[1] += " = " + data[i]

				self[lastSection][data[0]] = data[1]

	def write(self):
		file = open(self.path, "w")
		out = ";AUTO GENERATED DONT CHANGE IF NOT SHARISH"

		for section in self:
			out += f"\n[{section}]"

			for prop in self[section]:
				out += f"\n{prop} = {self[section][prop]}"
			out += "\n"

		file.write(out)
		file.close()


#cfg = Config("./config.ini", autosave=True) # Init
#cfg.read() # REad
#print(cfg["key"])
#cfg.set("f",{"Ahaha":"Kэк"}) # Set
#cfg.set("f", "") # delete
#cfg.write() # Write