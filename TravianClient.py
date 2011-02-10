#!/usr/bin/python
# -*- coding: utf-8; -*- 
#


import codecs
import os.path
import urllib
import urllib2
import cookielib

import os
import random
import hashlib





		
		
class TravianClient(object):
	def __init__(self, config):
		object.__init__(self)
		

		self.cache = "/home/angelo/workspace/foure-tout/src/travian/cache"
		self.COOKIEFILE = 'travian.cookie'
		self.cj = cookielib.LWPCookieJar()
	
		if os.path.isfile(self.COOKIEFILE):
			print "cookie!"
			self.cj.load(self.COOKIEFILE)

		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(opener)
		
		self.config =  config
		
		self.txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT)'}



	def getValue(self, html, start, end):
	    ind1 = html.find(start) + len(start)
	    ind2 = html[ind1:].find(end) + ind1
	    value = html[ind1:ind2]
	    #print "%s:%s" % (ind1, ind2)
	
	    return value
		
	def login(self):
		theurl = 'http://speed.travian.us/login.php'
		txdata = None

		#get login page and form item names
		try:
			req = urllib2.Request(theurl, txdata, self.txheaders)			
			handle = urllib2.urlopen(req)
		except IOError, e:
			print 'We failed to open "%s".' % theurl
			if hasattr(e, 'code'):
				print 'We failed with error code - %s.' % e.code
			elif hasattr(e, 'reason'):
				print "The error object has the following 'reason' attribute :"
				print e.reason
			return False
		else:
			
			strForm = handle.read().decode('UTF-8')
			#doc = fromstring(strForm)
			
			#form = doc.forms[0]
			#p_name = form.action
			#loginvalue = form.fields["login"]
			#fields = form.inputs.keys()
			
			loginvalue = self.getValue(strForm, '<input type="hidden" name="login" value="', '" />')
			userfield = self.getValue(strForm, '<input class="text" type="text" name="', '"')
			passfield = self.getValue(strForm, '<input class="text" type="password" name="', '"')			
			
			screenWidth = "3120"
			screenHeight = "1050"
			w = screenWidth + "%3A" + screenHeight
			
			x = random.randrange(80)
			y = random.randrange(20)			
			
			post = {
			    userfield:self.config.username, 
			    passfield:self.config.password, 
			    "s1.x":x, 
			    "s1.y":y, 
			    "s1":"login", 
			    "w":w, 
			    "login":loginvalue
			}			
		

		theurl = 'http://' + self.config.servername + '/dorf1.php'
		txdata = urllib.urlencode(post)
		#print 'use username: ',self.config.username,' and password: ', self.config.password, ' to login'
		#print "login value: %s" % loginvalue

		
		try:
			req = urllib2.Request(theurl, txdata, self.txheaders)
			handle = urllib2.urlopen(req)

		except IOError, e:
			print 'We failed to open "%s".' % theurl
			if hasattr(e, 'code'):
				print 'We failed with error code - %s.' % e.code
			elif hasattr(e, 'reason'):
				print "The error object has the following 'reason' attribute :"
				print e.reason
			return False
		else:
			#here we got web form after login should be http://s1.travian.cn/dorf1.php

			strHtml = handle.read()
			#print handle.geturl()

			if strHtml.find('login') > 0 and strHtml.find(u'username:') > 0 and strHtml.find(u'password:') > 0 :
				return False
			#print 'These are the cookies we have received so far :'
			#for index, cookie in enumerate(self.cj):
			#	print index, '  :  ', cookie        
			self.cj.save(self.COOKIEFILE)                     # save the cookies again
		return True
		


	def transformUrl(self, url):
		return hashlib.md5(url).hexdigest()

	def getFile(self, hash):
		path = os.path.join(self.cache, "%s.html" % (hash))
		content = None
		
		if os.path.isfile(path):
			fp = open(path, "r")
			content = fp.read()
			fp.close()
		
		return content

	def getCache(self, url):
		
		cache = self.transformUrl(url)
		content = self.getFile(cache)
		
		if content is not None:
			print "cache return: %s" % (url)

		return content

	def setCache(self, url, html):
		#print "cache: %s" % (url)
		
		file = self.transformUrl(url)
		file += ".html"
		path = os.path.join(self.cache, file)
		
		if os.path.isfile(path):
			os.remove(path)
			
		fp = open(path, "w")
		fp.write(html)
		fp.close()

	

	def get(self, page):
		url = "http://%s/%s" % (self.config.servername, page)
		content = None
		#content = self.getCache(url)
		
		c_page = os.path.join(self.cache, page.replace(".php", ".html"))
		if os.path.isfile(c_page):
			#content = open(c_page, "r").read()
			#print "cache"
			pass
		
		if content is None:
			content = self.getHtmlByURL(url)
			self.setCache(url, content)

		return content
	
	
	def getHtmlByURL(self,theurl):
		strHtml = ''
		succ = False
		
		for i in range(self.config.RetryNum):
			if not succ:
				#print 'Getting ' + theurl + '. The ' + str(i+1) + 'th try...'
				try:
					req = urllib2.Request(theurl, None, self.txheaders)
					handle = urllib2.urlopen(req)
				except IOError, e:
					print 'We failed to open "%s".' % theurl
					if hasattr(e, 'code'):
						print 'We failed with error code - %s.' % e.code
					elif hasattr(e, 'reason'):
						print "The error object has the following 'reason' attribute :"
						print e.reason
				else:
					succ = True
					strHtml = handle.read().decode('UTF-8');

		return strHtml
	



				
			
			