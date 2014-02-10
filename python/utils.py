#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.
def create_dir(directory, verbose):
	from os import path as op
	import os, shutil

	if os.path.exists(directory):
		shutil.rmtree(directory)
		if verbose > 0:
			print "The existing folder '" + op.basename(directory) + "' has been overwriten."
	os.makedirs(directory)

def cmd(command, verbose):
	import os, subprocess, shlex

	if verbose >= 2:
		print '>>>' + command

	out = None if verbose == 4 else open(os.devnull, 'w')
	err = None if verbose >= 3 else open(os.devnull, 'w')

	try:
		p = subprocess.Popen(shlex.split(command), stdout = out, stderr = err)
	except:
		print "Err: Can't build the file with OpenScad."
		p = False

	return p

def indent(elem, level=0):
	i = "\n" + level*"\t"
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "\t"
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

def get_params(param_path, xml_path):
	import xml.etree.ElementTree as ET
	import re
	root = ET.parse(xml_path).getroot()
	params = list()

	with open(param_path, 'r') as param:
		for line in param:
			data = re.sub(r'\s+', '=', line.strip())
			if data:
				data = data.split('=')
				isnumber = data[1].replace(".", "", 1).isdigit()
				if data[0] == 'thickness':
					root.set('thickness', data[1])
				else:
					data = data[0] + "=" + (data[1] if isnumber else "'" + data[1] + "'")
					params.append(data)
	datas = '; '.join(params)
	root.set('data', datas)

	ET.ElementTree(root).write(xml_path, encoding = "UTF-8", xml_declaration = True)