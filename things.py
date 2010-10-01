#
#  things.py
#  Things Python API
#
#  Created by Jeff Verkoeyen on 2010-10-01.
#  Copyright 2010 Jeff Verkoeyen. Apache 2.0
#

import os
import subprocess

def get_project_id(name):
	cmd = """tell application "Things"
	set checkProject to project "%s"
	checkProject
end tell""" % (name)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		if stderr.find('(-1728)') >= 0:
			return None
		else:
			print "Unhandled error:"
			print stderr
			return None
	else:
		return stdout.rsplit(' ')[-1]

def set_project_description(name, description):
	cmd = """tell application "Things"
	set updateProject to project "%s"
	set notes of updateProject to "%s"
end tell""" % (name, description)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		if stderr.find('(-1728)') >= 0:
			return None
		else:
			print "Unhandled error:"
			print stderr
			return None
	else:
		return stdout.rsplit(' ')[-1]

def create_project(name, description):
	cmd = """tell application "Things"
	set newProject to make new project with properties {name:"%s", notes:"%s"}
	newProject
end tell""" % (name, description)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		print "Unhandled error:"
		print "'" + stderr + "'"
		return None

	return stdout.rsplit(' ')[-1]

def get_ticket_id(project_name, name):
	cmd = """tell application "Things"
	set ticket to to do named "%s" of project "%s"
	ticket
end tell""" % (name, project_name)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		if stderr.find('(-1728)') >= 0:
			return None
		else:
			print "Unhandled error:"
			print stderr
			return None
	else:
		return stdout.rsplit(' ')[-1]

def create_ticket(project_name, name, description, url):
	cmd = """tell application "Things"
	set newToDo to make new to do with properties {name:"%s", notes:"%s\nLighthouse URL: %s"} at beginning of project "%s"
end tell""" % (name, description, url, project_name)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		print "Unhandled error:"
		print "'" + stderr + "'"
		return None

	return stdout.rsplit(' ')[-1]
