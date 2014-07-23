#!/usr/bin/env python

from ConfigParser import ConfigParser
CONFIGFILE = 'stitch.conf'
config = ConfigParser()
config.read(CONFIGFILE)
config.add_section('shit')
config.set('shit','shit','3')
config.write(open(CONFIGFILE, 'w'))
