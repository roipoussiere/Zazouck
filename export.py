#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Ouack.
# Ouack is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Ouack is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Ouack. If not, see <http://www.gnu.org/licenses/>.

import time, shutil, os

def get_nb_lines(input_path) :
	nb_lines = 0
	with open(input_path, 'r') as f_input :
		for line in f_input : nb_lines += 1
	return nb_lines
          
def print_line(i, nb_corners, t_init) :
	print "Compiling file " + str(i+1) + "/" + str(nb_corners),
	print "(" + str(int(round(i/float(nb_corners)*100))) + "%)",
	if i==0 :
		print "- please wait... "
	else :
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
		remaining = time.strftime("%Hh%Mm%Ss", time.gmtime((time.time()-t_init)/i*(nb_corners-i)))
		print "- started for " + spent + ", please wait", remaining + "."

def create_dir(export_path) :
	export = os.path.dirname(export_path)
	if os.path.exists(export):
		shutil.rmtree(export_path)
	os.makedirs(export)

def make_parts(table_path, export_path, verbose, openscad_path, f_scad_path, ) :
	redirection = "" if verbose else "> /dev/null"
	nb_corners = get_nb_lines(table_path)-1
	print "Compilation started.", nb_corners, "files will be created in", export_path
	
	with open(table_path, 'r') as f_table :		
		f_table.readline()
		create_dir(export_path)
		t_init = time.time()
		
		#for i in range(options.start_from) :
		#	f_table.readline() # À compléter		
	
		i = 0
		for line in f_table :
			name = line[0:5]
			print_line(i, nb_corners, t_init)
			i+=1
			data_option = "-D 'data=\"" + line.rstrip('\n') + "\"'"
			export_stl = "-o " + export_path + name + ".stl"
			#export_pict = "-o " + options.picture_path + name + ".png"
			
			os.system(openscad_path + " " + f_scad_path + " " + data_option + " " + export_stl + " " + redirection)

			#if options.picture_path != None :
			#	os.system(openscad_path + " " + f_scad_path + " " + data_option + " " + export_pict + " " + redirection)

	total_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
	print "\n*** Finished! ***"
	print i, "stl files successfully created in " + total_time + "."
