'''
PyWowRpg -- A Python, text based RPG inspired by WoW...
Author: Emil Lauridsen

Licensed under the GNU GPL,
Full License is included in gpl-3.0.txt
'''
import pickle, random, time, sys, os
#import maplib
import configurate as conf
import re
import events
import battle
import itemsystems

try: os.chdir(os.path.dirname(__file__))
except: pass

def log(arg):
    try: prelog = open('game.log').read()
    except: prelog = ''
    logg = open('game.log', 'w')
    logg.write(prelog+time.asctime(time.localtime())+': '+arg+'\n')

########################################################################
#                                                                      #
#  Data classes & Functions                                            #
#                                                                      #
########################################################################

class Monster:
    '''Class holding the data of a monster'''
    def __init__(self, name, hep, dmg, level):
        # -- dmg = [min, max]
        self.name = name
        self.hp = hep * level
        self.mindmg = dmg[0]
        self.maxdmg = dmg[1]
        self.level = level
        
    def roll_damage(self):
        '''Rolls the monsters Damage'''
        return random.randint(self.mindmg, self.maxdmg)*self.level
    
    @property    
    def get_health(self):
        '''Returns the monsters health'''
        return self.hep
 
class Stats(object):
    '''Used to store a player's stats'''
    def __init__(self):
        self.stats = {'str':0, 'agi':0, 'sta':0, 'spi':0, 'int':0}
        self.item_stats = {'str':0, 'agi':0, 'sta':0, 'spi':0, 'int':0}
        self.armor = 0
        
    @property
    def get_stats(self):
        '''Returns the stats'''
        return self.stats
        
    @property
    def get_armor(self):
        '''Returns the armor'''
        return self.armor

class Item(object):
    '''This class contatains a item'''
    def __init__(self, name, price, stats, stack, tpe):
        self.name = str(name)
        self.price = int(price)
        self.stats = str(stats)
        self.stack = int(stack)
        self.type = str(tpe)
        
    def make(self, lst):
        '''Generates a item from a list of data'''
        self.name = str(lst[0])
        self.price = int(lst[1])
        self.stats = str(lst[2])
        self.stack = int(lst[3])
        self.type = str(lst[4])
        
    def __repr__(self):
        return '[ %s, Price: %sg, Stats: %s ]' % (self.name, self.price,
                '%s %s %s' %(self.pstats['amount'], self.pstats['what'],
                self.pstats['type']))
    
    @property    
    def pstats(self):
        '''Returns an items parsed stats'''
        return statparser(self.stats)
        
def statparser(stats):
    '''Returns a set of parsed stats'''
    amount = r'''([0-9\-]+)'''
    types = r'''(\S+)\.(\S+)'''
    res = re.compile(amount+types)
    results = {}
    result = res.search(stats).groups()
    results['amount'] = result[0]
    results['what'] = result[1]
    results['type'] = result[2]
    return results

class Player:
    '''The player class'''
    def __init__(self, name):
        global rusty_sword
        self.level = 1
        self.name = name
        self.race = 0
        self.wclass = 0
        self.gender = 0
        self.xp = 0
        self.inventory = inventory()
        self.inventory.add_item(starter_item)
        self.inventory.equip('Rusty Knife')
    
    @property
    def player_class(self):
        '''Returns the players class as a string'''
        return conf.classes[self.wclass]
        
    @property
    def player_race(self):
        '''Returns the players race as a string'''
        # -- Returns the players race as a string
        return conf.races[self.race]
        
    @property
    def player_gender(self):
        '''Returns the players gender as a string'''
        # -- Returns the players gender as a string
        return conf.genders[self.gender]

    def save(self):
        '''Saves character to a file'''
        # -- Saves character to a file
        file = open('./save/%s.sav' % self.name, 'w')
        pickle.dump(self, file)
        file.close()

    def load(self):
        '''Loads character data from a file'''
        #-- Loads character data from a file
        file = open('./save/%s.sav' % self.name, 'r')
        pkd = pickle.load(file)
        file.close()
        self.set(pkd)
        
    def set(self, ins):
        '''Used with load to load the loaded data into the class'''
        # -- Used with load to load the loaded data into the class
        self.race = ins.race
        self.wclass = ins.wclass
        self.level = ins.level
        self.xp = ins.xp
        self.inventory = ins.inventory
        self.spell = conf.Spellbook(self.player_class)
        
    def make_from_list(self, lst):
        '''Used to load char data from a list'''
        # -- Used to load char data from a list
        # ?? [class, race, gender, level, experience]
        self.wclass = lst.pop(0)
        self.race = lst.pop(0)
        self.gender = lst.pop(0)
        self.level = lst.pop(0)
        self.xp = lst.pop(0)
        self.spell = conf.Spellbook(self.player_class)
        
    def roll_damage(self):
        damage = self.inventory.equipped['weapon'].pstats['amount'].split('-')
        dmg = random.randint(int(damage[0]), int(damage[1])) * self.level
        if self.inventory.has_equip('trinket'):
            if self.inventory.equipped['trinket'].pstats['what'] == 'damage':
                dmg += int(self.inventory.equipped['trinket'].pstats['amount'])
        return dmg

        
    def spell_damage(self, name):
        #try:
        damage = self.spell.getspell(name)['amount'].split('-')
        return random.randint(int(damage[0]), int(damage[1])) * self.level
        #except:
        #    return self.roll_damage()
            
    def get_hp(self):
        php = self.level * 100 + self.level
        if self.inventory.has_equip('trinket'):
            if self.inventory.equipped['trinket'].pstats['what'] == 'health':
                php += int(self.inventory.equipped['trinket'].pstats['amount'])
        return php
        
    def get_armor_reduction(self):
        arm = 0
        if self.inventory.has_equip('armor'):
            if self.inventory.equipped['armor'].pstats['what'] == 'armor':
                arm += int(self.inventory.equipped['armor'].pstats['amount'])
        if self.inventory.has_equip('shield'):
            if self.inventory.equipped['shield'].pstats['what'] == 'armor':
                arm += int(self.inventory.equipped['shield'].pstats['amount'])
        if self.inventory.has_equip('trinket'):
            if self.inventory.equipped['trinket'].pstats['what'] == 'armor':
                arm += int(self.inventory.equipped['trinket'].pstats['amount'])
        armor = float(arm-300)/2
        if armor < 0:
            return 0
        else:
            return armor

        
        
        
class inventory:
    '''The Inventory'''
    def __init__(self):
        self.items = {}
        self.equipped = {'weapon': None,
                        'armor': None,
                        'shield': None,
                        'trinket': None}
        self.amount = {}
        self.gold = 0
    
    def add_item(self, item, amount=1):
        '''Add an item'''
        if item.name in self.items.keys():
            if self.amount[item.name] <= item.stack:
                self.amount[item.name] += amount
            else:
                pass
        elif item.name not in self.items.keys():
            self.items[item.name] = item
            self.amount[item.name] = amount
            
    def get_item(self, name):
        '''Get an items data from inventory'''
        if self.items.has_key(name):
            return self.items[name]
    
    def take_item(self, name, amount=1):
        if self.items.has_key(name):
            item = self.items[name]
            if self.amount[name] > 1:
                self.amount[name] -= amount
            else:
                del self.items[name]
                del self.amount[name]
        else:
            return False
        return item
            
    def add_gold(self, amount):
        '''Add gold from inventory'''
        self.gold += amount
        
    def take_gold(self, amount):
        '''Take gold from inventory'''
        self.gold -= amount
    
    def equip(self, name):
        type = self.items[name].type
        if self.equipped[type]:
            self.unequip(type)
            self.equipped[type] = self.take_item(name)
        else:
            self.equipped[type] = self.take_item(name)
            
    def unequip(self, type):
        if self.equipped[type]:
            item = self.equipped[type]
            self.equipped[type] = None
            self.add_item(item)
        else:
            pass
    
    def has_equip(self, slot):
        return self.equipped[slot]
            
class Equipper:
    def __init__(self, player):
        self.pla = player
        
    def run(self):
        while True:
            print '#'*5+'Inventory'+'#'*5
            i = 1
            if self.pla.inventory.items.keys():
                for item in self.pla.inventory.items.keys():
                    print '(%s) %s'%(str(i), self.pla.inventory.get_item(item))
                    i += 1
            else:
                print 'You have no items to equip!!'
                break
            item = raw_input("Which item do you want to equip? ")
            if type(cmd) == type(""):
                if cmd == "exit": break
                else: print "Please enter a number"
            else:
                self.pla.inventory.equip(self.pla.inventory.items.keys()[int(item)-1])
            break
            
        
                
# -- Static Items
# --                    name       price    stats             stacks    type
starter_item = Item('Rusty Knife', 0,     '1-11melee.damage', 1,      'weapon')

########################################################################
#                                                                      #
#  Game classes                                                        #
#                                                                      #
########################################################################

class game():
    '''The class loading the game'''
    def __init__(self, glog=log):
        # -- self.tclass is a list of Classes
        # -- self.races is a list of Races
        # -- self.gender is a list of Genders
        # -- self.data is a placeholder for character data
        self.tclass = conf.classes
        self.races = conf.races
        self.gender = conf.genders
        self.data = None
        self.log = glog
        self.register_events()
    
    def register_events(self):
        self.eh = events.EventSystem()
        self.eh.RegisterEvent('OnCombat')
        self.eh.RegisterEvent('CombatEvent')
        self.eh.RegisterEvent('OnDeath')
        self.eh.RegisterEvent('OnLevelUp')
        self.eh.AddCallToEvent('OnCombat', self.log)
        self.eh.AddCallToEvent('CombatEvent', self.log)
        self.eh.AddCallToEvent('OnDeath', self.log)
        self.eh.AddCallToEvent('OnLevelUp', self.log)
    
    def ask(self):
        '''Ask if user has a character'''
        # -- Now we ask the user if he/she has a character
        yn = raw_input('Do you have a character?: ')
        y = ['y', 'Y', 'Yes', 'yes']
        n = ['n', 'N', 'No', 'no']
        if yn in y:
            self.load()
        elif yn in n:
            self.create()
        else:
            print '%s, is not a yes or a no' % yn
            sys.exit()

    def load(self):
        '''Used to load a character'''
        print 25 * '\n'
        chn = raw_input('Name of saved character: ')
        # -- chd is list with all character data
        # ?? [class, race, gender, level, experience]
        self.data = Player(chn)
        self.data.load()
        print 25 * '\n'

    def create(self):
        '''Used to create a character'''
        print 25 * '\n'
        print 'You don\'t need to capitalize the game does it for you'
        chn = raw_input('Character name: ')
        chc = raw_input('Class: ').capitalize()
        chra = raw_input('Race: ').capitalize()
        chg = raw_input('Gender: ').capitalize()
        self.chfn = './save/'+ chn +'.sav'
        # -- cc is class, sr is race, cg is gender
        # -- cl is level, cxp is experience,
        # -- cdl is list with all character data:
        
        cc = self.tclass.index(chc)
        cr = self.races.index(chra)
        cg = self.gender.index(chg)
        cl = 1
        cxp = 0
        cdl = [cc, cr, cg, cl, cxp]
        self.data = Player(chn)
        self.data.make_from_list(cdl)
        self.data.save()
        print 25 * '\n'

    def save(self):
        '''Saves the current Game'''
        self.log('Saving Game')
        self.data.save()

if __name__ == '__main__':
    gamec = game()
    gamec.ask()
    print '\n'*25
    print 'Welcome to pythonwow-rpg!'
    while True:
        cmd = raw_input('Command >>> ')
        if cmd == 'help':
            print 'Commands:'
            print '<> battle - begins a battle'
            print '<><> hit - hits the enemy in a battle'
            print '<><> spell - cast a spell on the enemy in a battle'
            print '<><> hide - you hide from the enemy in a battle'
            print '<><> flee - you flee from the battle'
            print '<> equip - enter the equipment menu'
            print '<> shop - enter the store'
            print '<> exit - save and exit the game'
        elif cmd == 'battle':
            b = battle.BattleBackend(Monster('Ogre', 100, [1, 10], gamec.data.level), gamec)
            b.start()
        elif cmd == 'equip':
            e = Equipper(gamec.data)
            e.run()
            gamec.save()
        elif cmd == 'shop':
            s = itemsystems.Store(gamec.data)
            s.run()
            gamec.save()
        elif cmd == 'exit':
            gamec.save()
            exit(0)
        else:
            print '"%s" is not a valid command' %cmd
            print 'Write "help" for a list of avaible commands'
