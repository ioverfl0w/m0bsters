"""
Used to determine if connection has been lost or not.
"""

import traceback
import time

class KeepAlive:
	
	def __init__(self, eng):
		self.name = "keepalive"
		#delay in seconds
		self.delay = 30
		self.start = 0
		self.engine = eng
		self.bots = []

	def reload_schedule(self):
		self.bots = self.engine.get_bots()
		
	def strike(self):
		return (self.start + self.delay) <= time.time()
			
	def clear(self):
		self.start = time.time()

	def perform(self):
		self.engine.check()
		for b in self.bots:
			b.ping()
