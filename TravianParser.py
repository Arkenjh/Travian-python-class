#!/usr/bin/python
# -*- coding: utf-8; -*- 
#


import re

from HTMLParser import HTMLParser

from lxml import etree
from StringIO import StringIO
from lxml.html import fromstring



class TravianParser:
    
    def __init__(self):
        
        self.res = re.compile('<td id="l([1-4]+)" title="([0-9]+)">([0-9]+)/([0-9]+)</td>')
        self.build = re.compile('build.php\?id=([0-9]+)')
        self.profile = re.compile('spieler.php\?uid=([0-9]+)')
        self.building = re.compile('([a-zA-Z ]+) level ([0-9]+)')
        self.movements = re.compile("([0-9]+)([a-zA-Z.]+)in([0-9\:]+)Hrs")
        self.coords = re.compile("\(([0-9\-]+)\|([0-9\-]+)\)")

        self.parser = etree.HTMLParser()

    def parse(self, html):        
        #return etree.parse(StringIO(html), self.parser)
        return fromstring(html)


    def getRallyPoint(self, doc):

        persons = {}
        
        my = {}
        renforcement = {}
        prisoners = {}
        

        for table in doc.cssselect("table.troop_details"):
                    
            village, owner = [a.text_content() for a in table.cssselect("thead td a")]
            tr = [tr for tr in table.cssselect('tbody.units tr')]
            names = [img.get("title") for img in tr[0].cssselect('td img')]
            units = [td.text_content() for td in tr[1].iter(tag="td")]
                
            troops = {}
            
            for name, number in zip(names, units):
                if name not in troops:
                    troops[name] = int(number)
                    
                                    
            if owner == "Own troops":
                my[village] = troops
            elif "Troops imprisoned from" in owner:
                owner = owner.replace("Troops imprisoned from ", "").strip()
                if not owner in prisoners:
                    prisoners[owner] = {}
                    
                prisoners[owner][village] = troops
            else:
                owner = owner.replace("'s troops", "").strip()
                if not owner in renforcement:
                    renforcement[owner] = {}
                                    
                renforcement[owner][village] = troops

        
        return [my, renforcement, prisoners]


    # spieler.php?uid=xxx ONLY !
    def getVillages(self, doc):
        villages = []
        
        table = doc.get_element_by_id("villages")
        for tr in table.iter(tag="tr"):
            name, coords, population = "", "", ""
            for td in tr.iter(tag="td"):
                if "class" in td.attrib:
                    cl = td.get("class")
                    
                    if cl == "nam":
                        name = td.text_content()
                        
                    elif cl == "hab":
                        population = td.text_content()
                    elif cl == "aligned_coords":
                        text = td.text_content().replace("\n", "").replace("\t", "")
                        coords = self.coords.findall(text)[0]
        
            if name and population and coords:
                villages.append([name, population, coords])
                     
        return villages
    
    
    # ALL PAGES !
    def getProfileUid(self, doc):
        uid = 0
        
        div = doc.get_element_by_id("side_navi")
        for a in div.iter(tag="a"):
            href = a.get("href")
            
            if self.profile.match(href):
                uid = self.profile.findall(href)[0]

        return uid

    ### ALL PAGES !
    def getRes(self, doc):
        
        res = []
        
        div_res = doc.get_element_by_id("resWrap")    
        for td in div_res.iter(tag='td'):
            title = td.get('title')
            id = td.get('id')
            text = td.text_content()
        
            if id in ["l1", "l2", "l3", "l4"]:
                current, capacity = text.split("/")
                res.append([id, int(title), int(current), int(capacity)])
                #self.Village.resources.update(id, production=int(title), value=int(current), capacity=int(capacity))
        
        return res
    
    
    ### dorf1.php ONLY !
    def getTroops(self, doc):
        troops = []
        try:
            div_troops = doc.get_element_by_id("troops")
            for tr in div_troops.iter(tag="tr"):
                unit_name, unit_number = "", ""
                for td in tr.iter(tag="td"):
                    if "class" in td.attrib:
                        cl = td.get("class")
                        if cl == "num":
                            unit_number = td.text_content()
                        elif cl == "un":
                            unit_name = td.text_content()
                    
                    if unit_name and unit_number:
                        troops.append([unit_name, unit_number])        
                        
        except:
            return []
        else:
            return troops        

    ### dorf1.php ONLY !
    def getFields(self, doc):
        fields = []
        
        div = doc.get_element_by_id("rx")    
        for area in div.iter(tag='area'):
            title = area.get("title")
            href = area.get("href")
            farm, level, id = "", 0, 0
            
            if self.building.match(title):
                farm, level = self.building.findall(title)[0]
            if self.build.match(href):
                id = self.build.findall(href)[0]

            if farm and level and id:
                fields.append([id, farm, level])
            
        return fields
    
    
    ### dorf1.php ONLY !
    def getMovements(self, doc):

        try:
            table = doc.get_element_by_id("movements")
        except KeyError:
            return []
        else:
            move = []
            for tr in table.iter(tag="tr"):
                href, type, time, number = "", "", "", 0
                
                for link in tr.iter(tag="a"):
                    if "href" in link.attrib:
                        href = link.get("href")
                
                for td in tr.iter(tag="td"):
                    text = str(td.text_content()).encode('ascii', 'ignore')
                    if len(text) > 2:
                        if self.movements.match(text):
                            number, type, time = self.movements.findall(text)[0]
                            if type == "Reinf.":
                                type = "reinforcing"
                            move.append([type, number, time, href])
                            
            return move
    
        
    ### dorf2.php ONLY !
    def getVillageBuildings(self, doc):
        buildings = []
        
        map = doc.get_element_by_id("map2")
        for area in map.iter(tag='area'):
            title = area.get('title')
            href = area.get('href')
            build_id, name, level, = "", "", 0
            
            if title and href:
                if self.build.match(href):
                    build_id = self.build.findall(href)[0]
                    
                if self.building.match(title):
                    name, level = self.building.findall(title)[0]                    
                    
                buildings.append([build_id, name, level])                
                #self.Village.updateBuilding(build_id, name=name, level=level)
                
        return buildings
    
    ### ALL PAGES ! 
    def getVillageName(self, doc):
        name = ""
        
        for h1 in doc.iter(tag='h1'):
            title = h1.text_content()
            if title:
                name = title
                
        return name

    ### ALL PAGES !
    def getServerTime(self, doc):
        server_time = ""
        calculated = ""            
        div_time = doc.get_element_by_id("ltimeWrap")
        tmp = div_time.text_content()
        
        for line in tmp.split("\n"):
            line = line.strip()
            if line is not "":
                if "Server time" in line:
                    server_time = line
                elif "am" in line or "pm" in line:
                    server_time += " %s" % line
                elif "Calculated" in line:
                    calculated = line
                    
        return [server_time, calculated]            
                        

        

        

        
                