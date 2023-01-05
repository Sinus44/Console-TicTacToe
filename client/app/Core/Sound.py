import wave
import pyaudio
import threading

class Sound:
	def __init__(self, filePath):
		self.filePath = filePath
		self.chunksize = 1024
		self.volume = 1
		self.off = False
		
		self.portaudio = pyaudio.PyAudio()
		self.thread = threading.Thread(target=self.p)  

		wavefile = wave.open( self.filePath, 'r' )

		self.format = self.portaudio.get_format_from_width(wavefile.getsampwidth())
		self.channels = wavefile.getnchannels()
		self.defaultRate = wavefile.getframerate()
		self.rate = self.defaultRate

	def p(self):
		wavefile = wave.open( self.filePath, 'r' )

		self.streamobject = self.portaudio.open(format=self.format, channels=self.channels, rate=self.rate, output=True ) 
		self.data = wavefile.readframes(self.chunksize)

		while len(self.data) > 0 and not self.off:
			if self.off: return
			self.streamobject.write(self.data)
			self.data = wavefile.readframes(self.chunksize)

	def speed(self,speed):
		self.rate = int(self.defaultRate * speed)

	def play(self):
		self.off = False
		if not self.thread.is_alive():
			self.thread = threading.Thread(target=self.p)
			self.thread.start()

	def volume(volume):
		self.volume = volume

	def stop(self):
		self.off = True
