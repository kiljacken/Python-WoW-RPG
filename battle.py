#!/usr/bin/python
import random
import configurate as conf
import itemsystems

def percent_reduce(int, perct):
    return float(int)-(float(int)/float(100)*float(perct))

# -- Stuff for spells
class dam:
    # -- Normal Damages
    mel = 'melee'
    ran = 'ranged'
    # -- Magic Damages
    phy = 'physical'
    arc = 'arcane'
    fir = 'fire'
    fro = 'frost'
    nat = 'nature'
    sha = 'shadow'
    hol = 'holy'
    
    def __getitem__(self, item):
        return '%s.damage' %eval('self.'+item)
        
    def random(self, ranged=None):
        if ranged:
            dmgs = 'mel ran arc fir fro nat sha hol'.split(' ')
        else:
            dmgs = 'mel arc fir fro nat sha hol'.split(' ')
        return self[random.choice(dmgs)]
    
class bon:
    dmg = 'damage'
    hea = 'health'
    arm = 'armor'
    
    def __getitem__(self, item):
        return '%s.bonus' %eval('self.'+item)
    
    def random(self):
        bons = 'dmg hea arm'.split(' ')
        return self[random.choice(bons)]
    
class shi:
    hea = 'health'
    spe = 'spell'
    
    def __getitem__(self, item):
        return '%s.shield' %eval('self.'+item)
    
# -- Battle command parser
class BattleBackend:
    def __init__(self, monster, gameclass):
        self.dataclass = gameclass
        self.mon = monster
        self.pla = gameclass.data
        self.log = {'player': {'hits': [], 'other': []}, 'monster': {'hits': [], 'other': []}}
        self.php = self.dataclass.data.get_hp()
        # -- Not supported yet
        self.dmgbonus = 0
        self.reduction = 0
        self.shield = 0

    def start(self):
        self.dataclass.eh.RaiseEvent('OnCombat', 'Player is entering combat')
        while 1:
            cmd = raw_input('Battle >>> ')
            self.sendCommand(cmd)
            if self.php <= 0 or self.mon.hp <= 0:
                break
        self.deathCheck()
        
    def sendCommand(self, cmd):
        if cmd == 'hit':
            ph = self.pla.roll_damage()
            mh = self.mon.roll_damage()
            self.mon.hp -= ph
            self.php -= int(percent_reduce(mh, self.dataclass.data.get_armor_reduction()))
            print '<Battle> %s hits %s for %s damage, %s has %s hp left...' %(self.pla.name, self.mon.name, str(ph), self.mon.name, self.mon.hp)
            print '<Battle> %s hits %s for %s damage, %s has %s hp left...' %(self.mon.name, self.pla.name, str(mh), self.pla.name, self.php)
            self.log['player']['hits'].append(ph)
            self.log['monster']['hits'].append(mh)
        elif cmd.startswith('spell'):
            splname = ' '.join(cmd.split(' ')[1:]).title()
            ph = self.pla.spell_damage(splname)
            mh = self.mon.roll_damage()
            self.mon.hp -= ph
            self.php -= int(percent_reduce(mh, self.dataclass.data.get_armor_reduction()))
            print '<Battle> %s hits %s for %s damage, %s has %s hp left...' %(self.pla.name, self.mon.name, str(ph), self.mon.name, self.mon.hp)
            print '<Battle> %s hits %s for %s damage, %s has %s hp left...' %(self.mon.name, self.pla.name, str(mh), self.pla.name, self.php)
            self.log['player']['hits'].append(ph)
            self.log['monster']['hits'].append(mh)
        elif cmd == 'flee':
            print '<Battle> %s flees from battle...' %self.pla.name
            self.php = 0
            self.mon.hp = 0
        elif cmd == 'hide':
            print '<Battle> %s hides from %s...' %(self.pla.name, self.mon.name)
            self.log['player']['other'].append('hide')
            self.log['monster']['other'].append('find')
            
    def deathCheck(self):
        if self.mon.hp > self.php:
            # -- Monster wins
            self.dataclass.eh.RaiseEvent('OnDeath', 'Player died')
            print '<Battle> %s dies...' %self.pla.name
        elif self.mon.hp < self.php:
            # -- Player wins
            print '<Battle> %s kills %s' %(self.pla.name, self.mon.name)
            XpSystem().battlerun(self.mon, self.dataclass)
            self.loot()
        else:
            if self.log['player']['hits'][-1] > self.log['monster']['hits'][-1]:
                # -- Player wins
                print '<Battle> %s kills %s' %(self.pla.name, self.mon.name)
                XpSystem().battlerun(self.mon, self.dataclass)
                self.loot()
            elif self.log['player']['hits'][-1] < self.log['monster']['hits'][-1]:
                # -- Monster wins
                self.dataclass.eh.RaiseEvent('OnDeath', 'Player died')
                print '<Battle> %s dies...' %self.pla.name
                
    def loot(self):
        gold = self.mon.level*2.5+random.randint(0,self.mon.level)
        self.dataclass.data.inventory.add_gold(gold)
        print '<Battle> You loot', str(gold), 'Gold'
        print '<Battle> Current Gold:', self.dataclass.data.inventory.gold
        print '<Battle> You loot a item: %s' %itemsystems.ItemLoot(self.dataclass.data)
        self.dataclass.save()

class XpSystem():
    '''Handles xp gains and levelup's'''
    def __getitem__(self, arg):
        return self.max_xp(arg)
    
    def battlerun(self, unit, bootdata):
        '''Calculates xp gains'''
        # -- Monsters level
        monlvl = unit.level
        # -- Players Level
        melvl = bootdata.data.level
        # -- The xp the player gains
        xpgain = monlvl * random.randint(1, 5)
        xpgain *= melvl + (10/random.randint(1, 5))
        xpgain += random.randint(1, 10)
        # -- Give player the xp
        bootdata.data.xp += xpgain
        # -- Show player that he/she got xp
        print '<Battle> You gained %s xp' % str(xpgain)
        print '<Battle> You now have %s/%s xp' %(bootdata.data.xp, self[melvl])
        # -- Does Player Level Up?
        if bootdata.data.xp >= self[melvl]:
            bootdata.eh.RaiseEvent('OnLevelUp', 'Player gained a level')
            # -- Add the new level
            bootdata.data.level += 1
            # -- Reset XP
            bootdata.data.xp -= self[melvl]
            # -- Show player that he/she gained a level
            print '<Battle> You Gained A Level!!!'
            # -- Show Player his/her new level
            print '<Battle> You Are Now Level: %s' % str(bootdata.data.level)

    def max_xp(self, lvl):
        '''The maximum xp you can have if you are in level, <lvl>'''
        return int(conf.lvlupxp[lvl-1])
