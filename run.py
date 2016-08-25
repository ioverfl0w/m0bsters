#
#
#                _           _                   
#  /\/\    ___  | |__   ___ | |_  ___  _ __  ___ 
# /    \  / _ \ | '_ \ / __|| __|/ _ \| '__|/ __|
#/ /\/\ \| (_) || |_) |\__ \| |_|  __/| |   \__ \
#\/    \/ \___/ |_.__/ |___/ \__|\___||_|   |___/
#                                                                                
#
#
import sys
import time
sys.path.append("./lib/")
import Logger
import Event
import Access
import Scheduler
import Engine
import Utility
sys.path.append("./sched/")
import AuthSys
import KeepAlive
import MobsUpdate
import Regen
import MissionClock
import Security
sys.path.append("./mods/")
import SpamFilter
import Basic
import Mobster
import Missions
import LegalAffairs

logger = Logger.Logger()
access = Access.Access(logger)
event = Event.Event(access)
scheduler = Scheduler.Scheduler()

# bot network info
#		Title	Network			Port	NICK	USER		NICKSERV		[AJOIN]
rizon = Utility.Network("rizon", "irc.rizon.net", 6697)
ajoin = ["#mobsters", "#nova"] #First channel in Array will be the active game channel, 2nd channel is the OPs channel

#Two bots are required. First bot will be the main game bot, while the second one is the missions bot
bots = [[rizon, Utility.Identity("mobsters", "mobster", None, ajoin)],
		[rizon, Utility.Identity("DonVito", "dv", None, ajoin)]]
		
eng = Engine.Engine(event, bots, scheduler, logger) #event, bots, sched, logger
eng.soft_start() # This is a mobster's mod
bots = eng.get_bots()
#(CORE) modules we are loading
scheduler.schedule_event(AuthSys.AuthSys(eng))
scheduler.schedule_event(KeepAlive.KeepAlive(eng))
event.add_mod(SpamFilter.SpamFilter(bots[0], eng)) #SpamFilter (mobsters only)
event.add_mod(Basic.Basic(eng))


## GAME WORK		
		
#create the game instance
mobs = Mobster.Mobster(eng, bots[0], ajoin[0], Security.Security(bots[0], ajoin))
msnclk = MissionClock.MissionClock(bots[1], mobs.host_channel)
regen = Regen.Regen(mobs, bots[0])

#Module Instances
event.add_mod(mobs) #Mobster Game (mobsters only)
event.add_mod(LegalAffairs.LegalAffairs(bots[0], mobs, regen)) #Mobs (mobsters only)
event.add_mod(Missions.Missions(bots[1], mobs, msnclk)) #DonVito

#Scheduled Instances
scheduler.schedule_event(MobsUpdate.MobsUpdate(bots[1], mobs, ajoin[1])) #PayDay
scheduler.schedule_event(regen) #PointRegen
scheduler.schedule_event(msnclk)#MissionClock
scheduler.schedule_event(mobs.get_security())#SecurityTimer

## END GAME WORK

eng.execute()

