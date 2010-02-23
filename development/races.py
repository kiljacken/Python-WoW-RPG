#!/usr/bin/python
class Race:
    '''A playable race'''
    def __init__(self):
        self.classes = [] # -- The classes avaible for the race
        self.racial_hp = 100 # -- The race's racial hp (player hp = racial hp * player level (+ bonuses))
        self.racial_abilities = [] # -- The race's racial abilities
        
    def can_have_class(self, _class):
        '''checks if the race can be class: class'''
        return _class in self.classes

'''
Add races below
|  |  |
\/ \/ \/
'''

class Dwarf(Race):
    def __init__(self):
        Race.__init__(self)
        self.classes = ['Mage', 'Priest', 'Warrior']
        self.racial_hp = 110

class Human(Race):
    def __init__(self):
        Race.__init__(self)
        self.classes = ['Mage', 'Priest', 'Warrior']
        self.racial_hp = 90

class Elf(Race):
    def __init__(self):
        Race.__init__(self)
        self.classes = ['Mage', 'Priest']
        
class Orc(Race):
    def __init__(self):
        Race.__init__(self)
        self.classes = ['Mage', 'Shaman', 'Warrior']
        self.racial_hp = 110
        
        
class Goblin(Race):
    def __init__(self):
        Race.__init__(self)
        self.classes = ['Mage', 'Shaman', 'Warrior']
        self.racial_hp = 90
        
class Undead(Race):
    def __init__(self):
        Race.__init__(self)
        self.classes = ['Mage', 'Warrior']
        
