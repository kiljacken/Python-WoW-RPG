import time, os

try: os.chdir(os.path.dirname(__file__))
except: pass

def elog(arg):
    try: prelog = open('events.log').read()
    except: prelog = ''
    logg = open('events.log', 'w')
    logg.write(prelog+time.asctime(time.localtime())+': '+arg+'\n')

class EventSystem(object):
    def __init__(self):
        self.events = {} # -- {'eventName':['func1', 'func2']}
        
    def RegisterEvent(self, name):
        elog('Registering event: %s'%name)
        self.events[name] = []
        
    def AddCallToEvent(self, event, name):
        # -- name is the function name AS A STRING (func.__name__)
        if event in self.events.keys():
            if not name in self.events[event]: 
                elog('Adding call: %s, To event: %s'%(name,event))
                self.events[event].append(name)
            else: elog('That event already has that call!')
        else: elog('That event does not exist, please register it with RegsisterEvent')
        
    def RaiseEvent(self, event, data=''):
        if event in self.events.keys():
            if self.events[event]:
                for a in self.events[event]:
                    elog('Raising event: %s, With data: %s'%(event,data))
                    a(data)
            else: elog('Please add some calls to that event before raising it!')
        else: elog('That event does not exist, please register it with RegsisterEvent')

def echo(arg):
    print arg

def main():
    try: os.remove('events.log')
    except: pass
    a = EventSystem()
    a.RegisterEvent('OnExit')
    a.AddCallToEvent('OnExit', echo)
    a.RaiseEvent('OnExit', 'Event')
    
if __name__=='__main__': main()
