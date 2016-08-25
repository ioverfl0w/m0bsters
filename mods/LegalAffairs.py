import sys
import random
import Mobster
sys.path.append("./mods/mobsters")
import User
import Mob

mob_cost = 1000000

class LegalAffairs:
	
	def __init__(self, bot, mobs, regen):
		self.specific = bot # The 'mobsters' bot instance
		self.mobs = mobs
		self.bot_name = bot.nick
		self.regen = regen

	def message(self, bot, who, location, message, args):
		if not location == self.bot_name:
			return
		user = self.mobs.load_user(who[0])
		if self.mobs.identity_check(user, who):
				
			if args[0] == "create":
				if len(args) == 1:
					return bot.notice(user.get_nick(), "Try help create")
					
				if not user.load_mob() == 0:
					return bot.notice(user.get_nick(), "You are already in a mob! Leave that one first, then let's talk.")
					
				if args[len(args) - 1] == "confirm":
					name = message[message.index(args[1]):message.index(args[len(args) - 1]) - 1]
					mob = Mob.Mob(name)
					
					if not mob.get_size() == 0:
						return bot.notice(user.get_nick(), "That name is already registered.")
						
					if user.get_cash() < mob_cost:
						return bot.notice(user.get_nick(), "Insufficient funds. It costs $1M to purchase a Mob License.")
						
					if len(name) < 3:
						return bot.notice(user.get_nick(), "Unacceptable name. Must be more than 3 characters long.")
						
					mob.add_mobster(user.get_nick(), 2)
					user.add_cash(-1 * mob_cost)
					user.edit_mob(name)
					bot.message(self.mobs.host_channel, "[6Mob] 02" + user.get_nick() + " has established the mob 02" + name + ".")
					return bot.notice(user.get_nick(), "Congratulations on the founding of your new mob " + name + "!")
				return bot.notice(user.get_nick(), "To confirm the purchase of a Mob License for $10M, finish your statement with the word confirm.")
			
			if args[0] == "accept":
				if not self.regen.exisiting(user.get_nick()):
					return bot.notice(user.get_nick(), "You don't have any standing offers at this moment.")
					
				invite = self.regen.get_invite(user.get_nick())
				mob = self.mobs.load_user(invite[0]).load_mob()
				
				if mob == 0:
					return bot.notice(user.get_nick(), "There was an error loading the mob.")
					
				if mob.add_mobster(user.get_nick(), 0) == 2:
					self.regen.rem_invite(invite[1])
					user.edit_mob(mob.get_name())
					bot.notice(invite[0], user.get_nick() + " has accepted your invitation.")
					bot.message(self.mobs.host_channel, "[6Mob] 02" + user.get_nick() + " has joined 02" + mob.get_name())
					return bot.notice(user.get_nick(), "Welcome to " + mob.get_name() + ", " + user.get_nick())
					
				return bot.notice(user.get_nick(), "There was an error while accepting your invitation.")
				
			if user.get_mob_name() == 0:
				return
				
			if args[0] == "view":
				mob = user.load_mob()
				if not mob.get_access(user.get_nick()) > 0:
					return bot.notice(user.get_nick(), "Insufficient rights.")
				if len(args) == 1:
					mob = user.load_mob()
					return bot.notice(user.get_nick(), "[" + mob.get_name() + "] " + user.get_nick() + " - Rights: " + str(mob.get_access(user.get_nick())))
				view = self.mobs.load_user(args[1])
				if view == 0:
					return bot.notice(user.get_nick(), "User not found.")
				mob = view.load_mob()
				if view.get_mob_name() == 0 or mob.get_user(view.get_nick()) == 0:
					return bot.notice(user.get_nick(), view.get_nick() + " is not in our mob.")
				return bot.notice(user.get_nick(), "[" + mob.get_name() + "] " + view.get_nick() + " - Rights: " + str(mob.get_access(view.get_nick())))
				
			if args[0] == "set":
				mob = user.load_mob()
				if not mob.get_access(user.get_nick()) > 0:
					return bot.notice(user.get_nick(), "Insufficient rights.")
				if len(args) == 1:
					return bot.notice(user.get_nick(), "No user specified.")
				if len(args) < 3:
					return bot.notice(user.get_nick(), "Syntax: /msg " + self.bot_name + " set user rights")
				view = self.mobs.load_user(args[1])
				if view == 0:
					return bot.notice(user.get_nick(), "User not found.")
				try:
					amount = int(args[2])
				except ValueError:
					return bot.notice(user.get_nick(), "Invalid amount.")
				if view.get_mob_name() == 0:
					return bot.notice(user.get_nick(), view.get_nick() + " is not in our mob.")
				mob = view.load_mob()
				if mob.set_access(view.get_nick(), amount) == 2:
					return bot.notice(user.get_nick(), view.get_nick() + " has been adjusted to " + str(amount))
				return bot.notice(user.get_nick(), "Unable to update user rights.")
			
			if args[0] == "kick":
				mob = user.load_mob()
				if not mob.get_access(user.get_nick()) == 2:
					return bot.notice(user.get_nick(), "Insufficient rights.")
				if len(args) == 1:
					return bot.notice(user.get_nick(), "No user specified.")
				vic = self.mobs.load_user(args[1])
				if vic == 0:
					return bot.notice(user.get_nick(), "User not found.")
				if mob.rem_mobster(vic.get_nick()) == 2:
					vic.edit_mob("0")
					bot.message(self.mobs.host_channel, "[6Mob] 02" + vic.get_nick() + " has been kicked from 02" + mob.get_name())
					return bot.notice(user.get_nick(), vic.get_nick() + " has been removed from the mob.")
				return bot.notice(user.get_nick(), vic.get_nick() + " is not in that mob.")
			
			if args[0] == "list":
				mob = user.load_mob()
				return bot.notice(user.get_nick(), "(Size: " + str(mob.get_size()) + ") Members: " + mob.get_list())
				
			if args[0] == "leave":
				if len(args) == 1:
					return bot.notice(user.get_nick(), "To leave your mob, type /msg " + self.bot_name + " leave confirm")
					
				if args[1] == "confirm":
					mob = user.load_mob()
					mob.rem_mobster(user.get_nick())
					user.edit_mob("0")
					bot.message(self.mobs.host_channel, "[6Mob] 02" + user.get_nick() + " has just parted ways with 02" + mob.get_name())
					return bot.notice(user.get_nick(), "You have successfully left the mob " + mob.get_name())
			
			if args[0] == "invite":
				if len(args) == 1:
					return bot.notice(user.get_nick(), "No user specified.")
				
				who = self.mobs.load_user(args[1])
				
				if who == 0:
					return bot.notice(user.get_nick(), "User not found.")
					
				if not who.get_mob_name() == 0:
					return bot.notice(user.get_nick(), who.get_nick() + " is already in a mob.")
					
				mob = user.load_mob()
					
				if mob.check_mob(who.get_nick()):
					return bot.notice(user.get_nick(), who.get_nick() + " is already in your mob.")
					
				if self.regen.add_invite(user.get_nick(), who.get_nick()) == 2:
					bot.notice(who.get_nick(), "3On behalf of 02" + user.get_nick() + "3, you are presented an invitation to join 02" + mob.get_name() + "3. To accept, message me saying accept. This offer expires in two minutes.")
					return bot.notice(user.get_nick(), "Your invitation has been sent.")
					
				return bot.notice(user.get_nick(), "They currently have a standing offer. Wait a minute and try again.")
