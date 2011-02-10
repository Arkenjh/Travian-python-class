#!/usr/bin/python
# -*- coding: utf-8; -*- 
#

from TravianClient import TravianClient
from TravianParser import TravianParser
from village import Village, Resources
from units import Troop

class TravianLogic:
    
    def __init__(self, config):
        
        self.resources = Resources()
        self.Village = Village()
        
        self.parser = TravianParser()
        self.tclient = TravianClient(config)
        
        self.conn = False
        
    def connect(self):
        self.conn = self.tclient.login()
        
        return self.conn

    def update(self):
        if not self.conn:
            return False
        
        # FIELDS
        html = self.tclient.get("dorf1.php")
        dorf1 = self.parser.parse(html)
        
        # VILLAGE BUILDINGS
        html = self.tclient.get("dorf2.php")
        dorf2 = self.parser.parse(html)
        
        # PROFILE
        uid = self.parser.getProfileUid(dorf1)
        html = self.tclient.get("spieler.php?uid=%s" % (uid))
        profile = self.parser.parse(html) 
        
        ### RALLY POINT
        html = self.tclient.get("build.php?id=39")
        rally_point = self.parser.parse(html)
            
        
        village_name = self.parser.getVillageName(dorf1)
        server_time, calculated = self.parser.getServerTime(dorf1)
        
        res = self.parser.getRes(dorf1)
        troops = self.parser.getTroops(dorf1)
        movements = self.parser.getMovements(dorf1)
        
        
        fields = self.parser.getFields(dorf1)
        for field in fields:
            id, name, level = field
            self.Village.updateBuilding(id, name=name, level=level)            
        
        buildings = self.parser.getVillageBuildings(dorf2)
        for build in buildings:
            id, name, level = build
            self.Village.updateBuilding(id, name=name, level=level)
        
        villages = self.parser.getVillages(profile)
        

        
        print self.Village

        mega_troop = Troop()
        mega_troop.owner = "angelow"        
        
        my, reinf, prisoners = self.parser.getRallyPoint(rally_point)
        for village, troops in my.items():
            t = Troop()
            t.village = village
            t.owner = "myself"
            
            t.update(troops)
            print t
            mega_troop += t
            
        for owner, data in reinf.items():
            for village, troops in data.items():
                t = Troop()
                t.village = village
                t.owner = owner
                t.type = "deff"
                t.update(troops)

                
                print t                
                mega_troop += t
            
        for owner, data in prisoners.items():
            for village, troops in data.items():
                t = Troop()
                t.village = village
                t.owner = owner
                t.type = "prisoners"
                t.update(troops)

                print t          
                mega_troop += t
        
        mega_troop.owner = "angelow"
        mega_troop.village = village_name
        mega_troop.type = "all units"
        print mega_troop
        

        
        
            

        
        
        
        
        return True        