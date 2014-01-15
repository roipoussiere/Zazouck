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

class Export: # TODO : singleton

	def __init__(self, openscad_path, table_path, zazoucko_scad_dir, export_dir, nb_job_slots, verbose_lvl, low_qlt):
		self.openscad_path = openscad_path
		self.table_path = table_path
		self.zazoucko_scad_dir = zazoucko_scad_dir
		self.export_dir = export_dir
		self.nb_job_slots = nb_job_slots
		self.verbose_lvl = verbose_lvl
		self.low_qlt = low_qlt
		self.process = list()

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

	def make_pictures(self, img_dir):
		PICT_WIDTH = 150

		nb_corners = self._get_nb_lines(self.table_path)-2
		t_init = time.time()
		corner_scad_path = op.join(self.zazoucko_scad_dir, ("corner_light.scad" if self.low_qlt else "corner.scad"))

		print "\n*** Creating pictures in " + img_dir + " ***"
		with open(self.table_path, 'r') as f_table:		
			print f_table.readline()
			f_table.readline()

			for i, line in enumerate(f_table):
				self._print_status(i, nb_corners, t_init, True)
				corner_id = line[0:line.index(",")]
				start = [m.start() for m in re.finditer(r",",line)][3]+1 # position de départ des données
				data = line.rstrip('\n')[start:]

				data_options = "-D 'id=" + str(corner_id) + "; angles=\"" + data + "\"'"
				pict_options = "--imgsize=" + str(PICT_WIDTH) + "," + str(PICT_WIDTH) + " --camera=0,0,0,0,45,45,45"
				options = data_options + " " + pict_options
				output_file = op.join(img_dir, corner_id + ".png")
				
				self.openscad(corner_scad_path, options, output_file)

	def make_stls(self):
		t_init = time.time()
		nb_corners = self._get_nb_lines(self.table_path)-2
		corner_scad_path = op.join(self.zazoucko_scad_dir, ("corner_light.scad" if self.low_qlt else "corner.scad"))
		
		print "\n*** Compilation started.", nb_corners, "stl files will be created in", self.export_dir, "***\n"

		with open(self.table_path, 'r') as f_table:
			print "Model details: " + f_table.readline().rstrip('\n').replace(",", ", ") + "."
			if self.nb_job_slots == 1:
				print "Tip : You can parallelize this task on several cores with -j option."
				print "\nCompiling the first stl file, please wait..."
			else:
				print "\nCompiling", self.nb_job_slots if self.nb_job_slots < nb_corners else nb_corners, "stl files simultaneously, please wait..."
			f_table.readline()

			nb_created = 0
			for i, line in enumerate(f_table):
				corner_id = line[0:line.index(",")]
				#self._print_status(i, nb_corners, t_init)
				start = [m.start() for m in re.finditer(r",",line)][3]+1 # position de départ des données
				data = line.rstrip('\n')[start:]
				options = "-D 'id=" + str(corner_id) + "; angles=\"" + data + "\"'"
				output_file = op.join(self.export_dir, corner_id + ".stl")

				self.openscad(corner_scad_path, options, output_file, corner_id)
				nb_created = self.end_of_process(nb_created, nb_corners, t_init)
	
			while self.process:
				nb_created = self.end_of_process(nb_created, nb_corners, t_init)

		total_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
		print "\n*** Finished! ***"
		print i+1, "stl files successfully created in " + total_time + "."	

	def end_of_process(self, nb_created, nb_corners, t_init):
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
		for i, p in enumerate(self.process):
			if p[0].poll() == 0:
				del self.process[i]
				nb_created += 1
				print spent + ": Created file " + str(nb_created) + "/" + str(nb_corners) + ", n°" + str(p[1]) + "."
		return nb_created

	def make_model(self, full_model_path):
		print "Creating full model ", full_model_path
		corner_move_scad_path = op.join(self.zazoucko_scad_dir, "move_part.scad")

		with open(self.table_path, 'r') as f_table:
			f_table.readline()
			f_table.readline()
			
			for line in f_table:
				data = line.split(",")[0:4]
				name = data[0] + ".stl"
				options = "-D 'file=\"" + file_name + "\"; tx=" + data[1] + "; ty=" + data[2] + "; tz=" + data[3] + "'"
				self.openscad(corner_move_scad_path, options, full_model_path)

	def openscad(self, scad_file_path, options, output_file, i):
		cmd = self.openscad_path + " " + scad_file_path + " -o " + output_file + " " + options

		if self.verbose_lvl >= 1:
			print ">>>" + cmd
		err = None if self.verbose_lvl >= 2 else open(os.devnull, 'w')
		out = None if self.verbose_lvl == 3 else open(os.devnull, 'w')

		p = subprocess.Popen(shlex.split(cmd), stdout = out, stderr = err)
		self.process.append((p,i))

		if len(self.process) >= self.nb_job_slots:
			p.wait()