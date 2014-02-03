#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

from os import path as op
import xml.etree.ElementTree as ET
import os
import process

class Doc:
	# créer images dans cette classe ?
	def __init__(self, xml_path, doc_dir, scad_dir):
		self.doc_dir = doc_dir
		os.makedirs(doc_dir)
		self.create_files()
		self.scad_dir = scad_dir

	def create_files(self):
		index_path = op.join(self.doc_dir, "index.html")

		with open(index_path, 'w') as index:
			str = "<!DOCTYPE html>\n"
			str += "<html>\n"
			str += "\t<head>\n"
			str += "\t\t<title> Documentation </title>\n"
			str += "\t</head>\n"
			str += "\t<body>\n"
			str += "\t\t<h1> " + "part" + " </h1>\n"
			str += "\t</body>\n"
			str += "</html>\n"
			index.write(str)

	def make_pictures(self, img_dir):
		IMG_SIZE = 200

		print "\n*** Creating pictures ***\n"

		img_dir = op.join(doc_dir, "img")
		if not os.path.exists(img_dir):
			os.makedirs(img_dir)

		extra_options = "--imgsize=" + str(IMG_SIZE * 2) + "," + str(IMG_SIZE * 2) + \
				" --camera=0,0,0,45,0,45,140"

		corner = self.root.find('set')
		while corner.get('img') != "true":
			corner = self.root.find('set')

		part_scad_name = corner.get('file')
		part_scad_path = op.join(self.scad_dir, part_scad_name)

		#TODO: ne pas transmettre l'arbre puisque on l'a dans self

		self._start_processes(part_scad_path, corner, img_dir, 'png')

		dimentions = str(IMG_SIZE) + 'x' + str(IMG_SIZE)
		process_image = 'mogrify -trim +repage -resize ' + dimentions + \
				' -background "#FFFFE5" ' + '-gravity center -extent ' + dimentions + \
				' -fuzz 5% -transparent "#FFFFE5" ' + op.join(img_dir, "*.png")
		subprocess.Popen(shlex.split(process_image))
