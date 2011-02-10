#! /usr/bin/python
# -*- coding: utf-8; -*- 
#



import sys
from TravianLogic import TravianLogic
from Config import Config

if __name__ == '__main__':

    cfg = Config()
    travian = TravianLogic(cfg)
    
    
    if not travian.connect():
        print 'Invalid username or password'
        sys.exit()

    travian.update()

    #html = open("./cache/build39.html", "r").read()
    #rally_point = travian.parser.parse(html)
    
    #print travian.parser.getRallyPoint(rally_point)
