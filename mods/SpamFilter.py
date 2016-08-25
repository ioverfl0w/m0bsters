import time

class SpamFilter:
	
	def __init__(self, bot, eng):
		self.engine = eng
		self.specific = bot
		self.outspoken = []
		self.rule = [4, 2]
		self.length = 2
		self.ignore = []
		
	def unignore(self, nick):
		nick = nick.lower()
		for n in self.ignore:
			if n[0].lower() == nick:
				return self.ignore.remove(n)
		
	def add_ignore(self, nick):
		self.ignore.append([nick, time.time()])
		self.clear_nick(nick)
		
	def is_ignored(self, nick):
		nick = nick.lower()
		for n in self.ignore:
			if n[0].lower() == nick:
				return True
		return False
		
	def ignore_expired(self, nick):
		nick = nick.lower()
		for n in self.ignore:
			if n[0].lower() == nick and (n[1] + (self.length * 60)) < time.time():
				return True
		return False
		
	def append(self, nick):
		self.outspoken.append([nick, time.time()])
		return self.check(nick)
		
	def clear_nick(self, nick):
		for usr in self.outspoken:
			if usr[0].lower() == nick:
				self.outspoken.remove(usr)
				
	def check_times(self, nick):
		chk = self.get_usr(nick)
		return chk[len(chk) - 2][1] + self.rule[1] >= chk[len(chk) - 1][1]
				
	def get_usr(self, nick):
		chk = []
		for usr in self.outspoken:
			if usr[0].lower() == nick:
				chk.append(usr)
		return chk
		
	def check(self, nick):
		nick = nick.lower()
		chk = self.get_usr(nick)
		if len(chk) < self.rule[0] and not self.check_times(nick):
			return self.clear_nick(nick)
		#check count
		if len(chk) >= self.rule[0]:
			if (chk[0][1] + self.rule[1]) >= chk[self.rule[0] - 1][1]:
				self.add_ignore(nick) #spamming cunt
				return True
			self.clear_nick(nick)
		return False

	def message(self, bot, who, location, message, args):
		if self.is_ignored(who[0]) and not self.ignore_expired(who[0]):
			return "IGNORE" # requires edit in Event !!
		
		if not self.engine.get_access().get_user_rights(who, bot) > 0:
			if self.append(who[0]):
				bot.notice(who[0], "Notice - you have been ignored for spamming! Ignore will expire in " + str(self.length) + " minutes.")
			
			#bot.notice(who[0], "debug -- blocked:" + ("yes" if self.is_ignored(who[0]) else "no") + " -- ")
			
			if self.is_ignored(who[0]) and self.ignore_expired(who[0]):
				self.unignore(who[0])
				bot.notice(who[0], "You have been unignored. Don't spam to prevent this in the future.")
				
