#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import re

def clean_file(stl_path, cleaned_stl_path):
	words = ['vertex', 'endloop']
	with open(stl_path, 'r') as f_stl, open(cleaned_stl_path, 'w') as f_cleaned_stl:
		for line in f_stl:
			if any(word in line for word in words):
				line = re.sub('^endloop.*', '|', line.lstrip())
				line = line.replace("vertex", "")
				line = line.lstrip().replace(" ", ",")
				line = line.replace("\n", ";")
				line = line.replace("|;", "\n")
				f_cleaned_stl.write(line)

def file_to_model(cleaned_stl_path):
	model = []
	with open(cleaned_stl_path) as f_cleaned_stl:
		for line in f_cleaned_stl:
			line = re.sub('[;\n]$', '\n', line)
			p = []
			for point in line.split(';'):
				pos_str = point.split(',')
				pos_int = []
				for nb in pos_str:
					pos_int.append(float(nb))
				p.append(pos_int)
		
			model.append(p)

	return model
