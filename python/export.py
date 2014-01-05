#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Ouack.
# Ouack is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Ouack is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Ouack. If not, see <http://www.gnu.org/licenses/>.

import time, os

pict_width = 150

def get_nb_lines(input_path):
	nb_lines = 0
	with open(input_path, 'r') as f_input:
		for line in f_input: nb_lines += 1
	return nb_lines

def print_line(i, nb_corners, t_init, picture=False):
	f_type = "picture" if picture else "stl file"
	print "Compiling " + f_type + " " + str(i+1) + "/" + str(nb_corners),
	print "(" + str(int(round(i/float(nb_corners)*100))) + "%)",
	if i==0:
		print "- please wait... "
	else:
		spent = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
		remaining = time.strftime("%Hh%Mm%Ss", time.gmtime((time.time()-t_init)/i*(nb_corners-i)))
		print "- started for " + spent + ", please wait", remaining + "."

def compile_pictures(doc_dir, table_path, openscad_path, scad_file, verbose_lvl):
	create_dir(doc_dir)
	nb_corners = get_nb_lines(table_path)-2
	t_init = time.time()

	print "\n*** Creating pictures in " + doc_dir + " ***"
	with open(table_path, 'r') as f_table:		
		print f_table.readline()
		f_table.readline()

		i = 0
		for line in f_table:
			print_line(i, nb_corners, t_init, True)
			name = line[0:5]
			data_options = "-D 'data=\"" + line.rstrip('\n') + "\"'"
			pict_options = "--imgsize=" + str(pict_width) + "," + str(pict_width) + " --camera=0,0,0,0,0,0,90"
			options = data_options + " " + pict_options
			output_file = doc_dir + name + ".png"
			
			openscad(scad_file, options, output_file, openscad_path, verbose_lvl)
			i += 1

def make_parts(table_path, export_dir, verbose_lvl, openscad_path, scad_file, doc_dir):
	nb_corners = get_nb_lines(table_path)-2
	t_init = time.time()
	
	if doc_dir != None:
		compile_pictures(doc_dir, table_path, openscad_path, scad_file, verbose_lvl)

	print "\n*** Compilation started.", nb_corners, "files will be created in", export_dir, "***"

	with open(table_path, 'r') as f_table:
		print f_table.readline()
		f_table.readline()
		
		#for i in range(options.start_from):
		#	f_table.readline() # À compléter		
		
		i = 0
		for line in f_table:
			print_line(i, nb_corners, t_init)
			name = line[0:5]
			i+=1
			options = "-D 'data=\"" + line.rstrip('\n') + "\"'"
			output_file = export_dir + name + ".stl"

			openscad(scad_file, options, output_file, openscad_path, verbose_lvl)

	total_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t_init))
	print "\n*** Finished! ***"
	print i, "stl files successfully created in " + total_time + "."

def openscad(scad_file, options, output_file, openscad_path, verbose_lvl):
	redirection = "" if verbose_lvl == 3 else "> /dev/null" if verbose_lvl == 2 else "> /dev/null 2> /dev/null"
	cmd = openscad_path + " " + scad_file + " -o " + output_file + " " + options + " " + redirection
	if verbose_lvl >= 1: print "    " + cmd
	os.system(cmd)
