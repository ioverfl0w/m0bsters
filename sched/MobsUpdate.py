import time
import os
import glob

class MobsUpdate:
	
	def __init__(self, don, mobs, ops):
		#delay in seconds
		self.ops = "#nova"
		self.delay = 60 * 50
		self.bot = don
		self.start = 0
		self.mobs = mobs
		mobs.update_timer(self)
		self.hard_update_active_players()
		
	def perform(self):
		active = []
		#generate everyone's income
		for u in glob.glob("./data/mobster/users/*"):
			user = self.mobs.load_user(os.path.basename(u)[:os.path.basename(u).index(".u")])
			
			if not user.get_host() == "banned" and not user.is_inactive():
				user.add_cash(user.get_income(self.mobs.prop_list) - user.get_upkeep(self.mobs.item_list))
				active.append(user)
		#self.bot.message(self.ops, "payday completed! user count: " + str(total) + "; users paid: " + str(comp))
		self.mobs.engine.log.write("Payday completed (users paid: " + str(len(active)) + ")")
		
	def hard_update_active_players(self):
		#self.mobs.engine.log.write("Hard update of active players")
		active = []
		for u in glob.glob("./data/mobster/users/*"):
			user = self.mobs.load_user(os.path.basename(u)[:os.path.basename(u).index(".u")])
			
			if not user.get_host() == "banned" and not user.is_inactive():
				active.append(user)
		self.update_active_players(active)
		
	def update_active_players(self, active):
		f = open("./data/mobster/data/active_list.l", 'w')
		for u in active:
			f.write(u.get_nick() + "\t" + str(u.get_level()) + "\n")
		f.close()
		
	def strike(self):
		return 1 if (self.start + self.delay) <= time.time() else 0
		
	def clear(self):
		self.start = time.time()
		
	def get_time_left(self):
		return int((self.start + self.delay) - time.time())
