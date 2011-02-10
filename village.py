#!/usr/bin/python
# -*- coding: utf-8; -*- 
#

class Building:
    def __init__(self, id):
        self.id = id
        self.name = ""
        self.level = 0
        
    def update(self, **args):
        for k,v in args.items():
            if k in self.__dict__:
                self.__dict__[k] = v
                
    def __repr__(self):
        o = "%s (%s)\n" % (self.name, self.level)
        return o                
        
        
class Village:
    def __init__(self):
        
        self.name = ""
        
        self.buildings = {}
        self.resources = Resources()
        self.farms = None
        
        for x in range(1, 41):
            id = self.getBuildId(x)
            if id not in self.buildings:
                self.buildings[id] = Building(id)
    
    def getBuildId(self, num):
        return "b_%s" % (num)
        
    def updateBuilding(self, num, **args):
            id = self.getBuildId(num)
            if id in self.buildings:
                self.buildings[id].update(**args)
            
    def __repr__(self):
        o = "main\n"
        
        ids = self.buildings.keys()
        
        o += "Fields:\n"
        for x in range(1, 20):
            id = self.getBuildId(x)
            building = self.buildings.get(id) 
            o += "\t (%s) %s" % (x, building.__repr__())
        
        o += "\n"
        o += "Buildings:\n"
        for x in range(20, 41):
            id = self.getBuildId(x)
            building = self.buildings.get(id) 
        
            if building.level:
                o += "\t (%s) %s" % (x, building.__repr__())                

        o += "\n"
        o += "Resources:\n"
        o += self.resources.__repr__()
        
        return o  

            
class Res:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.production = 0
        self.value = 0
        self.capacity = 0

    def update(self, **args):
        if "production" in args:
            self.production = int(args.get("production"))
        if "value" in args:
            self.value = int(args.get("value"))
        if "capacity" in args:
            self.capacity = int(args.get("capacity"))
            
    def __repr__(self):
        o = "%s: (%s/h) %s/%s\n" % (self.name, self.production, self.value, self.capacity)
        return o
        
class Resources:
    def __init__(self):
        self.ids = {
            "l1":"wheat", "l2":"iron", "l3":"clay", "l4":"wood"
        }
        
        self.wood = None
        self.clay = None
        self.iron = None
        self.wheat = None
        
        for id, res in self.ids.items():
            if res in self.__dict__:
                self.__dict__[res] = Res(id, res)
        
    def update(self, id, **args):
        attr = self.ids.get(str(id))
        if attr in self.__dict__:
            self.__dict__[attr].update(**args)
            
    def __repr__(self):
        o = ""
        for id, res in self.ids.items():
            if res in self.__dict__:
                o += "\t" + self.__dict__[res].__repr__()
                
        return o                