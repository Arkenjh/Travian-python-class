#!/usr/bin/python
# -*- coding: utf-8; -*- 
#


class Config(object):
    def __init__(self, **args):
        #Some default settings
        self.servername = 'speed.travian.us'
        self.username = 'angelow'
        self.password = '15021988'
        self.rect = [0,7,0,7]
        self.ThreadNum = 32
        self.RetryNum = 5
        self.ReLogin = False
        #Output mask for [Village, farm, oasis]
        self.Output = [True,True,True]
        self.ServerScale = 400
        self.log = False
        
class OptionException(Exception):
    def __init__(self,info):
        self.info = info
    def __str__(self):
        return repr(self.info)
