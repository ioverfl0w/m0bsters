import time

class AuthSys:
	
	def __init__(self, eng):
		self.name = "authsys"
		self.engine = eng
		self.engine.get_access().set_authsys(self)
		self.session = []
		#delay in seconds
		self.delay = 60*60 #1 hour timed session (time is in seconds)
		self.start = 0

	def clear_sessions(self):
		i = str(len(self.session))
		self.session = []
		self.engine.log.write("AuthSessions cleared. Sessions removed: " + i)
		
	def get_session(self, net, who):
		index = self.session_index(net, who)
		return self.session[index] if index >= 0 else None

	def session_index(self, net, who):
		net = net.lower()
		who = who.lower()
		for i in range(len(self.session)):
			if self.session[i][0].lower() == net and self.session[i][1].lower() == who:
				return i
		return -1

	def session_exist(self, net, who):
		net = net.lower()
		who = who.lower()
		for ses in self.session:
			if ses[0].lower() == net and ses[1].lower() == who:
				return True
		return False
		
	def time_left_list(self):
		result = []
		for session in self.session:
			result.append([session[0], session[1], (session[2] + self.delay) - time.time()])
		return result
		
	def time_left(self, index):
		return (self.session[index][2] + self.delay) - time.time()

	def add_session(self, net, who):
		if self.session_exist(net, who[0]):
			return False
			
		self.session.append([net, who, time.time()])
		if len(self.session) == 1:
			self.clear(locked=False)
			
		self.engine.log.write("AuthSession created for " + who + "@" + net)
		return True

	def del_session(self, ses):
		self.session.remove(ses)
		self.engine.log.write("AuthSession expired for " + ses[1] + "@" + ses[0])
		
		if len(self.session) > 0:
			self.start = self.session[0][2]
			#self.engine.log.write("AuthSys timed for " + self.session[0][1] + "@" + self.session[0][0]);
		
	def strike(self):
		return (self.start + self.delay) <= time.time()
			
	def clear(self, locked=True):
		if not locked:
			self.start = time.time()
	
	def perform(self):
		if len(self.session) == 0:
			return

		for ses in self.session:
			if (ses[2] + self.delay) <= time.time():
				self.del_session(ses)

