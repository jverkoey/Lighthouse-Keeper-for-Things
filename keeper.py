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

import ConfigParser

if __name__ == "__main__":
  config = ConfigParser.ConfigParser()
  config.read("config.ini")

  print config.get('lighthouse', 'token')
  print config.get('')
