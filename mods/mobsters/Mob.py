import os

class Mob:
	
	def __init__(self, mob):
		self.name = mob
		try:
			self.mob = self.load_list()
		except EnvironmentError:
			self.mob = []
			
	def get_name(self):
		return self.name
			
	def get_size(self):
		return len(self.mob)
		
	def get_list(self):
		s = ""
		for m in self.mob:
			s += m[0] + ", "
		return s
			
	def check_mob(self, nick):
		for n in self.mob:
			if n[0].lower() == nick.lower():
				return True
		return False
		
	def get_access(self, nick):
		for n in self.mob:
			if n[0].lower() == nick.lower():
				return int(n[1])
		return 0
		
	def set_access(self, nick, new_acc):
		user = self.get_user(nick)
		if user == 0:
			return 0
		
		for i in range(0, len(self.mob)):
			if self.mob[i][0] == user[0]:
				self.mob[i][1] = new_acc
				return self.update()
		return 0
				
		
	def get_user(self, nick):
		for n in self.mob:
			if n[0].lower() == nick.lower():
				return n
		return 0
		
	def add_mobster(self, nick, access):
		self.mob.append([nick, access])
		return self.update()
		
	def rem_mobster(self, nick):
		u = self.get_user(nick)
		if u == 0:
			return 0
			
		self.mob.remove(u)
		
		#delete empty mobs
		if len(self.mob) == 0:
			os.remove("./data/mobster/mobs/" + self.name + ".m")
			return 2
		return self.update()
		
	def update(self):
		f = open("./data/mobster/mobs/" + self.name + ".m", 'w')
		for n in self.mob:
			f.write(str(n[0]) + "\t" + str(n[1]) + "\n")
		f.close()
		return 2
		
	def load_list(self):
		return [line.strip().split("\t") for line in open("./data/mobster/mobs/" + str(self.name) + ".m")]
