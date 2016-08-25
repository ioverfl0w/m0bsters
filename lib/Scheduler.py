class Scheduler:
	
	def __init__(self):
		self.evt = []
		
	def get_event(self, name):
		for x in self.evt:
			if x.name == name:
				return x
		return None
		
	def get_list(self):
		result = []
		for e in self.evt:
			result.append(e.name)
		return result
		
	def schedule_event(self, sched):
		self.evt.append(sched)
		sched.clear()

	def reload_mods(self):
		for x in self.evt:
			try:
				x.reload_schedule()
			except Exception:
				pass

	def check(self):
		for x in self.evt:
			if x.strike():
				x.perform()
				x.clear()
