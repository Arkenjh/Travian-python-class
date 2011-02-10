#! /usr/bin/python
# -*- coding: utf-8; -*- 
#



class Troop:
    
    def __init__(self):
        self.owner = ""
        self.village = ""
        self.type = ""
        
        self._attrs = []
        
    def update(self, data):
        for unit, number in data.items():
            self.__dict__[unit] = int(number)
            
            if unit not in self._attrs:
                self._attrs.append(unit)
    
    def add(self, unit, number):
        #print unit
        if unit in self.__dict__:
            self.__dict__[unit] += int(number)
        else:
            self.__dict__[unit] = int(number)
            self._attrs.append(unit)

    def getUnits(self):
        tmp = {}
        for unit in self._attrs:
            tmp[unit] = self.__dict__.get(unit)
        
        return tmp
    
    def __add__(self, troop):
        new_troop = Troop()
        new_troop.__dict__ = self.__dict__
        
        #for unit, number in self.getUnits().items():
        #    new_troop.add(unit, number)
        
        for unit, number in troop.getUnits().items():
            new_troop.add(unit, number)
            
        return new_troop
            
    
    def __repr__(self):
        out = "\n%s's troop from %s" % (self.owner, self.village)
        if self.type:
            out += "\n (%s)" % (self.type.upper())
            
        for unit in self._attrs:
            number = self.__dict__.setdefault(unit, 0)
            if number:
                out += "\n\t %s: %s" % (unit, number)
        
        return out
            