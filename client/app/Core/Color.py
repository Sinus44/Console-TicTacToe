class Color:
	BLACK	 = '\33[30m'
	RED	     = '\33[31m'
	GREEN	 = '\33[32m'
	YELLOW   = '\33[33m'
	BLUE	 = '\33[34m'
	PURPLE   = '\33[35m'
	SKY	     = '\33[36m'
	SNOW	 = '\33[37m'
	GREY	 = '\33[90m'
	PINK	 = '\33[91m'
	LIME	 = '\33[92m'
	BANANA   = '\33[93m'
	AZURE	 = '\33[94m'
	VIOLET   = '\33[95m'
	AQUA	 = '\33[96m'
	WHITE	 = '\33[97m'

	class Background:
		BLACK  = '\33[40m'
		RED	   = '\33[41m'
		GREEN  = '\33[42m'
		YELLOW = '\33[43m'
		BLUE   = '\33[44m'
		PURPLE = '\33[45m'
		SKY	   = '\33[46m'
		SNOW   = '\33[47m'
		GREY   = '\33[100m'
		PINK   = '\33[101m'
		LIME   = '\33[102m'
		BANANA = '\33[103m'
		AZURE  = '\33[104m'
		VIOLET = '\33[105m'
		AQUA   = '\33[106m'
		WHITE  = '\33[107m'

		def rgb(r, g, b):
			return f"\33[48;2;{r};{g};{b}m"

	default = "\33[0m"
	underline = "\33[4m"
	negative = "\33[7"

	def rgb(r, g, b):
		return f"\33[38;2;{r};{g};{b}m"