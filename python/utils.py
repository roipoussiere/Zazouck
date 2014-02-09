#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

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
				data = data[0] + "=" + (data[1] if isnumber else "'" + data[1] + "'")
				params.append(data)
	datas = '; '.join(params)
	root.set('data', datas)

	ET.ElementTree(root).write(xml_path, encoding = "UTF-8", xml_declaration = True)