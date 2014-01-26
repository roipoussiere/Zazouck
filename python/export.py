#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import time, os, re, tempfile
import solid, stl
from os import path as op
import subprocess
import shlex
import signal
import xml.etree.ElementTree as ET

class Export: # TODO : singleton

	def __init__(self, project_dir, openscad_path, scad_dir, nb_job_slots, verbose_lvl, test):
		self.openscad_path = openscad_path
		self.project_dir = project_dir
		self.scad_dir = scad_dir
		self.nb_job_slots = nb_job_slots
		self.verbose_lvl = verbose_lvl
		self.test = test

		self.process = list() # liste de tuples (retour process, nom du fichier)
		self.nb_created = 0 # pour afficher le nombre de fichiers crées lors d'un ctrl-c
		signal.signal(signal.SIGINT, self.signal_handler)

		self.xml_path = op.join(project_dir, "build.zaz")
		self.root = ET.parse(self.xml_path).getroot()

		if test:
			print "Running in testing mode - don't print these files."

	def _print_status(self, i, nb_corners, t_init, picture=False):
		f_type = "picture" if picture else "stl file"
		print "Compiling " + f_type + " " + str(i+1) + "/" + str(nb_corners),
		print "(" + str(int(round(i/float(nb_corners)*100))) + "%)",
		if i==0:
			print "- please wait... "
		else:
			spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
			remaining = time.strftime("%Hh%Mm%Ss", time.gmtime((time.time()-t_init)/i*(nb_corners-i)))
			print "- started for " + spent + ", please wait", remaining + "."

	def make_documentation(self, doc_dir):
		IMG_SIZE = 200

		img_dir = op.join(doc_dir, "img")
		if not os.path.exists(img_dir):
			os.makedirs(img_dir)
		self.make_pictures(img_dir, IMG_SIZE)

	def make_pictures(self, img_dir, pict_width):
		extra_options = "--imgsize=" + str(pict_width*2) + "," + str(pict_width*2) + \
				" --camera=0,0,0,45,0,45,140"
		print "\n*** Creating pictures ***\n"

		corner = self.root.find('set')
		while corner.get('img') != "true":
			corner = self.root.find('set')

		part_scad_name = corner.get('file') if not self.test else corner.get('light_file')
		part_scad_path = op.join(self.scad_dir, part_scad_name)

		#TODO: ne pas transmettre l'arbre puisque on l'a dans self
		self._start_processes(part_scad_path, corner, img_dir, "png")

		dimentions = str(pict_width) + 'x' + str(pict_width)
		process_image = 'mogrify -trim +repage -resize ' + dimentions + \
				' -background "#FFFFE5" ' + '-gravity center -extent ' + dimentions + \
				' -fuzz 5% -transparent "#FFFFE5" ' + op.join(img_dir, "*.png")
		subprocess.Popen(shlex.split(process_image))

	def make_stl(self):
		for set in self.root.findall('set'):
			print "\n*** Creating " + set.get('name') + "s ***\n"

			part_scad_name = set.get('light_file') if self.test and \
					'light_file' in set.attrib else set.get('file')
			part_scad_path = op.join(self.scad_dir, part_scad_name)

			export_path = op.join(self.project_dir, set.get('name'))

			if not os.path.exists(export_path):
				os.makedirs(export_path)

			self._start_processes(part_scad_path, set, export_path, set.get('type'))

		self._save_xml()

	def _save_xml(self):
		ET.ElementTree(self.root).write(self.xml_path, encoding = "UTF-8", xml_declaration = True)

	def _start_processes(self, part_scad_path, set_tree, export_dir, type):
		nb_files = len(set_tree)

		print nb_files, type, "files will be created in " + export_dir + "."

		t_init = time.time()
		self.nb_created = 0

		if self.nb_job_slots == 1:
			print "Compiling the first " + type + " file, please wait...\n"
		else:
			nb_creating = self.nb_job_slots if self.nb_job_slots < nb_files else nb_files
			print "Compiling", nb_creating, type, "files simultaneously, please wait...\n"

		for part in set_tree:
			if 'done' not in part.attrib:
				options = "-D 'id=" + part.get('id') + "; " + part.get('data').replace('\'', '"') + "'"

				output_path = op.join(export_dir, part.get('id') + "." + type)
				self._openscad(part_scad_path, options, output_path, part)
				self._end_of_process(nb_files, t_init, type, part)
			else:
				print part.get('id') + '.' + type + ' already exists, pass.'

		while self.process:
			self._end_of_process(nb_files, t_init, type, part)

		print "\nFinished!", self.nb_created, type, "files successfully created in " + export_dir + "."

	def _end_of_process(self, nb_files, t_init, type, part):
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - t_init))

		for i, p in enumerate(self.process):
			
			if p[0].poll() == 0:
				del self.process[i]
				self.nb_created += 1
				progress = str(self.nb_created) + "/" + str(nb_files)

				# trouver la partie qui vient de se terminer
				if type != 'png':
					p[1].set('done', 'true')
					self._save_xml()

				print spent + ": Created file " + progress + ": " + p[1].get('id') + "." + type + '.'

	# def make_model(self, stls_dir, full_model_path):
	# 	import shutil

	# 	print "\n*** Creating full model ***\n"
	# 	print "This file will be created in " + full_model_path

	# 	temp_path = op.join(tempfile.gettempdir(), "full_model")
	# 	if os.path.exists(temp_path):
	# 		shutil.rmtree(temp_path)
	# 	os.makedirs(temp_path)

	# 	corner_move_scad_path = op.join(self.scad_dir, "move_part.scad")

	# 	with open(self.corners_table_path, 'r') as table:
	# 		table.readline()
	# 		table.readline()
			
	# 		for i, line in enumerate(table): # utiliser start_processes ?
	# 			data = line.split(",")[0:4]
	# 			file_name = data[0] + ".stl"
	# 			options = "-D 'file=\"" + op.join(stls_dir, file_name) + "\"; " + \
	# 					"tx=" + data[1] + "; ty=" + data[2] + "; tz=" + data[3] + "'"
	# 			output_file = op.join(temp_path, "moved_" + file_name)
	# 			self._openscad(corner_move_scad_path, options, output_file)

	def _openscad(self, scad_file_path, options, output_file, part):
		cmd = self.openscad_path + ' ' + scad_file_path + ' -o ' + output_file + ' ' + options

		if self.verbose_lvl >= 1:
			print '>>>' + cmd
		err = None if self.verbose_lvl >= 2 else open(os.devnull, 'w')
		out = None if self.verbose_lvl == 3 else open(os.devnull, 'w')

		p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = err)

		self.process.append((p, part))

		if len(self.process) >= self.nb_job_slots:
			p.wait()

	def signal_handler(self, signal, frame):
		import sys
		print "\n\nCompilation interrupted by the user."
		print self.nb_created, "file" + ('s' if self.nb_created > 1 else '') + " were created."
		print "You can continue this work later with this command:"
		print "zazouck " + self.project_dir + "'."
		sys.exit(0)