#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazoucko.
# Zazoucko is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazoucko is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazoucko. If not, see <http://www.gnu.org/licenses/>.

import time, os, re, tempfile
import solid, stl
from os import path as op
import subprocess
import shlex
import signal

class Export: # TODO : singleton

	def __init__(self, openscad_path, table_path, zazoucko_scad_dir, export_dir, nb_job_slots, verbose_lvl, test):
		self.openscad_path = openscad_path
		self.table_path = table_path
		self.zazoucko_scad_dir = zazoucko_scad_dir
		self.export_dir = export_dir
		self.nb_job_slots = nb_job_slots
		self.verbose_lvl = verbose_lvl
		self.test = test
		self.process = list()
		self.nb_created = 0
		signal.signal(signal.SIGINT, self.signal_handler)


	def _get_nb_lines(self, input_path):
		with open(input_path, 'r') as f_input:
			for nb_lines, line in enumerate(f_input):
				pass
		return nb_lines + 1

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

	def make_csv(self, input_stl_path, details_path, start_from, finish_at, shuffle):
		cleaned_path = op.join(tempfile.gettempdir(), "zazoucko_cleaned")

		stl.clean_file(input_stl_path, cleaned_path)
		_model = stl.file_to_model(cleaned_path)
		os.remove(cleaned_path)
		
		s = solid.Solid()
		s.fill_corners(_model)
		s.fill_polygons(_model)
		del _model
		
		s.set_connected_corners()
		s.set_angles()
		s.set_datas()
		s.fill_edges()
		#s.merge_coplanar_polygons() # TODO

		s.build_csv(self.table_path, start_from, finish_at, shuffle)
		
		if details_path != None:
			s.display(details_path)

		print "Successfully created table file in " + self.table_path + "."

	def make_documentation(self, doc_dir):
		img_dir = op.join(doc_dir, "img")

		os.makedirs(img_dir)
		self.make_pictures(img_dir, 150)

	def make_pictures(self, img_dir, pict_width):
		nb_corners = self._get_nb_lines(self.table_path)-2
		corner_scad_path = op.join(self.zazoucko_scad_dir, ("corner_light.scad" if self.test else "corner.scad"))

		print "\n*** Creating pictures ***\n"
		print str(nb_corners) + " pictures will be created in " + img_dir + "."

		with open(self.table_path, 'r') as f_table:		
			print "Model details: " + f_table.readline().rstrip('\n').replace(",", ", ") + "."
			f_table.readline()
			extra_options = "--imgsize=" + str(pict_width) + "," + str(pict_width) + " --camera=0,0,0,45,0,45,140"

			self._start_processes(corner_scad_path, nb_corners, f_table, img_dir, "png", extra_options)

		cmd = 'mogrify -transparent "#FFFFE5" ' + op.join(img_dir, "*.png")
		subprocess.Popen(shlex.split(cmd))

	def make_corners(self):
		nb_corners = self._get_nb_lines(self.table_path)-2
		corner_scad_path = op.join(self.zazoucko_scad_dir, ("corner_light.scad" if self.test else "corner.scad"))
		
		print "\n*** Creating corners ***\n"
		print nb_corners, "stl files will be created in " + self.export_dir + "."

		with open(self.table_path, 'r') as f_table:
			print "Model details: " + f_table.readline().rstrip('\n').replace(",", ", ") + "."
			if self.nb_job_slots == 1:
				print "Tip : You can parallelize this task on several cores with -j option."
			
			f_table.readline()
			self._start_processes(corner_scad_path, nb_corners, f_table, self.export_dir, "stl")

		print "\n*** Finished! ***"
		print self.nb_created, "stl files successfully created in " + self.export_dir + "."

	def _start_processes(self, scad_path, nb_files, f_table, output_dir, extension, extra_options = ""):
		t_init = time.time()
		self.nb_created = 0

		if self.nb_job_slots == 1:
			print "\nCompiling the first " + extension + " file, please wait..."
		else:
			print "\nCompiling", self.nb_job_slots if self.nb_job_slots < nb_files else nb_files, extension, "files simultaneously, please wait..."

		for line in f_table:
			corner_id = line[0:line.index(",")]
			start = [m.start() for m in re.finditer(r",",line)][3]+1 # position de départ des données
			data = line.rstrip('\n')[start:]
			options = "-D 'id=" + str(corner_id) + "; angles=\"" + data + "\"' " + extra_options
			output_path = op.join(output_dir, corner_id + "." + extension)

			self._openscad(scad_path, options, output_path, corner_id)
			self._end_of_process(nb_files, t_init, op.basename(output_path))

		while self.process:
			self._end_of_process(nb_files, t_init, op.basename(output_path))

	def _end_of_process(self, nb_files, t_init, file_name):
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - t_init))
		for i, p in enumerate(self.process):
			if p.poll() == 0:
				del self.process[i]
				self.nb_created += 1
				print spent + ": Created file " + str(self.nb_created) + "/" + str(nb_files) + ": " + file_name + "."

	def make_model(self, stls_dir, full_model_path):
		import shutil

		print "\n*** Creating full model ***\n"
		print "This file will be created in " + full_model_path

		temp_path = op.join(tempfile.gettempdir(), "full_model")
		if os.path.exists(temp_path):
			shutil.rmtree(temp_path)
		os.makedirs(temp_path)

		corner_move_scad_path = op.join(self.zazoucko_scad_dir, "move_part.scad")

		with open(self.table_path, 'r') as f_table:
			f_table.readline()
			f_table.readline()
			
			for i, line in enumerate(f_table): # utiliser start_processes ?
				data = line.split(",")[0:4]
				file_name = data[0] + ".stl"
				options = "-D 'file=\"" + op.join(stls_dir, file_name) + "\"; tx=" + data[1] + "; ty=" + data[2] + "; tz=" + data[3] + "'"
				output_file = op.join(temp_path, "moved_" + file_name)
				self._openscad(corner_move_scad_path, options, output_file, i)

	def _openscad(self, scad_file_path, options, output_file, i):
		cmd = self.openscad_path + " " + scad_file_path + " -o " + output_file + " " + options

		if self.verbose_lvl >= 1:
			print ">>>" + cmd
		err = None if self.verbose_lvl >= 2 else open(os.devnull, 'w')
		out = None if self.verbose_lvl == 3 else open(os.devnull, 'w')

		p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = err)
		self.process.append(p)

		if len(self.process) >= self.nb_job_slots:
			p.wait()

	def signal_handler(self, signal, frame):
		import sys
		print "\n\nCompilation interrupted by the user."
		print self.nb_created, "file" + ("s" if self.nb_created > 1 else "") + " were created."
		print "Tip : You can continue this work with -s option."
		sys.exit(0)