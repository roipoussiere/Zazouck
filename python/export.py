#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazoucko.
# Zazoucko is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazoucko is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazoucko. If not, see <http://www.gnu.org/licenses/>.

import time, os, re, tempfile
import solid, stl

class Export: # TODO : singleton

	def __init__(self, openscad_path, table_path, zazoucko_scad_dir, export_dir, verbose_lvl, low_qlt):
		self.openscad_path = openscad_path
		self.table_path = table_path
		self.zazoucko_scad_dir = zazoucko_scad_dir
		self.export_dir = export_dir
		self.verbose_lvl = verbose_lvl
		self.low_qlt = low_qlt

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
		cleaned_path = tempfile.gettempdir() + "/" + "zazoucko_cleaned" # os.path.join

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
		s.merge_coplanar_polygons()

		s.build_csv(self.table_path, start_from, finish_at, shuffle)
		
		if details_path != None:
			s.display(details_path)

		print "Successfully created table file " + self.table_path + "."

	def make_pictures(self, img_dir):
		PICT_WIDTH = 150

		nb_corners = self._get_nb_lines(self.table_path)-2
		t_init = time.time()
		corner_scad_path = self.zazoucko_scad_dir + ("corner_light.scad" if self.low_qlt else "corner.scad")

		print "\n*** Creating pictures in " + img_dir + " ***"
		with open(self.table_path, 'r') as f_table:		
			print f_table.readline()
			f_table.readline()

			for i, line in enumerate(f_table):
				self._print_status(i, nb_corners, t_init, True)
				corner_id = line[0:line.index(",")]
				start = [m.start() for m in re.finditer(r",",line)][3]+1 # position de départ des données
				data = line.rstrip('\n')[start:]

				data_options = "-D 'id=" + str(corner_id) + "; data=\"" + data + "\"'"
				pict_options = "--imgsize=" + str(PICT_WIDTH) + "," + str(PICT_WIDTH) + " --camera=0,0,0,0,45,45,45"
				options = data_options + " " + pict_options
				output_file = img_dir + corner_id + ".png"
				
				self.openscad(corner_scad_path, options, output_file)

	def make_stls(self):
		nb_corners = self._get_nb_lines(self.table_path)-2
		t_init = time.time()
		corner_scad_path = self.zazoucko_scad_dir + ("corner_light.scad" if self.low_qlt else "corner.scad")
		
		print "\n*** Compilation started.", nb_corners, "files will be created in", self.export_dir, "***"

		with open(self.table_path, 'r') as f_table:
			print "Model details: " + f_table.readline().rstrip('\n').replace(",", ", ") + "."
			f_table.readline()
			
			for i, line in enumerate(f_table):
				self._print_status(i, nb_corners, t_init)
				corner_id = line[0:line.index(",")]
				start = [m.start() for m in re.finditer(r",",line)][3]+1 # position de départ des données
				data = line.rstrip('\n')[start:]
				options = "-D 'id=" + str(corner_id) + "; data=\"" + data + "\"'"
				output_file = self.export_dir + corner_id + ".stl"

				self.openscad(corner_scad_path, options, output_file)

		total_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
		print "\n*** Finished! ***"
		print i, "stl files successfully created in " + total_time + "."	

	def make_model(self, full_model_path):
		print "Creating full model ", full_model_path
		corner_move_scad_path = self.zazoucko_scad_dir + "move_part.scad"

		with open(self.table_path, 'r') as f_table:
			f_table.readline()
			f_table.readline()
			
			for line in f_table:
				t = line.split(",")[1:4]
				name = line[:5] + ".stl"
				options = "-D 'file=\"" + file_name + "\"; tx=" + t[0] + "; ty=" + t[1] + "; tz=" + t[2] + "'"
				self.openscad(corner_move_scad_path, options, full_model_path)

	def openscad(self, scad_file, options, output_file):
		redirection = "" if self.verbose_lvl == 3 else "> /dev/null" if self.verbose_lvl == 2 else "> /dev/null 2> /dev/null"
		cmd = self.openscad_path + " " + scad_file + " -o " + output_file + " " + options + " " + redirection
		if self.verbose_lvl >= 1: print ">>>" + cmd
		os.system(cmd)
