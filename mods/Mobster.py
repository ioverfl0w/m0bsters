import sys
import locale
import os
import glob
import time
sys.path.append("./mods/mobsters")
import User
import PropertyList
import ItemList
import MobstersGame
import Bank
import Hit
import MessageBuffer

class Mobster:

	# host - the game channel
	# sec - the 
	def __init__(self, eng, mobs, host, sec):
		self.engine = eng
		self.specific = mobs
		self.dir = "./data/mobster/"
		self.bot_name = mobs.nick
		self.host_channel = host
		self.prop_list = PropertyList.PropertyList(self.import_file(self.dir + "data/property_list.l"))
		self.item_list = ItemList.ItemList(self.import_file(self.dir + "data/item_list.l"))
		self.game = MobstersGame.MobstersGame(self)
		self.timer = 0
		self.security = sec
		self.public_toggle = False
		self.mobCredLevelUp = 3 # Points granted per level up
		self.msgb = MessageBuffer.MessageBuffer()
		#easy number reading
		locale.setlocale(locale.LC_ALL, "")
		
	def get_security(self):
		return self.security
		
	def update_timer(self, timer):
		if self.timer == 0:
			self.timer = timer
		
	def import_file(self, file_dir):
		return [line.strip() for line in open(file_dir)]
		
	def load_user(self, nick):
		try:
			x = self.import_file(self.dir + "users/" + nick.lower() + ".u")
			if len(x) == 0:
				return 0
			return User.User(x)
		except EnvironmentError:
			return 0
			
	def get_hitlist(self):
		s = ""
		for u in glob.glob(self.dir + "hitlist/*"):
			nick = os.path.basename(u)[:os.path.basename(u).index(".h")]
			hit = Hit.Hit(nick)
			s += nick + " (03$" + str(hit.get_bounty()) + "), "
		return s
			
	def load_bank(self, user):
		return Bank.Bank(user)
		
	def identity_check(self, user, who):
		if user == 0:
			return False
		return user.get_who().lower() == (who[0] + "@" + who[2]).lower()
			
	def new_user(self, user):
		user.update()
		
	def message(self, bot, who, location, message, args):
		#perform game checks (pm option)
		if location == self.bot_name:
			user = self.load_user(who[0])
			if not user == 0 and user.get_host() == "banned":
				return #banned....
			
			if args[0] == "recover" and not user == 0 and not self.identity_check(user, who):
				if len(args) == 1:
					return bot.notice(who[0], "Syntax: /msg " + self.bot_name + " recover recovery_key")
				if args[1] == user.get_recovery_key():
					user.edit_host(who[2])
					return bot.notice(who[0], "Your host has been changed to " + who[2] + ".")
				return bot.notice(who[0], "Recovery keys did not match.")
			
			if args[0] == "register" and user == 0:
				if who[0].startswith("mobster_"):
					return bot.notice(who[0], "Please change your nick! Use /nick your_name.")
				if len(args) == 2:
					return bot.notice(who[0], "To complete registration, append \"confirm\" to the end of the command.")
				if len(args) > 2 and args[2] == "confirm":
					bot.mode(location + " +v " + who[0])
					self.new_user(User.User([who[0] + "@" + who[2], str(args[1]), 10000, 1, 0, 100, 10, 0, 0, 0, time.time(), 0, 100, 10, 3])) #New Account
					bot.notice(who[0], "You have now registered to play Mobsters. You are " + who[0] + "@" + who[2] + ", and you will need to use this host to play on this nick. To start, /msg " + self.bot_name + " help")
					bot.notice(who[0], "Note -- your recovery key is " + args[1] + ". Please remember this, as it will allow you to change your host should it be necessary.")
					return bot.message(self.host_channel, "[8Arrival] Watch out, new Mobster 02" + who[0] + " has joined the game.")
				else:
					bot.notice(who[0], "Syntax: /msg " + self.bot_name + " register recovery_key")
					return bot.notice(who[0], "Your recovery_key is used in the case you need to recover your account when you may have changed hosts.")
			
			if self.identity_check(user, who):
				return self.game.command(bot, user, message, args)
			
		if location == self.host_channel and not self.security.is_locked():
			user = self.load_user(who[0])
			if not user == 0 and user.get_host() == "banned":
				return #banned....
				
			#noobs
			if (args[0] == "!help" or args[0] == "!reg" or args[0] == "help") and user == 0:
				bot.notice(who[0], "If you have an account but cannot get your host to match up, use /msg " + self.bot_name + " recover your_recovery_key . This is the key you set when you first created your account.")
				return bot.notice(who[0], "To register a mobsters account, type /msg " + self.bot_name + " register. You can't play without an account :-)")
				
			if user == 0:
				return #no account
			
			#check for channel spam
			self.msgb.add(user)
			if self.msgb.check() == 2: #FLOOD
				self.security.lockdown(self.msgb)
				return bot.message(self.host_channel, "02Notice - the channel has been locked down for 2 minutes due to flooding. You can continue playing by using /msg " + self.bot_name + " action")
				
			#trusted commands (admin)
			if args[0] == "!cmd" and self.engine.get_access().get_user_rights(who, bot) >= 2:
				return bot.notice(who[0], "!uhost !ban !tog !view !seen")
			
			if args[0] == "!uhost" and self.engine.get_access().get_user_rights(who, bot) >= 2:
				if len(args) > 2:
					u = self.load_user(args[1])
					if u == 0:
						return bot.notice(who[0], "Unable to access user file.")
					u.edit_host(args[2])
					return bot.message(self.host_channel, "Notice: host for '" + args[1] + "' changed to " + args[1] + "@" + args[2])
				else:
					return bot.notice(who[0], "Syntax: !uhost nick new_host")
					
			if args[0] == "!ban" and self.engine.get_access().get_user_rights(who, bot) >= 2:
				if len(args) > 1:
					u = self.load_user(args[1])
					if u == 0:
						return bot.notice(who[0], "User does not exist")
					bot.kick(location, args[1])
					bot.mode(location + " +b " + args[1] + "!*@" + u.get_host())
					u.edit_host("banned")
					return bot.message(location, "User has been banned.")
				else:
					return bot.notice(who[0], "Syntax: !ban [user]")
					
			if args[0] == "!tog" and self.engine.get_access().get_user_rights(who, bot) >= 2:
				self.public_toggle = not self.public_toggle
				return bot.message(self.host_channel, "Public-mode for general commands has been " + ("disabled" if self.public_toggle else "enabled") + ".")
			
			if args[0] == "!view" and self.engine.get_access().get_user_rights(who, bot) >= 1:
				if len(args) > 1:
					u = self.load_user(args[1])
					if u == 0:
						return bot.notice(who[0], "User not found.")
					m = u.load_mob()
					return bot.notice(who[0], "Info for " + u.get_who() + " - [lvl:" + str(u.get_level()) + ";cash:" + str(u.get_cash()) + ";income:" + str(u.get_income(self.prop_list)) + ";upkeep:" + str(u.get_upkeep(self.item_list)) + ";health:" + str(u.get_health()) + ";stamina:" + str(u.get_stamina()) + ";att_bonus:" + str(u.load_items().get_attack_bonus(self.item_list, m)) + ";def_bonus:" + str(u.load_items().get_defence_bonus(self.item_list, m)) + ";mob:" + str(u.get_mob_name()) + "]")
				else:
					return bot.notice(who[0], "Syntax: !view nick")
			
			#only registered users beyond this
			if not self.identity_check(user, who):
				return
			
			if args[0] == "!time":
				user.set_active()
				return bot.message(self.host_channel, "3Time to Payday 1- " + str(self.timer.get_time_left() / 60) + " minutes")
				
			if args[0] == "!stats":
				user.set_active()
				prop = user.load_properties()
				item = user.load_items()
				netw = self.get_netw(user)
				kdr = 0
				try:
					kc = user.get_kill_count()
					dc = user.get_death_count()
					kdr = round(float(kc) / float(dc), 2) if dc > 0 else kc if kc > 0 else dc * -1
				except Exception:
					pass
				return bot.message(self.host_channel, "(" + user.get_who() + ") 02Level: 03" + str(user.get_level()) + "02 - Mob: 03" + str("none" if user.get_mob_name() == 0 else user.get_mob_name()) + "02 - Cash: 03$" + str(user.get_cash()) + "02 - Payroll: 03$" + str(netw) + "02 - Kills: 03" + str(user.get_kill_count()) + "02 - Deaths: 03" + str(user.get_death_count()) + "02 - KDR: 03" + str(kdr) + "02 - Hits: 03" + str(user.get_hit_count()))
			
			if args[0] == "!seen":
				if len(args) > 1:
					u = self.load_user(args[1])
					if u == 0:
						return bot.notice(who[0], "User not found.")
					return bot.message(location, u.get_nick() + " was last seen: " + str(int(time.time() - u.get_last_active()) / 60) + " minutes ago.")
				else:
					return bot.notice(who[0], "Syntax: !seen nick")
			if not self.identity_check(user, who):
				return
				
			#perform game checks
			if not self.public_toggle:
				self.game.command(bot, user, message, args)
				
	def get_netw(self, user):
		return user.load_properties().get_total_income(self.prop_list) - user.load_items().get_total_expense(self.item_list)

	def join(self, bot, who, location):
		if location == self.host_channel:
			user = self.load_user(who[0])
			bot.notice(who[0], "3Welcome to " + self.host_channel + " - the official channel for Mobsters on Rizon!")
			if self.public_toggle: #if public mode is disabled, let people know
			    bot.notice(who[0], "3Notice: public mode is currently disabled, meaning all game commands will need to me Direct messaged to " + self.bot_name)
			    
			if user == 0:
				return bot.notice(who[0], "3Your nick currently isn't registered. Make sure you're identified (your host is your key) and register to play!")
			if not self.identity_check(user, who):
				return bot.notice(who[0], "4Notice: you are currently using a nick that is already registered. If this is your nick, change to your Mobster host to play and rejoin. Otherwise, it is suggested you change your nick.")
			if user.get_host() == "banned":
				bot.message(who[0], "You have been banned from Mobsters. You can appeal this by joining #nova")
				bot.mode(location + " +b " + who[0] + "!*@" + who[2])
				return bot.kick(location, who[0]) # user is banned!
			
			bot.mode(location + " +v " + who[0])
			return bot.notice(who[0], "You have successfully been identified.")
