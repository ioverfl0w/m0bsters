import socket
import ssl
import time

class IrcBot:

	def __init__(self, eng, net, sslEnable=True):
		self.nick = None
		self.engine = eng
		self.network = net
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.network.address, self.network.port))
		if sslEnable:
			self.irc = ssl.wrap_socket(sock)
		self.irc.setblocking(0)
		self.irc.settimeout(.01)

	def __str__(self):
		return "[Name:" + self.network.name + " Addr:" + self.network.address + ";Port:" + str(self.network.port) + "]"

	def close(self):
		try:
			self.irc.send("QUIT Quit\r\n")
			self.irc.close()
		except Exception:
			pass

	def connect(self, ident):
		self.nick = ident.nick
		self.irc.send("NICK " + ident.nick + "\r\n")
		self.irc.send("USER " + ident.user + " * * :5Become the next top mobster in #mobsters\r\n")

		while True:
			s = self.read()

			if s == "":
				continue

			s = s.strip()
			x = s.split("\n")

			for y in x:
				a = y.split(" ")
				#print y

				if a[0].lower() == "ping":
					self.pong(a[1])
					continue

				if a[1] == "433":
					print "ERROR - nick in use!"
					exit()

				if a[1] == "376":
					if not ident.nickserv == None:
						self.message("NickServ", "identify " + ident.nickserv)
						time.sleep(1)

					if not ident.ajoin == None:
						for chan in ident.ajoin:
							self.join(chan)
							
					#set private umode
					self.mode(self.nick + " +p")
					return

	def send(self, st):
		try:
			self.irc.send(st + "\r\n")
		except:
			self.engine.shutdown(self)

	def ping(self):
		self.send("PING novabotirc")

	def whois(self, target):
		self.send("WHOIS " + target)

	def pong(self, arg):
		self.send("PONG " + arg)

	def message(self, target, message):
		self.send("PRIVMSG " + target + " :" + message)

	def notice(self, target, message):
		self.send("NOTICE " + target + " :" + message)

	def join(self, chan):
		self.send("JOIN " + chan)
		self.send("WHO " + chan)

	def part(self, chan):
		self.send("PART " + chan + "\r\n")

	def kick(self, chan, who):
		self.send("KICK " + chan + " " + who + " :Goodbye")

	def mode(self, modes):
		self.send("MODE " + modes)

	def read(self):
		try:
			return self.irc.recv(4096).strip()
		except socket.error:
			return ""
