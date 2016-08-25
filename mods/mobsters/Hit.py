import os

class Hit:
	
	def __init__(self, nick):
		self.nick = nick
		try:
			self.args = self.load_list()
		except EnvironmentError:
			self.args = []
			
	def exist(self):
		return not len(self.args) == 0
			
	def get_bounty(self):
		return int(self.args[0])
		
	def add_bounty(self, amount):
		#new bounty
		if not self.exist():
			self.args.append(amount)
		else:
			self.args[0] = int(self.args[0]) + amount
		return self.update()
		
	def delete(self):
		os.remove("./data/mobster/hitlist/" + self.nick + ".h")
		
	def update(self):
		f = open("./data/mobster/hitlist/" + self.nick + ".h", 'w')
		for n in self.args:
			f.write(str(n) + "\n")
		f.close()
		return 2

	def load_list(self):
		return [line.strip() for line in open("./data/mobster/hitlist/" + self.nick + ".h")]
