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
import network
import os
import subprocess
import sys
import things

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
	cache_expiration_seconds = 60*60

	def __init__(self, config):
		self.config = config
		self.projects = []

		try:
			os.mkdir(Lighthouse.cache_path)
		except Exception:
			pass

	def update_projects(self):
		self.config.log("Fetching the projects list...")

		xml = network.get_xml(Project.endpoint, config)
		data = network.xml_to_data(xml)
		
		self.projects = []
		
		for project_data in data.projects:
			if not isinstance(project_data, BeautifulSoup.Tag):
				continue

			project = Project(project_data)
			project.update_tasks()
			self.projects.append(project)


class Project(dict):
	endpoint = "projects.xml"
	
	def __init__(self, project_data):
		for node in project_data.contents:
			if not isinstance(node, BeautifulSoup.Tag):
				continue
			self[node.name] = node.string

		self.id = things.get_project_id(self.name())

		if self.id is None:
			print "Creating a new Things project for " + self['name'] + "..."
			self.id = things.create_project(self.name(), self.description())
		else:
			things.set_project_description(self.name(), self.description())

	def name(self):
		return self['name'] + ' (LH)'

	def description(self):
		description = self['description']
		if description is None:
			description = ""
		else:
			description += "-"
		description += "Imported from Lighthouse"
		return description

	def update_tasks(self):
		print 'hai'



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
	
	