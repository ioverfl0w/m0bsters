import locale

class PropertyList:
	
	def __init__(self, f):
		self.props = self.sort(f)
		
	def rreplace(self, s, old, new):
		li = s.rsplit(old, 1)
		return new.join(li)
		
	def clean_amount(self, amount):
		amount = self.rreplace(amount, "000000000", "b")
		amount = self.rreplace(amount, "000000", "m")
		amount = self.rreplace(amount, "000", "k")
		return amount
		
	def get_fancy_list(self, user):
		s = "1"
		r = []
		count = 0
		caunt = 0
		for x in self.props:
			if user.get_level() >= int(x[0]):
			    # Cost, Income
				s += x[1] + " (4C:$" + self.clean_amount(str(self.get_price(count, user))) + ",3I:$" + self.clean_amount(str(self.get_income(count))) + "1), "
				count += 1
				caunt += 1
				
				
				if caunt == 10:
					r.append(s)
					s = "1"
					caunt = 0
		if not s == "1":
			r.append(s)
		return r
		
	def get_property(self, i):
		return self.props[int(i)]
		
	def get_level(self, i):
		return int(self.get_property(i)[0])
		
	def get_label(self, i):
		return str(self.get_property(i)[1])
		
	def get_price(self, i, user):
		price = int(self.get_property(i)[2])
		return (price + user.load_properties().get_tax(i, price))
		
	def get_income(self, i):
		return int(self.get_property(i)[3])
	
	def get_id(self, label):
		i = 0
		for x in self.props:
			if x[1].lower() == label:
				return i
			i += 1
		return -1
		
	def sort(self, inpu):
		lst = []
		for x in inpu:
			lst.append(x.split("\t"))
		return lst
