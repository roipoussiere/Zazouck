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

		os.makedirs(op.join(self.doc_dir, 'parts_html'))
		self.make_pictures()
		self.make_html_menu(self.root)
		self.make_html_details(self.root)
		self.replace_html_index()

	def replace_html_index(self):
		import time
		index = op.join(self.doc_dir, 'index.html')
		os.rename(index, index + '~')

		with open(index, 'w') as fout, open(index + '~', 'r') as fin:
			for line in fin:
				line = line.replace('__TITLE__', (self.root.get('id') + ' documentation').capitalize())
				line = line.replace('__MODEL_PATH__', './parts_html/' + self.root.get('id'))
				line = line.replace('__TIME__', time.strftime('on %b %d, %Y at %l:%M%p'))
				fout.write(line)

		os.remove(index + '~')

	def make_html_menu(self, tree = False):
		parts_dir = op.join(self.doc_dir, 'parts')
		content = ET.Element('summary')

		menu = ET.SubElement(content, 'div')
		menu.set('id', 'menu')

		link = ET.SubElement(menu, 'a')
		link.text = self.root.get('id').capitalize()
		link.set('class', 'focus')
		link.set('href', './parts_html/' + self.root.get('id') + '.html')
		link.set('id', self.root.get('id'))
		link.set('onclick', 'document.getElementsByClassName("focus")[0].className = ""; this.className = "focus";')
		link.set('target', 'detail')

		self.feed_menu(self.root, menu)

		file_path = op.join(self.doc_dir, 'menu.html')
		self.make_html(file_path, content, 'stylesheet.css')

	def feed_menu(self, tree, menu):
		ul = ET.SubElement(menu, 'ul')
		for elmt in tree:
			li = ET.SubElement(ul, 'li')

			link = ET.SubElement(li, 'a')
			link.text = elmt.get('id').capitalize()
			link.set('href', './parts_html/' + elmt.get('id') + '.html')
			link.set('id', elmt.get('id'))
			link.set('onclick', 'document.getElementsByClassName("focus")[0].className = ""; this.className = "focus";')
			link.set('target', 'detail')
			
			if len(elmt) > 0:
				self.feed_menu(elmt, li)

	def make_html_details(self, tree):
		for elmt in tree:
			self.make_html_details(elmt)

		content = ET.Element('article')

		family_infos = ET.SubElement(content, 'div')
		family_infos.set('id', 'infos')
		
		img_path = '../parts_img/' + tree.get('id') + '.png' if tree.tag == 'part' else \
				'../img/group.png' if tree.tag == 'family' else ''

		if img_path != '':
			img = ET.SubElement(family_infos, 'img')
			img.set('class', 'large')
			img.set('src', img_path)

		element_text = ET.SubElement(family_infos, 'div')
		element_text.set('id', 'text')

		family_name = self.get_family_attribute(tree, 'id')
		title = family_name.capitalize() + ' ' if tree.tag == 'part' else ''
		ET.SubElement(element_text, 'h2').text = title + tree.get('id').capitalize()

		if family_name != '':
			parent = ET.SubElement(element_text, 'p')
			parent.text = 'Parent: '
			link = ET.SubElement(parent, 'a')
			link.set('href', family_name + '.html')
			link.set('class', 'link_info')
			ET.SubElement(link, 'b').text = family_name.capitalize()

		if len(tree) != 0:
			text_data = ET.SubElement(element_text, 'p')
			text_data.text = 'Number of elements: '
			ET.SubElement(text_data, 'b').text = str(len(tree))

		infos = (('Type', 'type', True), ('Position', 'pos', True), ('Rotation','rot', True), \
				('Generated by', 'file', False), ('Light version', 'light_file', False))

		for info in infos:
			parent_data = self.get_family_attribute(tree, info[1])
			data = tree.get(info[1]) if info[1] in tree.attrib else parent_data
			if data != '' and (tree.tag != 'part' or tree.tag == 'part' and info[2]):
				text_data = ET.SubElement(element_text, 'p')
				text_data.text = info[0] + ': '
				ET.SubElement(text_data, 'b').text = data

		parent_data = self.get_family_attribute(tree, 'data')
		curent_data = tree.get('data') if 'data' in tree.attrib else ''
		datas = parent_data + curent_data
		if datas != '':
			for data in datas.split(';'):
				tab_data = data.replace("'", '').replace(',', ', ').split('=')
				text_data = ET.SubElement(element_text, 'p')
				text_data.text = tab_data[0].capitalize() + ': '
				ET.SubElement(text_data, 'b').text = tab_data[1].capitalize()

		if len(tree) != 0:
			ET.SubElement(content, 'hr')
			childrens = ET.SubElement(content, 'div')
			childrens.set('class', 'elements')

			ET.SubElement(childrens, 'h3').text = 'Elements'

			for element in tree:
				childrens.append(self.html_elements(element.get('id')))

			clear_div = ET.SubElement(content, 'div')
			clear_div.set('class', 'separator')

		if 'connections' in tree.attrib:
			ET.SubElement(content, 'hr')
			connections = ET.SubElement(content, 'div')
			connections.set('class', 'elements')

			ET.SubElement(connections, 'h3').text = 'Connected to'

			for connection_id in tree.get('connections').split(';'):
				connections.append(self.html_elements(connection_id))

			clear_div = ET.SubElement(content, 'div')
			clear_div.set('class', 'separator')

		file_path = op.join(self.doc_dir, 'parts_html', tree.get('id') + '.html')
		self.make_html(file_path, content, '../stylesheet.css')

	def html_elements(self, elmt_id):
		file_path = elmt_id + '.html'

		elmt = ET.Element('a')
		#link.set('onclick', 'menu.getElementsById(' + element.get('id') + ') = "focus";')
		elmt.set('href', file_path)
		elmt.set('class', 'element')

		part_div = ET.SubElement(elmt, 'div')
		part_div.set('class', 'icon')
		ET.SubElement(part_div, 'h3').text = elmt_id.capitalize()

		img_path = '../parts_img/' + elmt_id + '.png'
		img = ET.SubElement(part_div, 'img')
		img.set('class', 'thumbnail')
		img.set('src', img_path)

		return elmt

	def get_family_attribute(self, elmt, attribute):
		parent_map = dict((c, p) for p in self.root.getiterator() for c in p)
		try:
			value = parent_map[elmt].get(attribute)
			return value if value != None else ''
		except:
			return ''

	def make_html(self, file_path, content, css_path):
		html = ET.Element('html')
		head = ET.SubElement(html, 'head')

		link = ET.SubElement(head, 'link')
		link.set('rel', 'stylesheet')
		link.set('href', css_path)

		body = ET.SubElement(html, 'body')
		#body.set('onload', 'menu.getElementsById(' + element.get('id') + ') = "focus";')
		body.append(content)
		utils.indent(html)

		with open(file_path, 'w') as f:
			f.write('<!DOCTYPE html>\n')
			ET.ElementTree(html).write(f, 'utf-8')

	def make_pictures(self):
		IMG_SIZE = 200

		print "\n*** Creating pictures ***"

		img_dir = op.join(self.doc_dir, 'parts_img')
		os.makedirs(img_dir)


		for family in (family for family in self.root if 'img' in family.attrib):
			img_opt = "--imgsize=" + str(IMG_SIZE * 2) + "," + str(IMG_SIZE * 2) + " --camera=" + family.get('img')
			part_scad_path = op.join(self.scad_dir, family.get('file'))

			process.Process(part_scad_path, family, img_dir, self.jobs, self.openscad_path, self.verbose, img_opt)

			dimentions = str(IMG_SIZE) + 'x' + str(IMG_SIZE)
			cmd = 'mogrify -trim +repage -resize ' + dimentions + \
					' -background "#FFFFE5" ' + '-gravity center -extent ' + dimentions + \
					' -fuzz 15% -transparent "#FFFFE5" ' + op.join(img_dir, '*.png')
			# - colorspace xxx
			#shadow_cmd = 'for f in ' + op.join(img_dir, '*.png') + '; do convert $f -trim ' + \
			#		'\( +clone -background black -shadow 80x5+5+5 \) +swap -background none -layers merge $f; done'

			try:
				subprocess.Popen(shlex.split(cmd))
				#os.system(shadow_cmd)
			except:
				print "Error when processing images. Do you have ImageMagick installed?"