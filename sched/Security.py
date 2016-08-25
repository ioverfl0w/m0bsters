import time

class Security:
	
	def __init__(self, bot, ajoin):
		#delay in seconds
		self.host_chan = ajoin[0]
		self.ops = ajoin[1]
		self.delay = 120
		self.start = 0
		self.bot = bot
		self.locked = False
		
	def strike(self):
		return 1 if (self.start + self.delay) <= time.time() else 0
			
	def clear(self):
		self.start = time.time()
	
	def lockdown(self, buff):
		self.locked = True
		self.clear()
		self.bot.message(self.ops, "notice: channel lockdown in effect. culprits: " + buff.get_culprits())
		
	def is_locked(self):
		return self.locked
	
	def perform(self):
		if not self.locked:
			return
			
		self.locked = False
		self.bot.message(self.host_chan, "02Notice - the channel lockdown has been lifted. Please refrain from spamming to avoid this in the future.")
		self.bot.message(self.ops, "notice: channel lockdown lifted.")
