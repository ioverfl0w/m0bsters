class Network:

	def __init__(self, name, address, port):
		self.name = name
		self.address = address
		self.port = port

class Identity:

	def __init__(self, nick, user, pw, ajoin):
		self.nick = nick
		self.user = user
		self.nickserv = pw
		self.ajoin = ajoin

class Misc:

	def space(self, string, total_len):
		if len(string) > total_len:
			return string_a
		
		return string + (" " * (total_len - len(string)))

	def timedString(self, seconds):
		m = int(seconds / 60)
		s = int(seconds - (m * 60))
		h = 0 if m < 60 else m / 60
		m = m if h == 0 else m - (h * 60)
		return ("" if h == 0 else str(h) + "h") + ("" if m == 0 else str(m) + "m") + str(s) + "s";
