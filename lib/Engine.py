import time
import traceback
import IrcBot

#
# Note - this file has been edited for mobster use
#

class Engine:

	def __init__(self, event, botinfo, sched, log):
		self.event = event
		self.binfo = botinfo
		self.sched = sched
		self.offline = []
		self.bots = []
		self.log = log
		self.log.write("Engine created")

	def shutdown(self, bot, immediate=False):
		index = self.index(bot)
		if index >= 0:
			bot.close()
			self.offline.append(index)
			self.bots.remove(bot)
			self.log.write("Shutdown of " + bot.network.name + " complete (id-" + str(index) + ")")
			if immediate:
				self.check()
				
	def soft_start(self):
		self.log.write("Initiating soft start...")
		self.create_bots()

	def boot(self):
		#self.log.write("Starting system...")
		#self.create_bots()
		self.event.reload_mods()
		self.sched.reload_mods()
		self.log.write("Loaded " + str(len(self.event.mods)) + " Modules")
		self.log.write("Loaded " + str(len(self.sched.evt)) + " Schedules")
		self.log.write("Engine boot complete")

	def create_bots(self):
		c = 0
		for i in self.binfo:
			self.bots.append(self.connect(i))
			c += 1
			self.log.write("Connected " + str(c) + " of " + str(len(self.binfo)))

	def check(self):
		if len(self.offline) > 0:
			retainer = []
			for i in self.offline:
				self.log.write("Restarting bot #" + str(i))
				try:
					self.bots.insert(i, self.connect(self.binfo[i]))
					self.log.write("Reconnected " + self.binfo[i][1].nick + "@" + self.binfo[i][0].name + " id-" + str(i))
				except:
					self.log.write("Error reconnecting " + self.binfo[i][1].nick + "@" + self.binfo[i][0].name)
					retainer.append(i)
			self.offline = retainer

	def connect(self, index):
		bot = IrcBot.IrcBot(self, index[0])
		bot.connect(index[1])
		return bot

	def get_bots(self):
		return self.bots
		
	def get_network(self, name):
		result = []
		name = name.lower()
		for bot in self.get_bots():
			if bot.network.name.lower() == name:
				result.append(bot)
		return result if len(result) > 0 else None

	def execute(self):
		self.boot()

		while True:
			self.sched.check()
			for a in self.get_bots():
				self.event.process(a, a.read())
			time.sleep(0.02) #prevents cpu 100
		
	def index(self, bot):
		for i in range(len(self.binfo)):
			if self.binfo[i][0] == bot.network:
				return i
		return -1
		
	def get_access(self):
		return self.event.access
