class Mmath:
	def round(x):
		return int((x // 1) if x % 1 < 0.5 else ((x // 1) + 1))
	
	def clamp(x, minValue=0, maxValue=1):
		return max(min(x, maxValue), minValue)