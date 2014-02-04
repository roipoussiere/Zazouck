#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

from os import path as op
import xml.etree.ElementTree as ET
import os, subprocess, shlex, shutil
import process, utils

class Doc:
	def __init__(self, xml_path, zazouck_dir, doc_dir, scad_dir, jobs, openscad_path, verbose):
		self.doc_dir = doc_dir
		os.makedirs(doc_dir)
		self.jobs = jobs
		self.openscad_path = openscad_path
		self.verbose = verbose
		self.scad_dir = scad_dir
		self.root = ET.parse(xml_path).getroot()

		self.make_pictures()
		shutil.copy(op.join(zazouck_dir, op.join("doc_generation", "doc.css")), doc_dir)
		self.create_main_file()

	def create_main_file(self):
		index_path = op.join(self.doc_dir, "index.html")
		title = (self.root.get('name') + " documentation").capitalize()

		html = ET.Element("html")

		head = ET.SubElement(html, "head")
		ET.SubElement(head, "title").text = title

		link = ET.SubElement(head, "link")
		link.set('rel', 'stylesheet')
		link.set('href', 'doc.css')
		
		body = ET.SubElement(html, "body")
		ET.SubElement(body, "h1").text = title

		for set in self.root:
			set_div = ET.SubElement(body, 'div')
			set_div.set('class', 'set')
			ET.SubElement(set_div, 'h2').text = set.get('name').capitalize() + 's'

			clear_div = ET.SubElement(body, 'div')
			clear_div.set('class', 'separator')

			for part in set:
				part_div = ET.SubElement(set_div, 'div')
				part_div.set('class', 'part')
				ET.SubElement(part_div, 'h3').text = part.get('id')

				if set.get('img') == 'true':
					img = ET.SubElement(part_div, 'img')
					img.set('class', 'part')
					img.set('src', op.join('img', part.get('id') + '.png'))

		utils.indent(html)
		tree = ET.ElementTree(html)
		tree.write(index_path, encoding = "UTF-8", xml_declaration = True)

	def make_pictures(self):
		IMG_SIZE = 200

		print "\n*** Creating pictures ***"

		img_dir = op.join(self.doc_dir, "img")
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
		process.Process(part_scad_path, corner, img_dir, self.jobs, self.openscad_path, self.verbose, is_img = True)
					#part_scad_path, set_tree, export_dir, nb_job_slots, openscad_path, verbose_lvl, is_img = False, is_assembly = False
		dimentions = str(IMG_SIZE) + 'x' + str(IMG_SIZE)
		process_image = 'mogrify -trim +repage -resize ' + dimentions + \
				' -background "#FFFFE5" ' + '-gravity center -extent ' + dimentions + \
				' -fuzz 5% -transparent "#FFFFE5" ' + op.join(img_dir, "*.png")
		subprocess.Popen(shlex.split(process_image))
