#!/usr/bin/python

class Missile:
    '''A one time effect'''
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target
        self.effect()
        
    def effect(self):
        pass
        
class Aura:
    '''A effect that last until canceled'''
    def __init__(self, target):
        '''Places aura on target'''
        self.holder = target
        self.holder.auras.append(self)
        self.create()
        
    def create(self):
        '''Here different variables can be set on holder'''
        pass
        
    def destroy(self):
        '''Here all custom variables on holder shall be removed'''
        
    def remove(self):
        '''Removes aura from holder'''
        del self.holder.auras[self.holder.auras.index(self)]
        self.destroy()

class Buff:
    '''A timed effect'''
    def __init__(self, caster, target):
        self.caster = caster
        self.target = target
        time = 1 #Time is in battle rounds
        
    def effect(self):
        pass

'''
Add racial spells below
|  |  |
\/ \/ \/
'''

'''<No Racials Yet>'''
'''</No Racials Yet>'''

'''
Add class spells below
|  |  |
\/ \/ \/
'''
'''<Mage>'''
class Fireball(Missile):
    def effect(self):
        self.target.hp -= random.randint(10*self.caster.level, 25*self.caster.level)
        
class Frostball(Missile):
    def effect(self):
        self.target.hp -= random.randint(7*self.caster.level, 24*self.caster.level)
'''</Mage>'''

'''<Priest>'''
class Holy_Smite(Missile):
    def effect(self):
        self.target.hp -= random.randint(5*self.caster.level, 27*self.caster.level)
        
class Agony(Missile):
    def effect(self):
        self.target.hp -= random.randint(1*self.caster.level, 28*self.caster.level)
'''</Priest>'''

'''<Shaman>'''
class Wrath(Missile):
    def effect(self):
        self.target.hp -= random.randint(4*self.caster.level, 28*self.caster.level)
        
class Poison_Ivy(Missile):
    def effect(self):
        self.target.hp -= random.randint(1*self.caster.level, 27*self.caster.level)
'''</Shaman>'''

'''<Warrior>'''
class Stab(Missile):
    def effect(self):
        self.target.hp -= random.randint(5*self.caster.level, 30*self.caster.level)
        
class Slash(Missile):
    def effect(self):
        self.target.hp -= random.randint(1*self.caster.level, 30*self.caster.level)
'''</Warrior>'''
