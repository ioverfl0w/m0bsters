import time

class MessageBuffer:
	
	def __init__(self):
		self.specific = 0
		self.rule = [8, 3]
		self.cache = []
		self.cul = []
		
	def add(self, user):
		self.cache.append([user, time.time()])
		
	def clear(self):
		self.cache = []
		
	def get_culprits(self):
		s = ""
		for c in self.cul:
			s += c[0].get_nick() + ", "
		self.cul = []
		return s
		
	def check(self):
		if len(self.cache) > 1 and self.cache[len(self.cache) - 2][1] + self.rule[1] < self.cache[len(self.cache) - 1][1]:
			self.clear()
			return 0
		if len(self.cache) >= self.rule[0]:
			if self.cache[(len(self.cache) - 1)][1] - self.cache[0][1] <= self.rule[1]:
				self.cul = self.cache
				self.clear()
				return 2
			self.clear()
		return 0
