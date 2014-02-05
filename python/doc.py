#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

from os import path as op
import xml.etree.ElementTree as ET
import os, subprocess, shlex, distutils.core
import process, utils

class Doc:
	def __init__(self, xml_path, zazouck_dir, doc_dir, scad_dir, jobs, openscad_path, verbose):
		self.doc_dir = doc_dir
		self.jobs = jobs
		self.openscad_path = openscad_path
		self.verbose = verbose
		self.scad_dir = scad_dir
		self.root = ET.parse(xml_path).getroot()

		doc_files_dir = op.join(zazouck_dir, 'doc_generation')
		distutils.dir_util.copy_tree(doc_files_dir, doc_dir)

		self.make_pictures()
		self.make_html_parts()
		self.make_html_families()
		self.make_html_menu()
		self.make_html_model()

	def make_html_model(self):
		import time

		content = ET.Element('article')
		ET.SubElement(content, 'p').text = 'Please select a part on the summary.'
		ET.SubElement(content, 'p').text = 'documentation created at ' + time.strftime('%l:%M%p on %b %d, %Y')
		file_path = op.join(self.doc_dir, 'model.html')
		self.make_html(file_path, content)

	def make_html_menu(self):
		parts_dir = op.join(self.doc_dir, 'parts')
		content = ET.Element('summary')
		ul_family = ET.SubElement(content, 'ul')

		for family in self.root:
			li_family = ET.SubElement(ul_family, 'li')

			link = ET.SubElement(li_family, 'a')
			link.text = family.get('name').capitalize() + 's'
			link.set('href', op.join(self.doc_dir, family.get('name') + '.html'))
			link.set('target', 'detail')

			ul_part = ET.SubElement(li_family, 'ul')
			for part in family:
				li_part = ET.SubElement(ul_part, 'li')

				link = ET.SubElement(li_part, 'a')
				link.text = part.get('id')
				link.set('href', op.join(parts_dir, part.get('id') + '.html'))
				link.set('target', 'detail')

		file_path = op.join(self.doc_dir, 'menu.html')
		self.make_html(file_path, content)

	def make_html_families(self):
		img_dir = op.join(self.doc_dir, 'img')

		for family in self.root:
			content = ET.Element('article')
			ET.SubElement(content, 'h2').text = family.get('name').capitalize() + 's'

			parts_div = ET.SubElement(content, 'div')
			parts_div.set('class', 'icons')

			for part in family:
				file_path = op.join(op.join(self.doc_dir, 'parts'), part.get('id') + '.html')

				part_link = ET.SubElement(parts_div, 'a')
				part_link.set('href', file_path)
				part_link.set('class', 'part')

				part_div = ET.SubElement(part_link, 'div')
				part_div.set('class', 'icon')
				ET.SubElement(part_div, 'h3').text = part.get('id')

				if family.get('img') == 'true':
					img = ET.SubElement(part_div, 'img')
					img.set('class', 'thumbnail')
					img.set('src', op.join(img_dir, part.get('id') + '.png'))

			clear_div = ET.SubElement(content, 'div')
			clear_div.set('class', 'separator')

			file_path = op.join(self.doc_dir, family.get('name') + '.html')
			# (self.root.get('name') + " documentation").capitalize()
			self.make_html(file_path, content)

	def make_html_parts(self):
		img_dir = op.join(self.doc_dir, 'img')
		parts_dir = op.join(self.doc_dir, 'parts')
		os.makedirs(parts_dir)

		for family in self.root:
			type = family.get('type')
			
			for part in family:
				content = ET.Element("article")

				if family.get('img') == 'true':
					img = ET.SubElement(content, 'img')
					img.set('class', 'large')
					img.set('src', op.join(img_dir, part.get('id') + '.png'))

				infos_div = ET.SubElement(content, 'div')
				ET.SubElement(infos_div, 'p').text = 'Id: ' + part.get('id')
				ET.SubElement(infos_div, 'p').text = \
						'Position: ' + ('unknown' if part.get('pos') == None else part.get('pos'))
				ET.SubElement(infos_div, 'p').text = \
						'Rotation: ' + ('unknown' if part.get('rot') == None else part.get('rot'))

				ET.SubElement(infos_div, 'p').text = 'Datas:'
				ul_data = ET.SubElement(infos_div, 'ul')

				for data in part.get('data').split(';'):
					ET.SubElement(ul_data, 'li').text = data

				file_path = op.join(parts_dir, part.get('id') + '.html')
				# type + ' ' + part.get('id').capitalize()
				self.make_html(file_path, content)

	def make_html(self, file_path, content):
		html = ET.Element('html')
		head = ET.SubElement(html, 'head')

		link = ET.SubElement(head, 'link')
		link.set('rel', 'stylesheet')
		link.set('href', 'index.css')

		body = ET.SubElement(html, 'body')
		body.append(content)
		utils.indent(html)
		ET.ElementTree(html).write(file_path)

	def make_pictures(self):
		IMG_SIZE = 200

		print "\n*** Creating pictures ***"

		img_dir = op.join(self.doc_dir, "img")
		if not os.path.exists(img_dir):
			os.makedirs(img_dir)

		extra_options = "--imgsize=" + str(IMG_SIZE * 2) + "," + str(IMG_SIZE * 2) + \
				" --camera=0,0,0,45,0,45,140"

		corner = self.root.find('family')
		while corner.get('img') != "true":
			corner = self.root.find('family')

		part_scad_name = corner.get('file')
		part_scad_path = op.join(self.scad_dir, part_scad_name)

		#TODO: ne pas transmettre l'arbre puisque on l'a dans self
		process.Process(part_scad_path, corner, img_dir, self.jobs, self.openscad_path, self.verbose, is_img = True)

		dimentions = str(IMG_SIZE) + 'x' + str(IMG_SIZE)
		process_image = 'mogrify -trim +repage -resize ' + dimentions + \
				' -background "#FFFFE5" ' + '-gravity center -extent ' + dimentions + \
				' -fuzz 5% -transparent "#FFFFE5" ' + op.join(img_dir, "*.png")
		try:
			subprocess.Popen(shlex.split(process_image))
		except:
			print "Warning: please install ImageMagic to build nice pictures for the documentation."
