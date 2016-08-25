class Item:
	
	def __init__(self, nick):
		self.nick = nick
		try:
			self.items = self.load_list()
		except EnvironmentError:
			self.items = []
		
	def get_fancy_list(self, db):
		s = ""
		for x in self.get_item_list():
			s += x[1] + " " + db.get_label(x[0]) + ", "
		return s
		
	def get_item_list(self):
		return self.items
		
	def get_value(self, item_id):
		for val in self.items:
			if int(val[0]) == int(item_id):
				return int(val[1])
		return -1
		
	def get_total_expense(self, market):
		t = 0
		for a in self.get_item_list():
			t += (market.get_upkeep(a[0]) * int(a[1]))
		return t
		
	def get_attack_bonus(self, market, mob):
		t = 0
		size = mob.get_size() if not mob == 0 else 0
		for a in self.get_item_list():
			t += (market.get_att_bonus(a[0]) * ((size if size < int(a[1]) else int(a[1])) if size > 0 else 1))
		return t	
			
	def get_defence_bonus(self, market, mob):
		t = 0
		size = mob.get_size() if not mob == 0 else 0
		for a in self.get_item_list():
			t += (market.get_def_bonus(a[0]) * ((size if size < int(a[1]) else int(a[1])) if size > 0 else 1))
		return t
		
	def del_item(self, item_id, amount):
		i = 0
		for a in self.get_item_list():
			if int(a[0]) == item_id:
				self.items[i][1] = int(a[1]) - amount
				if self.items[i][1] == 0:
					self.items.remove(self.items[i])
				return self.update()
			i += 1
		return self.update()
		
	def add_item(self, item_id, amount):
		i = 0
		for a in self.get_item_list():
			if int(a[0]) == item_id:
				self.items[i][1] = int(a[1]) + amount
				return self.update()
			i += 1
		self.items.append([item_id, amount])
		return self.update()
		
	def update(self):
		f = open("./data/mobster/item/" + self.nick + ".i", 'w')
		for x in self.get_item_list():
			f.write(str(x[0]) + "\t" + str(x[1]) + "\n")
		f.close()
		return 2
		
	def load_list(self):
		return [line.strip().split("\t") for line in open("./data/mobster/item/" + self.nick + ".i")]

max_items_used = 10
