#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import time
from os import path as op
import os
import subprocess
import shlex


class Process():

	def __init__(self, part_scad_path, set_tree, export_dir, nb_job_slots, openscad_path, verbose_lvl, is_img = False, is_assembly = False):
		self.process = list() # liste de tuples (retour process, nom du fichier)
		self.nb_created = 0 # pour afficher le nombre de fichiers crées lors d'un ctrl-c
		self.part_scad_path = part_scad_path
		self.set_tree = set_tree
		self.export_dir = export_dir
		self.nb_job_slots = nb_job_slots
		self.openscad_path = openscad_path
		self.verbose_lvl = verbose_lvl
		self._start_processes(is_img, is_assembly)

	# TODO : option pour passer si done existe ?
	def _start_processes(self, is_img, is_assembly):
		nb_files = len(self.set_tree)
		t_init = time.time()
		self.nb_created = 0
		type = 'png' if is_img else self.set_tree.get('type')

		print nb_files, type, "files will be created in " + self.export_dir + '.'

		if self.nb_job_slots == 1:
			print "Compiling the first " + type + " file, please wait...\n"
		else:
			nb_creating = self.nb_job_slots if self.nb_job_slots < nb_files else nb_files
			print "Compiling", nb_creating, type, "files simultaneously, please wait...\n"

		for part in self.set_tree:
			if 'done' not in part.attrib or is_assembly:
				id = 'id=' + part.get('id') + '; '
				pos = 'pos=[' + part.get('pos') + ']; ' if 'pos' in part.attrib and is_assembly else ''
				rot = 'rot=[' + part.get('rot') + ']; ' if 'rot' in part.attrib and is_assembly else ''
				var = part.get('data').replace('\'', '"')

				options = "-D '" + id + pos + rot + var + "'"

				output_path = op.join(self.export_dir, part.get('id') + "." + type)
				self.openscad(self.part_scad_path, options, output_path, part)
				self._end_of_process(nb_files, t_init, type, part)
			else:
				print part.get('id') + '.' + type + ' already exists, pass.'
				self.nb_created += 1

		while self.process:
			self._end_of_process(nb_files, t_init, type, part)

		print "\nFinished!", self.nb_created, type, "files successfully created in " + self.export_dir + '.'

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

	def _end_of_process(self, nb_files, t_init, type, part):
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - t_init))

		for i, p in enumerate(self.process):
			
			if p[0].poll() == 0:
				del self.process[i]
				self.nb_created += 1
				progress = str(self.nb_created) + '/' + str(nb_files)

				if type != 'png':
					p[1].set('done', 'true')

				print spent + ": Created file " + progress + ': ' + p[1].get('id') + '.' + type + '.'

	def openscad(self, scad_file_path, options, output_file, part):
		cmd = self.openscad_path + ' ' + scad_file_path + ' -o ' + output_file + ' ' + options

		if self.verbose_lvl >= 1:
			print '>>>' + cmd
		err = None if self.verbose_lvl >= 2 else open(os.devnull, 'w')
		out = None if self.verbose_lvl == 3 else open(os.devnull, 'w')

		p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = err)

		self.process.append((p, part))

		if len(self.process) >= self.nb_job_slots:
			p.wait()