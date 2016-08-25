class Property:
	
	def __init__(self, nick):
		self.nick = nick
		try:
			self.props = self.load_list()
		except EnvironmentError:
			self.props = []
			
	def get_fancy_list(self, db):
		s = ""
		for x in self.get_prop_list():
			s += x[1] + " " + db.get_label(x[0]) + ", "
		return s
		
	def get_prop_list(self):
		return self.props
		
	def get_value(self, prop_id):
		for x in self.get_prop_list():
			if int(x[0]) == int(prop_id):
				return int(x[1])
		return 0
	
	def get_tax(self, prop_id, price):
		return int((self.get_value(prop_id) * price) * 0.1)
		
	def get_total_income(self, market):
		t = 0
		for a in self.get_prop_list():
			t += market.get_income(a[0]) * int(a[1])
		return t
		
	def add_property(self, prop_id, amount):
		i = 0
		for a in self.get_prop_list():
			if int(a[0]) == prop_id:
				self.props[i][1] = int(a[1]) + amount
				return self.update()
			i += 1
		self.props.append([prop_id, amount])
		return self.update()
		
	def update(self):
		f = open("./data/mobster/property/" + self.nick + ".p", 'w')
		for x in self.get_prop_list():
			f.write(str(x[0]) + "\t" + str(x[1]) + "\n")
		f.close()
		return 2
		
	def load_list(self):
		return [line.strip().split("\t") for line in open("./data/mobster/property/" + self.nick + ".p")]
