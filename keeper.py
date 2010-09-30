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
import ConfigParser
import sys

class Config(dict):
	"""The configuration information for this script."""
	
	def __init__(self, options):
		self.required_options = ['token', 'account']

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

if __name__ == "__main__":
	parser = OptionParser()
	
	parser.add_option("-t", "--token", dest="token", help="Your Lighthouse token")
	parser.add_option("-a", "--account", dest="account", help="Your Lighthouse account")
	parser.add_option("-c", "--config", dest="config", help="The config file to use",
						default="config.ini")

	(options, args) = parser.parse_args()

	config = Config(options)

	print "Your configuration settings:"
	print "Lighthouse Token:   " + config['token']
	print "Lighthouse Account: " + config['account']