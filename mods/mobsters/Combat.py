import math
import random
import locale
import Hit

# This section really needs some work.... Balancing is not my forte

class Combat:

	def __init__(self, mobs):
		self.mobs = mobs
		self.base_damage = 2
		self.attack_range = 15 #level difference to fight
		self.xp_rate = 2 #(multiplier)
		self.killed_terms = mobs.import_file("./data/mobster/data/killed_terms.l")
		
	def get_attackee(self, nick):
		return self.mobs.load_user(nick)
		
	def is_dead(self, user):
		return True if user.get_health() == 0 else False
		
	def fight(self, bot, host, victim):
		# This Will Add a level range for attacking !!
		#if math.fabs(host.get_level() - victim.get_level()) > self.attack_range:
		#	return bot.notice(host.get_nick(), "Your level difference is too great. (Your level: " + str(host.get_level()) + " - Their level: " + str(victim.get_level()) + ")")
		
		if victim.get_health() <= round(victim.get_maxhealth() * .1):
			return bot.notice(host.get_nick(), "They are currently in the emergency room!")
		
		fight = [self.get_damage(host, victim), self.get_damage(victim, host)]
		
		victim.add_health(fight[0] * -1)
		host.add_health(fight[1] * -1)
		
		host.add_stamina(-1)
		
		h = host.add_xp(fight[0] * self.xp_rate)
		v = victim.add_xp(fight[1] * self.xp_rate)
		bot.message(self.mobs.host_channel, "04" + host.get_nick() + " attacked 02" + victim.get_nick() + " and deals 04" + str(fight[0]) + " damage. " +
											"02" + victim.get_nick() + " retaliates and deals 04" + str(fight[1]) + ".")
											
		if fight[0] > fight[1]:#host won
			c = 0 if victim.get_cash() <= 0 else int(victim.get_cash() / 5)
			victim.add_cash(-1 * c)
			host.add_cash(c, 1)
			bot.notice(host.get_nick(), "You remove " + str(locale.currency(c, grouping=True)) + " from " + victim.get_nick() + "'s wallet.")
		else:#victim won
			c = 0 if host.get_cash() <= 0 else int(host.get_cash() / 5)
			host.add_cash(-1 * c)
			victim.add_cash(c)
			bot.notice(host.get_nick(), "You were robbed of " + str(locale.currency(c, grouping=True)) + "!")
											
		#check if died
		if self.is_dead(host):
			self.died(bot, victim, host)
		if self.is_dead(victim):
			self.died(bot, host, victim)
			
		#handle leveling up
		if h == 1:
			self.levelup(bot, host)
		if v == 1:
			self.levelup(bot, victim)
				
		
	def died(self, bot, killer, victim):
		bot.message(self.mobs.host_channel, "[4Defeat] 02" + victim.get_nick() + " was " + self.killed_terms[random.randint(0, len(self.killed_terms) - 1)] + " by 02" + killer.get_nick() + ".")
		
		#revive them
		case = self.mobs.import_file("./data/mobster/data/death_terms.l")
		case = case[random.randint(0, len(case) - 1)].split("\t")
		victim.add_health(victim.get_maxhealth())
		
		#penalty + prize
		cash = 0 if victim.get_cash() <= 0 else (victim.get_cash() / 2)
		victim.add_cash(cash * -1)
		killer.add_cash(cash)
		victim.add_death()
		killer.add_kill()
		bot.notice(victim.get_nick(), "Your body was recovered from " + case[0] + " by " + case[1] + ". You notice your wallet is missing $" + str(cash) + "...")
		bot.notice(killer.get_nick(), "You search " + victim.get_nick() + "'s body and find $" + str(cash) + ".")
		
		#check for bountys
		hit = Hit.Hit(victim.get_nick())
		if not hit.exist():
			return
			
		killer.add_hit()
		killer.add_cash(hit.get_bounty())
		bot.message(self.mobs.host_channel, "[3Bounty] Bounty of 3$" + str(hit.get_bounty()) + " on 02" + victim.get_nick() + " has been claimed by 02" + killer.get_nick())
		bot.notice(killer.get_nick(), "You take the body of " + victim.get_nick() + " and bring him into Don Vito's cafe to claim your Hit Reward of " + str(hit.get_bounty()))
		hit.delete()
		
	def get_damage(self, attacker, victim):
		level_diff = attacker.get_level() - victim.get_level()
		att_bonus = self.get_bonuses(attacker)
		vic_bonus = self.get_bonuses(victim)
		mn = random.randint(1, 4) if att_bonus[0] > vic_bonus[1] else 0
		mx = (self.base_damage if att_bonus[0] > vic_bonus[1] else 0) + random.randint(1, ((att_bonus[0] - vic_bonus[1]) if mn > 0 else 1))
		att = random.randint(0 + mn, mx)
		return victim.get_health() if att > victim.get_health() else att
		
	def get_bonuses(self, user):
		i = user.load_items()
		m = user.load_mob()
		return [int(i.get_attack_bonus(self.mobs.item_list, m)), int(i.get_defence_bonus(self.mobs.item_list, m))]
		
	def levelup(self, bot, u):
		earned = int(math.pow(u.get_level() + level_offset, 3))
		u.add_cash(earned)
		bot.notice(u.get_nick(), "Congratulations! You are now level " + str(u.get_level()) + ". You have earned $" + str(earned) + ".")
		bot.message(self.mobs.host_channel, "[3Achievement] 2" + u.get_nick() + " has risen to level " + str(u.get_level()) + ".")
		
		#Award with Mob Cred
		u.edit_mobcred(self.mobs.mobCredLevelUp)
		bot.notice(u.get_nick(), "You have been awarded " + str(self.mobs.mobCredLevelUp) + " Mob Cred! Use help store to learn more about mob cred.")

level_offset = 15
