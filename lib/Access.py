"""

USER RIGHTS:

0 - normal
1 - trusted
2 - admin
3 - root

"""

class Access:
	
	def __init__(self, logger):
		self.list = []
		self.auth = None
		self.location = "./data/access.dat"
		self.log = logger
		self.reload_access()

	def set_authsys(self, sys, confirm=False):
		if self.auth == None or confirm:
			self.auth = sys
			return
		else:
			self.log.write("Critical: AuthSys not carried")
			exit()
			
	def get_status(self, who, net):
		who = who.lower()
		net = net.lower()
		for i in range(len(self.list)):
			if self.list[i][0].lower() == net and self.list[i][1] == who:
				return i
		return None
		
	def update_user(self, who, net, level):
		index = self.get_status(who, net)
		level = int(level)
		if index == None:
			self.add_user(who, net, level)
		else:
			self.list[index] = self.configure(who,net,level)
		self.log.write("Updated access +(" + who + "@" + net + " --> " + str(level) + ")+")
		return self.update_access()

	def is_authed(self, who, bot):
		return self.auth.session_exist(bot.network.name, who)
	
	def add_user(self, who, net, level):
		self.list.append(self.configure(who,net,level))
		
	def rem_user(self, who, net):
		index = self.get_status(who, net)
		if index == None:
			return False
		self.log.write("Updated access -(" + who + "@" + net + ")-")
		del self.list[index]
		return True
		
	def configure(self, who, net, level):
		return [net.lower(), who.lower(), int(level)]
		
	def get_user_rights(self, who, bot):
		who = who[0].lower()
		for u in self.list:
			if (u[0].lower() == bot.network.name.lower()) and (u[1].lower() == who):
				return u[2] if self.is_authed(who, bot) else 0
		return 0

	def has_rights(self, who, bot):
		who = who.lower()
		for u in self.list:
			if (u[0].lower() == bot.network.name.lower()) and (u[1].lower() == who):
				return True
		return False
		
	def update_access(self):
		o = open(self.location, 'w')
		for x in self.list:
			o.write(x[1] + "\t" + x[0] + "\t" + str(x[2]) + "\n")
		o.close()
		return True

	def reload_access(self):
		self.list = []
		o = open(self.location, 'r')
		i = o.read()
		o.close()

		if not self.auth == None:
			self.auth.clear_sessions()

		line = i.split("\n")
		for l in line:
			if not l.startswith("#"):
				args = l.split("\t")
				if len(args) == 3:
					# nick	net	lvl
					self.add_user(args[0], args[1], int(args[2]))
