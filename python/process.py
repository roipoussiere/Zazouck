#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import os, sys, time, subprocess, shlex, platform
from os import path as op


class Process():

	def __init__(self, part_scad_path, set_tree, export_dir, nb_job_slots, openscad_path, verbose_lvl, is_img = False, is_assembly = False):
		self.process = list() # liste de tuples (retour process, nom du fichier)
		self.nb_created = 0 # pour afficher le nombre de fichiers crées lors d'un ctrl-c
		self.progress = 0 # nb entre 0 et 78
		self.part_scad_path = part_scad_path
		self.set_tree = set_tree
		self.nb_files = len(set_tree)
		self.export_dir = export_dir
		self.nb_job_slots = nb_job_slots
		self.t_init = time.time()
		self.openscad_path = openscad_path
		self.verbose_lvl = verbose_lvl
		self.type = 'png' if is_img else set_tree.get('type')
		try:
			self.console_width = int(os.popen('stty size', 'r').read().split()[1])
		except:
			self.console_width = 80
		self._start_processes(is_img, is_assembly)

	# TODO : option pour passer si done existe ?
	def _start_processes(self, is_img, is_assembly):
		print self.nb_files, self.type, "files will be created in " + self.export_dir + '.'

		if self.nb_job_slots == 1:
			print "Compiling the first " + self.type + " file, please wait...\n"
		else:
			nb_creating = self.nb_job_slots if self.nb_job_slots < self.nb_files else self.nb_files
			print "Compiling", nb_creating, self.type, "files simultaneously, please wait..."

			print '_' * self.console_width if self.verbose_lvl == 0 else ''

		for part in self.set_tree:
			if 'done' not in part.attrib or is_assembly:
				id = 'id=' + part.get('id') + '; '
				pos = 'pos=[' + part.get('pos') + ']; ' if 'pos' in part.attrib and is_assembly else ''
				rot = 'rot=[' + part.get('rot') + ']; ' if 'rot' in part.attrib and is_assembly else ''
				var = part.get('data').replace('\'', '"')

				options = "-D '" + id + pos + rot + var + "'"

				output_path = op.join(self.export_dir, part.get('id') + "." + self.type)
				self.openscad(self.part_scad_path, options, output_path, part)
				self._end_of_process(part)
			else:
				print part.get('id') + '.' + self.type + ' already exists, pass.'
				self.nb_created += 1

		while self.process:
			self._end_of_process(part)

		print '\n' if self.verbose_lvl == 0 else ''
		print "Finished!", self.nb_created, self.type, "files successfully created in " + self.export_dir + '.'

	def _print_status(self, tree):
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - self.t_init))
		str_progress = str(self.nb_created) + '/' + str(self.nb_files)

		if self.verbose_lvl == 0:
			progress = int(round(self.console_width * float(self.nb_created) / self.nb_files))
			sys.stdout.write('#' * (progress - self.progress))
			sys.stdout.flush()
			self.progress = progress
		else:
			print spent + ": Created file " + str_progress + ': ' + tree.get('id') + '.' + self.type + '.'
		# f_type = "picture" if picture else "stl file"
		# print "Compiling " + f_type + " " + str(i+1) + "/" + str(nb_corners),
		# print "(" + str(int(round(i/float(nb_corners)*100))) + "%)",
		# if i==0:
		# 	print "- please wait... "
		# else:
		# 	spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - self.t_init))
		# 	remaining = time.strftime("%Hh%Mm%Ss", time.gmtime((time.time() - self.t_init)/i*(nb_corners-i)))
		# 	print "- started for " + spent + ", please wait", remaining + "."

	def _end_of_process(self, part):
		for i, p in enumerate(self.process):
			
			if p[0].poll() == 0:
				del self.process[i]
				self.nb_created += 1

				if self.type != 'png':
					p[1].set('done', 'true')
				self._print_status(p[1])

	def openscad(self, scad_file_path, options, output_file, part):
		cmd = self.openscad_path + ' ' + scad_file_path + ' -o ' + output_file + ' ' + options

		if self.verbose_lvl >= 2:
			print '>>>' + cmd
		err = None if self.verbose_lvl >= 3 else open(os.devnull, 'w')
		out = None if self.verbose_lvl == 4 else open(os.devnull, 'w')

		p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = err)

		self.process.append((p, part))

		if len(self.process) >= self.nb_job_slots:
			p.wait()