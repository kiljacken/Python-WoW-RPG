from random import choice, randint
from engine import Item, Player
import battle

# -- Don't delete!! It is very important!!
dummy = Player("dummy")

class Generate:
    def __init__(self):
        self.prefixes = ['Bloody', 'Dirty', 'Shiny', 'Evil']
        self.suffixes = ['Of Pain', 'Of Doom', 'Of Chaos', 'Of Light']
        self.weapons = ['Sword', 'Dagger', 'Staff', 'Hammer']
        self.armors = ['Cloak', 'Chain Mail', 'Plate Mail', 'Scale Mail', 'Leather Jacket']
        self.shields = ['Buckler', 'Targe', 'Large Shield', 'Barrel Lid', 'Tortoise Shell']
        self.trinkets = ['Tooth', 'Skull', 'Spine', 'Rune', 'Carrot', 'Potato']
        
    def weapon(self):
        # -- Make a name
        name = choice(self.prefixes)
        name += ' '+choice(self.weapons)+' '
        name += choice(self.suffixes)
        # -- Make some damage
        min = randint(0,20)
        max = randint(min+1, 40)
        # -- Calculate Price
        price = 0
        price += round(((min+max)/2)*12.5)
        q = price
        q /= max-min
        price += round(q)
        # -- Make Stats string
        stats = str(min)+'-'+str(max)+battle.dam().random()
        return Item(name, price, stats, 1, 'weapon')
        
    def armor(self):
        # -- Make a name
        name = choice(self.prefixes)
        name += ' '+choice(self.armors)+' '
        name += choice(self.suffixes)
        # -- Roll the armor points
        armor = randint(1, 250)
        # -- Calculate the price
        price = 0
        price += armor*10
        q = price
        q /= armor
        price += round(q)
        # -- Make Stats string
        stats = str(armor)+battle.bon()['arm']
        return Item(name, price, stats, 1, 'armor')
        
    def shield(self):
        # -- Make a name
        name = choice(self.prefixes)
        name += ' '+choice(self.shields)+' '
        name += choice(self.suffixes)
        # -- Roll the armor points
        armor = randint(1, 150)
        # -- Calculate the price
        price = 0
        price += armor*10
        q = price
        q /= armor
        price += round(q)
        # -- Make Stats string
        stats = str(armor)+battle.bon()['arm']
        return Item(name, price, stats, 1, 'shield')
        
    def trinket(self):
        # -- Make a name
        name = choice(self.prefixes)
        name += ' '+choice(self.trinkets)+' '
        name += choice(self.suffixes)
        # -- Roll the armor points
        bonus = randint(1, 50)
        # -- Calculate the price
        price = 0
        price += bonus*15
        q = price
        q /= bonus
        price += round(q)
        # -- Make Stats string
        stats = str(bonus)+battle.bon().random()
        return Item(name, price, stats, 1, 'trinket')
        
def ItemLoot(player):
    typech = choice(['weapon', 'armor', 'shield', 'trinket'])
    item = eval("Generate().%s()" %typech)
    player.inventory.add_item(item)
    return item

class Store:
    def __init__(self, player):
        self.items = [ItemLoot(dummy) for e in range(randint(4, 16))]
        self.player = player
        
    def run(self):
        print '\n'*25
        print 'Welcome to Ye Olde Shop'
        cmd = raw_input('Do you want to buy or sell? ')
        while cmd != 'exit':
            if cmd == 'buy':
                print '\n'*25
                self.buy_display()
            elif cmd == 'sell':
                print '\n'*25
                self.sell_display()
            else:
                break
            print 'Welcome to Ye Olde Shop'
            cmd = raw_input('Do you want to buy or sell? ')
                
    def buy_display(self):
        print '#'*5+'Ye Olde Shop'+'#'*5
        i = 1
        for item in self.items:
            print '(%s) %s'%(str(i), item)
            i += 1
        cmd = raw_input('What do you want to buy (type exit to exit)? ')
        try:
            if type(int(cmd)) == type(1):
                self.buy(self.items.pop(int(cmd)-1))
            else:
                print "\n"*25
        except:
            print "\n"*25
    
    def sell_display(self):
        print '#'*5+'Ye Olde Shop'+'#'*5
        i = 1
        if self.player.inventory.items.keys():
            for item in self.player.inventory.items.keys():
                print '(%s) %s'%(str(i), self.player.inventory.get_item(item))
                i += 1
            cmd = raw_input('What do you want to sell (type exit to exit)? ')
            try:
                if type(int(cmd)) == type(1):
                    self.sell(self.player.inventory.get_item(self.player.inventory.items.keys()[int(cmd)-1]))
                else:
                    print "\n"*25
            except:
                print "\n"*25
        
    def buy(self, item):
        if self.player.inventory.gold < item.price:
            print 'You can\'t afford that!'
        else:
            self.player.inventory.take_gold(item.price)
            self.player.inventory.add_item(item)
            print 'Item bought!!'
        print "\n"*25
        self.buy_display()
    
    def sell(self, item):
        item = self.player.inventory.take_item(item.name)
        self.player.inventory.add_gold(item.price)
        print 'Item sold!!'
        print "\n"*25
        self.sell_display()
    
def test():
    pla = Player('Kurt')
    pla.inventory.gold = 1000
    e = Generate()
    print e.weapon()
    print e.armor()
    print e.shield()
    print e.trinket()
    print ItemLoot(pla)
    a = Store(pla)
    a.run()
    
if __name__=='__main__':
    test()
    a = Store(dummy)
