#
#  keeper.py
#  The Lighthouse Keeper (for Things)
#
#  Keep your Lighthouse tasks up-to-date in Things.
#
#  http://lighthouseapp.com/api
#
#  Created by Jeff Verkoeyen on 2010-09-30.
#  Copyright 2010 Jeff Verkoeyen. Apache 2.0
#

from optparse import OptionParser
from urllib2 import HTTPError
from xml.dom import minidom
import BeautifulSoup
import ConfigParser
import hashlib
import os
import sys
import time
import urllib2

class Config(dict):
	"""The configuration information for this script."""
	
	def __init__(self, options):
		self.required_options = ['token', 'account']
		self.is_verbose = options.is_verbose

		any_missing = False
		for name in self.required_options:
			self[name] = options.__dict__[name]
			if self[name] is None:
				any_missing = True

		if any_missing:
			self.read_config(options.config)

	def read_config(self, config_path):
		config = ConfigParser.ConfigParser()
		config.read(config_path)

		try:		
			for name in self.required_options:
				if self[name] is None:
					self[name] = config.get('lighthouse', name)
		except ConfigParser.NoOptionError as exception:
			print exception
			exit
			
	def base_url(self):
		return 'http://%s.lighthouseapp.com/' % (self['account'])
	
	def log(self, text=""):
		if self.is_verbose:
			print text

class Lighthouse(object):
	# TODO: Make these configurable.
	cache_path = 'cache'
	cache_expiration_seconds = 60*5
	
	def __init__(self, config):
		self.config = config
		self.projects = []
		
		try:
			os.mkdir(Lighthouse.cache_path)
		except Exception:
			pass
	
	def url_to_cache_path(self, url):
		hash = hashlib.sha224(url).hexdigest()
		return os.path.join(Lighthouse.cache_path, hash)
	
	def cache_check(self, url):
		cache_path = self.url_to_cache_path(url)

		if os.path.isfile(cache_path):
			return (time.time() - os.stat(cache_path).st_mtime) < Lighthouse.cache_expiration_seconds
		else:
			return False
	
	def cache_get(self, url):
		cache_path = self.url_to_cache_path(url)
		
		f = open(cache_path, 'r')
		data = f.read()
		f.close()

		return data
	
	def cache_put(self, url, data):
		cache_path = self.url_to_cache_path(url)
		
		f = open(cache_path, 'w')
		f.write(data)
		f.close()
	
	def get_data(self, endpoint):
		url = os.path.join(self.config.base_url(), endpoint)
		
		data = None
		if not self.cache_check(url):
			self.config.log("Sending request to " + url)

			headers = { 
				'X-LighthouseToken' : self.config['token'],
			}
			req = urllib2.Request(url, None, headers)	

			try:
				response = urllib2.urlopen(req)
				data = response.read()
			except HTTPError as exception:
				self.config.log("There was an error fetching the data.")
				self.config.log(exception)
				self.config.log()
				exit

			self.cache_put(url, data)

			self.config.log("Fetched!")
			
		else:
			self.config.log("Loading from cache...")
			data = self.cache_get(url)
			self.config.log("Loaded!")
			
		
		return data
	
	def update_projects(self):
		self.config.log("Fetching the projects list...")

		data = self.get_data(Project.endpoint)
		
		
		

class Project(object):
	endpoint = "projects.xml"
	
	def __init__(self):
		print "hai"
	

if __name__ == "__main__":
	parser = OptionParser()
	
	parser.add_option("-a", "--account", dest="account", help="Your Lighthouse account")
	parser.add_option("-c", "--config", dest="config", help="The config file to use",
						default="config.ini")
	parser.add_option("-t", "--token", dest="token", help="Your Lighthouse token")					
	parser.add_option("-v", "--verbose", dest="is_verbose", action="store_true",
						help="Display verbose text")

	(options, args) = parser.parse_args()

	config = Config(options)

	config.log("Your configuration settings:")
	config.log("Lighthouse Token:    " + config['token'])
	config.log("Lighthouse Account:  " + config['account'])
	config.log("Lighthouse Base URL: " + config.base_url())
	config.log()
	
	l = Lighthouse(config)
	l.update_projects()
	
	