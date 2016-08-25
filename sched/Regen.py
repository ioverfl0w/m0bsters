import time
import glob
import os

#
# used to increase things at an interval of two minutes.
# ie - health (every 4 mins), stamina
# also manages Mob invites (expire after 2 minutes)
#

class Regen:
	
	def __init__(self, mobs, bot):
		#delay in seconds
		self.bot = bot # used for broadcasting messages
		self.delay = 120
		self.start = 0
		self.tick = 0
		self.mobs = mobs
		self.mob_invites = []
		
	def strike(self):
		return 1 if (self.start + self.delay) <= time.time() else 0
			
	def clear(self):
		self.start = time.time()
		
	def exisiting(self, target):
		for invite in self.mob_invites:
			if invite[1].lower() == target.lower():
				return True
		return False
		
	def get_invite(self, target):
		for invite in self.mob_invites:
			if invite[1].lower() == target.lower():
				return invite
		return []
		
	def add_invite(self, sender, target):
		if self.exisiting(target):
			return 1
		self.mob_invites.append([sender, target, time.time() + 60])
		return 2
		
	def rem_invite(self, target):
		if not self.exisiting(target):
			return 1
		self.mob_invites.remove(self.get_invite(target))
		return 2
		
	def perform(self):
		for u in glob.glob(self.mobs.dir + "users/*"):
			user = self.mobs.load_user(os.path.basename(u)[:os.path.basename(u).index(".u")])
			
			if self.tick == 1 and user.get_health() < user.get_maxhealth():
				user.add_health(5)
				
			if user.get_stamina() < user.get_maxstamina():
				user.add_stamina(1)
		
		if self.tick == 1:
			self.tick = 0
		else:
			self.tick = 1
			
		#update the active chart (used for targeting)
		self.mobs.timer.hard_update_active_players()
			
		#check invites
		for invite in self.mob_invites:
			if time.time() >= float(invite[2]):
				self.mob_invites.remove(invite)
				
		#advertise hits
		#hl = self.mobs.get_hitlist()
		#if not hl == "" and self.tick == 0: # every 4 minutes
		#	return self.bot.message(self.mobs.host_channel, "[6Advertisement] There are bounties still active!! " + hl)
		
