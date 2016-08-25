import sys
import random
import Mobster
sys.path.append("./mods/mobsters")
import User

class Missions:
	
	def __init__(self, bot, mobs, schd):
		self.specific = bot
		self.bot_name = bot.nick
		self.mobs = mobs
		self.clock = schd
		self.missions = []
		
	def new_mission(self, user):
		mission = [user, self.get_random_item(user), random.randint(10, 25*user.get_level())]
		self.missions.append(mission)
		return mission
		
	def get_random_item(self, user):
		t = random.randint(0, self.mobs.item_list.get_item_count() - 1)
		if self.mobs.item_list.get_level(t) <= user.get_level():
			return t
		return self.get_random_item(user)
		
	def get_mission(self, user):
		for m in self.missions:
			if m[0].get_who() == user.get_who():
				return m
		return []

	def message(self, bot, who, location, message, args):
		if args[0] == "!don" and bot.get_access().get_user_rights(who) >= 2:
			return bot.notice(who[0], self.bot_name + " has been " + ("enabled" if self.clock.tog() else "disabled"))
			
		if not location == self.bot_name:
			return
			
		user = self.mobs.load_user(who[0])
		if self.mobs.identity_check(user, who) and self.clock.get_mode():
			mission = self.get_mission(user)
			
			if args[0] == "godfather":
				if len(mission) == 0:
					mission = self.new_mission(user)
					return bot.message(user.get_nick(), "I see you are looking for work... Bring me " + str(mission[2]) + " " + self.mobs.item_list.get_label(mission[1]) + "s and I will see what I can do.")
				
				uitems = user.load_items()
				
				if uitems.get_value(mission[1]) >= mission[2]:
					return bot.message(user.get_nick(), "You have what I am looking for. Would you like to complete our arrangement?")
				
			#only mission-engaged users can use these
			if len(mission) == 0:
				return
				
			if args[0] == "help":
				return bot.message(user.get_nick(), "Your current mission is to bring me " + str(mission[2]) + " " + self.mobs.item_list.get_label(mission[1]) + "s.")
			
			if args[0] == "yes":
				uitems = user.load_items()
				if uitems.get_value(mission[1]) >= mission[2]:
					self.missions.remove(mission)
					uitems.del_item(mission[1], mission[2])
					cash = int(round((uitems.get_value(mission[1]) * mission[2])) * 1.5)
					xp = int((self.mobs.item_list.get_level(mission[1]) * mission[2]))
					user.add_cash(cash, 1)
					if user.add_xp(xp) == 1: #level up
						self.mobs.game.combat.levelup(bot, user)
					return bot.message(user.get_nick(), "Your services have not gone unnoticed - I have given you " + str(xp) + " experience points and $" + str(cash) + ".")
