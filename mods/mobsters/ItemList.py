import locale

class ItemList:
	
	def __init__(self, f):
		self.items = self.sort(f)
		
	def rreplace(self, s, old, new):
		li = s.rsplit(old, 1)
		return new.join(li)
		
	def clean_amount(self, amount):
		amount = self.rreplace(amount, "000000000", "b")
		amount = self.rreplace(amount, "000000", "m")
		amount = self.rreplace(amount, "000", "k")
		return amount
		
	def get_fancy_list(self, lvl):
		s = "1"
		r = []
		c = 0
		for x in self.items:
			if lvl >= int(x[0]):
			    # AttBonus, DefBonus, Cost, Upkeep
				s += x[1] + " [03" + x[4] + "/02" + x[5] + "/4$" + self.clean_amount(x[2]) + "/5$" + self.clean_amount(x[3]) + "1], "
				c += 1
				
				if c == 11:
					r.append(s)
					s = "1"
					c = 0
		if not s == "1":
			r.append(s)
		return r
		
	def get_item_count(self):
		return len(self.items)
		
	def get_item(self, i):
		return self.items[int(i)]
		
	def get_level(self, i):
		return int(self.get_item(i)[0])
		
	def get_label(self, i):
		return str(self.get_item(i)[1])
		
	def get_price(self, i):
		return int(self.get_item(i)[2])
		
	def get_upkeep(self, i):
		return int(self.get_item(i)[3])
		
	def get_att_bonus(self, i):
		return int(self.get_item(i)[4])
		
	def get_def_bonus(self, i):
		return int(self.get_item(i)[5])
		
	def get_id(self, label):
		i = 0
		for x in self.items:
			if x[1].lower() == label:
				return i
			i += 1
		return -1
		
	def sort(self, inpu):
		lst = []
		for x in inpu:
			lst.append(x.split("\t"))
		return lst
