#!/usr/bin/python
class CreationSkill:
    def __init__(self, player):
        self.player = player
        self.skill = 0
        self.takes = [[None, 0],] # -- [[item, amount],...]
        self.gives = [None, 0] # -- [item, amount]
        
    def make(self):
        succes = True
        taken = []
        for a in self.takes:
            item = self.player.inventory.take_item(a[0], a[1])
            if item:
                taken.append(item)
            else:
                print 'You haven\'t got enough %s!!!' %str(a)
                succes = False
        if succes:
            self.player.inventory.add_item(self.gives[0], self.gives[1])
            print str(self.gives[1])+'x'+str(self.gives[0].name)+' created!!!'
        else:
            for a in taken:
                self.player.inventory.add_item(a[0], a[1])
        return succes
        
class Profession:
    def __init__(self):
        self.creations = {} # -- Put children of the CreationSkill class here {Name: class}
        self.skill = 0
        self.maxskill = 450
        
    def create(self, what, player):
        creation = self.creations[what](player)
        if self.skill => creation.skill:
            creation.make()
            a = True
        else:
            print 'Skill level not high enough!!!'
            a = False
        if a:
            if self.skill != maxskill:
                self.skill += 1
        return a
