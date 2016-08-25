import time
import random

class MissionClock:
	
	def __init__(self, don, chan):
		#delay in seconds
		self.delay = 60
		self.start = 0
		self.bot = don
		self.home_chan = chan
		self.toggle = True
		self.enable = True
		
	def strike(self):
		return 1 if (self.start + self.delay) <= time.time() else 0
			
	def clear(self):
		self.start = time.time()
		
	def tog(self):
		self.enable = not self.enable
		return self.enable
		
	def get_mode(self):
		return self.toggle
	
	def perform(self):
		if not self.enable:
			return
		
		if self.toggle:
			self.delay = 60 * 29 #Time (in seconds) the mission bot takes to rejoin game channel
			self.toggle = False
			self.bot.part(self.home_chan)
		else:
			self.delay = 60 #Time (in seconds) the mission bot stays in game channel activated
			self.toggle = True
			self.bot.join(self.home_chan)
