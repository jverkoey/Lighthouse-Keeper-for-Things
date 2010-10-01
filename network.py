#
#  network.py
#  Network methods.
#
#  Created by Jeff Verkoeyen on 2010-10-01.
#  Copyright 2010 Jeff Verkoeyen. Licensed under the Apache License, Version 2.0.
#  http://www.apache.org/licenses/LICENSE-2.0
#

from keeper import Lighthouse
from urllib2 import HTTPError
import BeautifulSoup
import hashlib
import os
import time
import urllib2

def url_to_cache_path(url):
	hash = hashlib.sha224(url).hexdigest()
	return os.path.join(Lighthouse.cache_path, hash)

def cache_check(url):
	cache_path = url_to_cache_path(url)

	if os.path.isfile(cache_path):
		return (time.time() - os.stat(cache_path).st_mtime) < Lighthouse.cache_expiration_seconds
	else:
		return False

def cache_get(url):
	cache_path = url_to_cache_path(url)
	
	f = open(cache_path, 'r')
	data = f.read()
	f.close()

	return data

def cache_put(url, data):
	cache_path = url_to_cache_path(url)
	
	f = open(cache_path, 'w')
	f.write(data)
	f.close()

def get_xml(endpoint, config):
	url = os.path.join(config.base_url(), endpoint)
	
	data = None
	if not cache_check(url):
		config.log("Sending request to " + url)

		headers = { 
			'X-LighthouseToken' : config['token'],
		}
		req = urllib2.Request(url, None, headers)	

		try:
			response = urllib2.urlopen(req)
			xml = response.read()
		except HTTPError as exception:
			config.log("There was an error fetching the data.")
			config.log(exception)
			config.log()
			exit

		cache_put(url, xml)

		config.log("Fetched!")
		
	else:
		config.log("Loading from cache...")
		xml = cache_get(url)
		config.log("Loaded!")

	return xml
	
def xml_to_data(xml):
	return BeautifulSoup.BeautifulStoneSoup(xml)
