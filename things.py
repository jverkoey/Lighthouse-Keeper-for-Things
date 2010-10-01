#
#  things.py
#  Things Python API.
#
#  Methods for interacting with Things through Python via AppleScript.
#
#  Built based on the following guide:
#  http://culturedcode.com/things/download/ThingsAppleScriptGuide.pdf
#
#  Created by Jeff Verkoeyen on 2010-10-01.
#  Copyright 2010 Jeff Verkoeyen. Licensed under the Apache License, Version 2.0.
#  http://www.apache.org/licenses/LICENSE-2.0
#

import os
import subprocess

def get_project_id(name):
	"""Get the project's unique identifier from Things, if it exists. None otherwise."""

	cmd = """
tell application "Things"
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
	"""Set the project's Notes property in Things."""

	cmd = """
tell application "Things"
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
	"""Create a new Things project with the given name and description.
	Returns the Things id."""

	cmd = """
tell application "Things"
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
	"""Get the ticket's unique identifier from Things, if it exists. None otherwise."""

	cmd = """
tell application "Things"
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
	"""Create a new ticket in the given project."""

	cmd = """
tell application "Things"
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

def complete_ticket(project_name, name):
	"""Mark the given ticket as completed."""

	cmd = """
tell application "Things"
	set toDoToComplete to to do named "%s" of project "%s"
	set status of toDoToComplete to completed
end tell""" % (name, project_name)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		print "Unhandled error:"
		print "'" + stderr + "'"
		return None
	
	return True

def set_ticket_tags(project_name, name, tags):
	"""Set the ticket's tags property.
	
	tags is a string of the form: &quot;multi word&quot; singleword anotherword"""

	if tags is None:
		tags = ""

	taglist = tags.split(' ')
	cleantaglist = []
	buff = ""
	in_quote = False
	for tag in taglist:
		buff += tag.replace('&quot;', '')
		
		if tag.find('&quot;') == 0:
			in_quote = True
		if in_quote and tag.find('&quot;') > 0:
			cleantaglist.append(buff)
			buff = ""
			in_quote = False
		elif not in_quote:
			cleantaglist.append(buff)
			buff = ""
	tags = ','.join(cleantaglist)

	cmd = """
tell application "Things"
	set toDoToTag to to do named "%s" of project "%s"
	set tag names of toDoToTag to "%s"
end tell""" % (name, project_name, tags)

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		print "Unhandled error:"
		print "'" + stderr + "'"
		return None
	
	return True

def log_completed_tickets():
	"""Logs all completed tickets in Things."""

	cmd = """
tell application "Things"
	log completed now
end tell"""

	p = subprocess.Popen(['osascript', '-e', cmd], shell=False,
	 	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = p.communicate()

	if len(stderr) > 0:
		print "Unhandled error:"
		print "'" + stderr + "'"
		return None
	
	return True
