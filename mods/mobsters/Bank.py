class Bank:
	
	def __init__(self, user):
		self.nick = user.get_nick()
		try:
			self.balance = int(self.load_list()[0])
		except EnvironmentError:
			self.balance = 0
			
	def get_balance(self):
		return self.balance
		
	def withdraw(self, amount):
		if self.balance >= amount:
			self.balance -= amount
			return self.update()
		return 1
		
	def deposit(self, amount):
		self.balance += amount
		return self.update()
		
	def update(self):
		f = open("./data/mobster/bank/" + self.nick + ".b", 'w')
		f.write(str(self.balance))
		f.close()
		return 2
		
	def load_list(self):
		return [line.strip() for line in open("./data/mobster/bank/" + self.nick + ".b")]
