"""
Basic Control Module

Allows for authenticated users to control the bot with basic commands

Simply type '.' in chat or to bot to authenticate for session length
determined in:
	- ./sched/AuthSys.py - delay

"""

import sys
import datetime
sys.path.append("./lib/")
import Utility

class Basic:
	
	def __init__(self, eng):
		self.specific = 0
		self.engine = eng
		self.func = Utility.Misc()

	def message(self, bot, who, location, message, args):
		if args[0] == "." and self.engine.get_access().has_rights(who[0], bot): #identify
			if self.engine.get_access().is_authed(who[0], bot):
				return
			bot.whois(who[0])
			return

		if (self.engine.get_access().get_user_rights(who, bot) < 1): # Trusted Commands and Above (1+)
			return

		if args[0].lower() == "!rights":
			bot.notice(who[0], "rights: " + str(self.engine.get_access().get_user_rights(who, bot)))
			return
			
		if (self.engine.get_access().get_user_rights(who, bot) < 2): # Admin Commands and Above (2+)
			return

		if args[0].lower() == "!access":
			i = 0
			bot.notice(who[0], "Access list")
			bot.notice(who[0], "Num   Lev   " + self.func.space("Nick", 8) + "Network")
			for acc in self.engine.get_access().list:
					bot.notice(who[0], str(i) + "     " + str(acc[2]) + "     " + self.func.space(acc[1], 8) + acc[0])
					i += 1
			return
			
		if args[0].lower() == "!kick":
			if (len(args)) < 2:
				return bot.kick(location, who[0])
			else:
				return bot.kick(location, args[1])
			
		if args[0].lower() == "!auth":
			bot.notice(who[0], "Active Auths")
			bot.notice(who[0], "" + self.func.space("Network", 11) + self.func.space("Nick", 10) + "TimeLeft")
			seslist = self.engine.sched.get_event("authsys").time_left_list()
			for ses in seslist:
				bot.notice(who[0], self.func.space(ses[0], 11) + self.func.space(ses[1], 10) + self.func.timedString(int(ses[2])))
			return

		if (self.engine.get_access().get_user_rights(who, bot) < 3): # Root commands (3+)
			return
			
		if args[0].lower() == "!set":
			if len(args) < 4:
				return bot.notice(who[0], "Syntax: !set [network] [nick] [level]")
			if self.engine.get_network(args[1]) == None:
				return bot.notice(who[0], "Network '" + args[1] + "' not currently configured.")
			try:
				if self.engine.get_access().update_user(args[2], args[1], args[3]):
					return bot.notice(who[0], "Updated access.")
			except ValueError:
				return bot.notice(who[0], "Syntax: level must be an integer.")
				
		if args[0].lower() == "!del":
			if len(args) < 3:
				return bot.notice(who[0], "Syntax: !del [network] [nick]")
			if self.engine.get_network(args[1]) == None:
				return bot.notice(who[0], "Network '" + args[1] + "' not currently configured.")
			if self.engine.get_access().rem_user(args[2], args[1]):
				return bot.notice(who[0], "Updated access.")
			else:
				return bot.notice(who[0], "User not found.")

		if args[0].lower() == "!join" and len(args) > 1:
			bot.join(args[1])
			return

		if args[0].lower() == "!part":
			if len(args) > 1:
				bot.part(args[1])
			else:
				bot.part(location)
			return

		if args[0].lower() == "!reload":
			self.engine.get_access().reload_access()
			bot.message(location, "Access reloaded.")
			return
