import locale
import Combat
import Hit

class MobstersGame:
	
	def __init__(self, mobster):
		self.mobs = mobster
		self.props = self.mobs.prop_list
		self.items = self.mobs.item_list
		self.combat = Combat.Combat(self.mobs)
		
		#variables
		self.min_hit = 5000
		
	def sell_item(self, user, item_id, amount):
		if user.load_items().get_value(item_id) >= amount:
			return user.sell_item(self.items, item_id, amount)
		return 1
		
	def purchase_item(self, user, item_id, amount):
		if user.get_level() >= self.items.get_level(item_id) and user.get_cash() >= (self.items.get_price(item_id) * amount):
			return user.purchase_item(self.items, item_id, amount)
		return 1
			
	def purchase_property(self, user, prop_id, amount):
		if user.get_level() >= self.props.get_level(prop_id) and user.get_cash() >= (self.props.get_price(prop_id, user) * amount):
			return user.purchase_property(self.props, prop_id, amount)
		return 1
		
	def get_fancy_target_list(self, me, level):
		active = self.mobs.import_file(self.mobs.dir + "data/active_list.l")
		targets = ""
		for a in active:
			x = a.split('\t')
			if x[0].lower() == me.lower():
				continue
			if (int(x[1]) <= level + self.combat.attack_range) and (int(x[1]) >= level - self.combat.attack_range):
				targets += "02" + x[0] + " (0" + ("4" if int(x[1]) > level else "3") + "lv" + x[1] + "), "
		return targets
		
	def clean_amount(self, amount):
		return int(amount.replace("k", "000").replace("m", "000000").replace("b", "000000000"))
		
	def command(self, bot, user, message, args):
		#help topics
		if args[0] == "h2p":
			for l in self.mobs.import_file(self.mobs.dir + "text/how-to-play"):
				bot.notice(user.get_nick(), l)
			return
		if args[0] == "help":
			if len(args) == 1:
				for l in self.mobs.import_file(self.mobs.dir + "text/commands"):
					bot.notice(user.get_nick(), l)
				return
			else:
				try:
					for l in self.mobs.import_file(self.mobs.dir + "text/help/" + args[1].lower()):
						bot.notice(user.get_nick(), l)
				except Exception:
					bot.notice(user.get_nick(), "Help topic not found")
			return
			
		#hud
		if args[0] == "hud":
			prop = user.load_properties()
			item = user.load_items()
			mob = user.load_mob()
			bot.notice(user.get_nick(), "[HUD] 2Health: 03" + str(user.get_health()) + "/" + str(user.get_maxhealth()) + " 1- 2Lvl: 03" + str(user.get_level()) + " 1- 2XP: 03" + str(user.get_xp()) + "1/03" + str(user.next_level()) + " 1- " +
										"2Cash: 3$" + str(user.get_cash()) + " 1- 2Income: 3+$" + str(prop.get_total_income(self.props)) + "/hr 1- 2Upkeep: 4-$" + str(user.get_upkeep(self.items)) + "/hr 1- " +
										"2Stamina: 03" + str(user.get_stamina()) + "/" + str(user.get_maxstamina()) + " 1- 2Attack Bonus: 03" + str(item.get_attack_bonus(self.items, mob)) + " 1- 2Defence Bonus: 03" + str(item.get_defence_bonus(self.items, mob)) +
										" 1- 02MobCred: 03" + str(user.get_mobcred()))
			user.set_active()
			return
			
		#Targeting List
		if args[0] == "targets" or args[0] == "target":
			return bot.notice(user.get_nick(), "Targets in Range: " + self.get_fancy_target_list(user.get_nick(), user.get_level()))
						
		#owned properties
		if args[0] == "owned":
			prop = user.load_properties()
			item = user.load_items()
			bot.notice(user.get_nick(), "Owned Properties: " + prop.get_fancy_list(self.props))
			user.set_active()
			return bot.notice(user.get_nick(), "Owned Items: " + item.get_fancy_list(self.items))
			
		#banking money
		if args[0] == "bank":
			if len(args) == 1:
				return bot.notice(user.get_nick(), "Try help bank")
			if len(args) == 2 and args[1] == "balance":
				bank = self.mobs.load_bank(user)
				return bot.notice(user.get_nick(), "Account Balance for " + user.get_who() + ": 03$" + str(bank.get_balance()))
			if len(args) > 2:
				if not args[1] == "deposit" and not args[1] == "withdraw":
					return bot.notice(user.get_nick(), "Try help bank")
				
				bank = self.mobs.load_bank(user)
					
				try:
					if args[2] == "all" and args[1] == "withdraw":
						amount = bank.get_balance()
					elif args[2] == "all" and args[1] == "deposit":
						amount = user.get_cash()
					else:
						amount = self.clean_amount(args[2])
				except ValueError:
					return bot.notice(user.get_nick(), "Invalid amount.")
					
				if amount <= 0:
					return bot.notice(user.get_nick(), "Invalid amount.")
				
				if args[1] == "deposit":
					if user.get_cash() < amount:
						return bot.notice(user.get_nick(), "Insufficient funds.")
					tax = int(amount * 0.1)
					user.add_cash(-1 * amount, 1)
					bank.deposit(amount - tax)
					return bot.notice(user.get_nick(), "Your money has been safely deposited.")
				if args[1] == "withdraw":
					if bank.withdraw(amount) == 2:
						user.add_cash(amount)
						return bot.notice(user.get_nick(), "You have successfully withdrawn 03$" + str(amount))
					else:
						return bot.notice(user.get_nick(), "Insufficient funds.")
			else:
				return bot.notice(user.get_nick(), "No amount specified.")
		
		#healing
		if args[0] == "hospital":
			cost = (user.get_maxhealth() - user.get_health()) * 50
			if cost == 0:
				return bot.notice(user.get_nick(), "You already have max health.")
			if len(args) > 1 and args[1] == "confirm":
				if user.get_cash() < cost:
					return bot.notice(user.get_nick(), "You don't have enough money to do that.")
				user.add_health(cost / 50)
				user.add_cash(cost * -1, 1)
				return bot.notice(user.get_nick(), "You have successfully been healed to full health.")
			else:
				return bot.notice(user.get_nick(), "It will cost 03$" + str(cost) + " to heal you to full health. Type hospital confirm to confirm.")
		
		#attacking
		if args[0] == "attack":
			if len(args) > 1:
				if user.get_stamina() == 0:
					return bot.notice(user.get_nick(), "You don't have enough stamina for that!")
				victim = self.combat.get_attackee(args[1])
				if victim == 0:
					return bot.notice(user.get_nick(), "User not found.")
				if victim.get_host() == "banned":
					return bot.notice(user.get_nick(), "That user is banned.")
				if not victim.get_nick() == user.get_nick():
					return self.combat.fight(bot, user, victim)
				else:
					return bot.notice(user.get_nick(), "You cannot attack yourself.")
			else:
				return bot.notice(user.get_nick(), "Try help attack")
				
		#hitlist
		if args[0] == "hit":
			if len(args) < 3:
				if len(args) == 2 and args[1] == "list":
					hl = self.mobs.get_hitlist()
					return bot.notice(user.get_nick(), ("Available Hitlist: " + hl) if not hl == "" else "No hits currently available")
				return bot.notice(user.get_nick(), "Type help hit")
			victim = self.mobs.load_user(args[1])
			if victim == 0:
				return bot.notice(user.get_nick(), "User not found.")
			try:
				amount = self.clean_amount(args[2])
			except ValueError:
				return bot.notice(user.get_nick(), "Invalid amount.")
			if amount <= 0:
				return bot.notice(user.get_nick(), "Invalid amount.")
				
			if user.get_cash() < amount:
				return bot.notice(user.get_nick(), "Insufficient funds.")
				
			if amount < self.min_hit:
				return bot.notice(user.get_nick(), "Below minimum of 3$" + str(self.min_hit) + ".")
				
			hit = Hit.Hit(victim.get_nick())
			user.add_cash(-1 * amount, 1)
			hit.add_bounty(amount)
			bot.notice(victim.get_nick(), "A hit has been set for you! Current bounty: $" + str(hit.get_bounty()))
			bot.notice(user.get_nick(), "Your hit request has been posted for " + args[1])
			return bot.message(self.mobs.host_channel, "[4Bounty] A 03$" + str(hit.get_bounty()) + " bounty has been set on 02" + args[1])
				
		#selling items
		if args[0] == "sell":
			if len(args) < 3:
				return bot.notice(user.get_nick(), "Try help sell")
			s = message[message.index(args[1]):(message.index(args[len(args) - 1]) - 1)].lower()
			item_id = self.items.get_id(s)
			try:
					amount = self.clean_amount(args[len(args) - 1])
			except ValueError:
				return bot.notice(user.get_nick(), "Invalid amount.")
			if amount < 0:
				return bot.notice(user.get_nick(), "Invalid amount.")
			if item_id == -1:
				return bot.notice(user.get_nick(), "Unknown item! Try again.")
			if self.sell_item(user, item_id, amount) == 2:
				return bot.notice(user.get_nick(), "You sold " + str(amount) + " " + s + " and got $" + str(int(self.items.get_price(item_id) * 0.75 * amount)))
			else:
				return bot.notice(user.get_nick(), "You don't own that many.")
				
		# Mob Cred Store
		if args[0] == "store":
			if not len(args) > 1:
				return bot.notice(user.get_nick(), "Try help store")
			if len(args) == 2 and (args[1] == "hp" or args[1] == "stam" or args[1] == "cash"):
				return bot.notice(user.get_nick(), "Append confirm to this command to confirm you'd like to spend your Mob Cred.")
			if user.get_mobcred() <= 0:
				return bot.notice(user.get_nick(), "You don't have enough mob cred.")
			if args[1] == "hp" and args[2] == "confirm":
				user.edit_maxhealth(25)
				user.edit_mobcred(-1)
				return bot.notice(user.get_nick(), "Your new max health level is " + str(user.get_maxhealth()) + "! You have " + str(user.get_mobcred()) + " mob cred remaining.")
			if args[1] == "stam" and args[2] == "confirm":
				user.edit_maxstamina(1)
				user.edit_mobcred(-1)
				return bot.notice(user.get_nick(), "Your new max stamina level is " + str(user.get_maxstamina()) + "! You have " + str(user.get_mobcred()) + " mob cred remaining.")
			if args[1] == "cash" and args[2] == "confirm":
				user.add_cash(100000)
				user.edit_mobcred(-1)
				return bot.notice(user.get_nick(), "You have " + str(user.get_mobcred()) + " mob cred remaining.")
			else:
				return bot.notice(user.get_nick(), "Improper use of command. Try help store")
		
		#purchasing properties and items
		if args[0] == "buy":
			if len(args) > 1 and args[1] == "list":
				for prop in self.props.get_fancy_list(user):
					bot.notice(user.get_nick(), "7Available Properties: " + prop)
				for item in self.items.get_fancy_list(user.get_level()):
					bot.notice(user.get_nick(), "2Available Items: " + item)
				return bot.notice(user.get_nick(), "3Try buy info item/property and get a description and some info. Further info found on wiki")
			if len(args) < 3:
				return bot.notice(user.get_nick(), "Try help buy")
			if args[1] == "info":
				amount = 0
				s = message[message.index(args[2]):].lower()
			else:
				s = message[message.index(args[1]):(message.index(args[len(args) - 1]) - 1)].lower()
			prop_id = self.props.get_id(s)
			item_id = self.items.get_id(s)
			try:
				if not args[1] == "info":
					amount = self.clean_amount(args[len(args) - 1])
			except ValueError:
				return bot.notice(user.get_nick(), "Invalid amount.")
			if amount < 0:
				return bot.notice(user.get_nick(), "Invalid amount.")
			if prop_id == -1 and item_id == -1:
				return bot.notice(user.get_nick(), "Unknown object! Try again.")
			if prop_id > -1:
				if amount == 0:
					prop = self.props.get_property(prop_id)
					return bot.notice(user.get_nick(), "3(Info)1 " + prop[1] + " - Level: " + prop[0] + " - Cost: " + str(locale.currency(self.props.get_price(prop_id, user), grouping=True)) + " - Income: " + str(locale.currency(int(prop[3]), grouping=True)))
				if self.purchase_property(user, prop_id, amount) == 2:
					return bot.notice(user.get_nick(), "You have successfully purchased " + str(amount) + " " + s + "s.")
				else:
					return bot.notice(user.get_nick(), "Sorry, you don't have enough money to do that.")
			if item_id > -1:
				if amount == 0:
					item = self.items.get_item(item_id)
					return bot.notice(user.get_nick(), "3(Info)1 " + item[1] + " - Level: " + item[0] + " - Cost: " + str(locale.currency(int(item[2]), grouping=True)) + " - " + ("Upkeep: " + str(locale.currency(int(item[3]), grouping=True)) + " - " if int(item[3]) > 0 else "") + "Att Bonus: " + item[4] + " - Def Bonus: " + item[5])
				if ((self.mobs.get_netw(user) - (self.items.get_upkeep(item_id) * amount)) < 0):
					return bot.notice(user.get_nick(), "You cannot go into debt buying items.")
				if self.purchase_item(user, item_id, amount) == 2:
					return bot.notice(user.get_nick(), "You have successfully purchased " + str(amount) + " " + s + "s.")
				else:
					return bot.notice(user.get_nick(), "Sorry, you don't have enough money to do that.")
