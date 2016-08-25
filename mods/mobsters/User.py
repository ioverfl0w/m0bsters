import math
import time
import Property
import Item
import Mob

active_time = 60 * 60 * 24

#
#
# 0 - nick @ host
# 1 - recovery key (plaintext, maybe should change that lol)
# 2 - cash on hand
# 3 - level
# 4 - xp
# 5 - current health
# 6 - current stamina
# 7 - kill count
# 8 - death count
# 9 - hit count
# 10 - last active (ms)
# 11 - mob name
# 12 - max health
# 13 - max stamina
# 14 - mob cred points
#
#

class User:
	
	def __init__(self, args): #creates an identified user
		self.items = args
		
	def get_nick(self):
		return str(self.items[0].split("@")[0])
		
	def get_host(self):
		return str(self.items[0].split("@")[1])
		
	def get_who(self):
		return str(self.items[0])
		
	def get_recovery_key(self):
		return str(self.items[1])
		
	def get_cash(self):
		return int(self.items[2])
		
	def get_level(self):
		return int(self.items[3])
		
	def get_xp(self):
		return int(self.items[4])
		
	def get_health(self):
		return int(self.items[5])
		
	def get_maxhealth(self):
		return int(self.items[12])
		
	def get_stamina(self):
		return int(self.items[6])
		
	def get_maxstamina(self):
		return int(self.items[13])
		
	def get_mobcred(self):
		return int(self.items[14])
		
	def get_kill_count(self):
		return int(self.items[7])
		
	def get_death_count(self):
		return int(self.items[8])
		
	def get_hit_count(self):
		return int(self.items[9])
		
	def get_last_active(self):
		return float(self.items[10])
		
	def get_mob_name(self):
		try:
			return int(self.items[11])
		except ValueError:
			return self.items[11]
		
	def get_income(self, db):
		return self.load_properties().get_total_income(db)
		
	def get_upkeep(self, db):
		return self.load_items().get_total_expense(db)
	
	def edit_host(self, new_host):
		self.items[0] = self.get_nick() + "@" + new_host
		self.update()
		
	def next_level(self):
		return int(math.pow(self.get_level() + 3, 3))
		
	def add_xp(self, amount):
		code = 0
		self.items[4] = int(self.items[4]) + amount
		if self.get_xp() >= self.next_level():#level up
			self.items[3] = int(self.items[3]) + 1
			code = 1
		self.update()
		return int(code)
		
	def add_health(self, amount):
		self.items[5] = int(int(self.items[5]) + amount)
		self.update()
		
	def add_stamina(self, amount):
		self.items[6] = int(self.items[6]) + amount
		self.update()
		
	def add_cash(self, amount, active=0):
		self.items[2] = self.get_cash() + amount
		self.update(active)
		return self.items[2]
		
	def edit_mobcred(self, a):
		self.items[14] = int(self.items[14]) + a
		self.update()
		
	def edit_maxhealth(self, m):
		self.items[5] = int(self.items[5]) + m # add to current health as welllll
		self.items[12] = int(self.items[12]) + m
		self.update()
		
	def edit_maxstamina(self, s):
		self.items[6] = int(self.items[6]) + s # add to current stamina
		self.items[13] = int(self.items[13]) + s
		self.update()
		
	def add_kill(self):
		self.items[7] = int(self.items[7]) + 1
		self.update()
		
	def add_death(self):
		self.items[8] = int(self.items[8]) + 1
		self.update()
		
	def add_hit(self):
		self.items[9] = int(self.items[9]) + 1
		self.update()
		
	def set_active(self):
		self.update(1)
		
	def edit_mob(self, new_mob):
		self.items[11] = new_mob
		self.update(1)
		
	def is_inactive(self):
		return ((float(self.items[10]) + active_time) < time.time())
		
	def sell_item(self, db, item_id, amount):
		self.add_cash(int(db.get_price(item_id) * 0.75) * amount, 1)
		return self.load_items().del_item(item_id, amount)
		
	def purchase_item(self, db, item_id, amount):
		self.add_cash(-1 * (db.get_price(item_id) * amount), 1)
		return self.load_items().add_item(item_id, amount)
		
	def purchase_property(self, db, prop_id, amount):
		self.add_cash(-1 * ((db.get_price(prop_id, self) * amount)), 1)
		return self.load_properties().add_property(prop_id, amount)
		
	def load_properties(self):
		return Property.Property(self.get_nick())
		
	def load_items(self):
		return Item.Item(self.get_nick())
		
	def load_mob(self):
		return 0 if self.get_mob_name() == 0 else Mob.Mob(self.get_mob_name())
		
	def update(self, active=0):
		if active == 1:
			self.items[10] = time.time()
		f = open("./data/mobster/users/" + self.get_nick().lower() + ".u", 'w')
		for x in self.items:
			f.write(str(x) + "\n")
		f.close()
