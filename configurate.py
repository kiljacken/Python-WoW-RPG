import ConfigParser, re, os

try: os.chdir(os.path.dirname(__file__))
except: pass

def StatParser(stats):
        amount = r'''([0-9\-]+)'''
        types = r'''(\S+)\.(\S+)'''
        res = re.compile(amount+types)
        results = {}
        result = res.search(stats).groups()
        results['amount'] = result[0]
        results['what'] = result[1]
        results['type'] = result[2]
        return results

def runalgorithm():
    tmp = [int(config.get('xp', 'firstx'))]
    x = int(config.get('xp', 'firstx'))
    for g in range(int(config.get('xp', 'maxlvl'))):
        exec('x = %s' %config.get('xp', 'algorithm'))
        tmp.append(x)
    return tmp

class Spellbook:
    '''A Wrapper for the spellbook.ini file'''
    def __init__(self, wclass):
        self.config = ConfigParser.ConfigParser()
        self.config.read('spellbook.ini')
        self.wclass = wclass
        self.spells = self.config.get(self.wclass, 'spells').split(',')
        self.spelldata = self.config.get(self.wclass, 'spldat').split(',')
        
    def getspell(self, spell):
        '''Gets a spell for classes spellbook'''
        if spell in self.spells:
            return StatParser(self.spelldata[self.spells.index(spell)])
        else:
            return self.default
    
    @property   
    def default(self):
        '''Returns the default spell'''
        return self.getspell(self.config.get(self.wclass, 'default'))

# -- Open The INI file
config = ConfigParser.ConfigParser()
config.read('data.ini')
# -- Extract data from INI file
races = config.get('lists', 'races').split(',')
classes = config.get('lists', 'classes').split(',')
genders = config.get('lists', 'genders').split(',')
lvlupxp = runalgorithm()

if __name__ == '__main__':
    print Spellbook('Mage').default
    print lvlupxp
