#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import argparse, multiprocessing, tempfile, os
from datetime import datetime as date
from os import path as op
tmp_dir = tempfile.gettempdir()
cwd_dir = os.getcwd()
version = str(date.now().year-2013) + "." + str(date.now().month) + "." + str(date.now().day)

def _correct_input(string):
	if not op.exists(string):
		raise argparse.ArgumentTypeError("Filename %r doesn\'t exists in this directory." % string)

	if not op.isdir(string) and op.splitext(string)[1] not in (".stl", ".csv"):
		raise argparse.ArgumentTypeError("%r is not a .stl, a .csv file or a folder." % string)
	return string


def parser(): 
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description = """\
                               *** Zazouck ***
This program allows you to build constructions, by generating 3D files
from your model. It works in 2 times: first, it build .csv table files
describing the parts (very fast), then it compile this one into a lot
of .stl files (can be long). See README.md for getting started.""",
		epilog = """\
Author: Nathanaël Jourdane - nathanael@jourdane.net
Zazouck is licensed under GNU GPLv3: www.gnu.org/licenses/gpl-3.0.html""")
	
	# TODO: il faut 2 fichiers .csv pour compiler les pièces.
	parser.add_argument('input_path', action = 'store',
		type = _correct_input,
		help = "3d model (stl file) or model directory if it's already created.")

	# 
	parser.add_argument('-o', '--output-dir', action = 'store', default = None,
		type = argparse.FileType('w'),
		help = "Directory where all the files will be exported (current dir. by default)")
	
	# TODO + aujouter valeur par defaut
	parser.add_argument('-p', '--param-path', action = 'store', default = None,
		type = argparse.FileType('r'),
		help = "Load a parameters file from PARAM_PATH, containing the parts parameters.")
		
	# 
	parser.add_argument('-t', '--test', action = 'store_true', default = False,
		help = "The files are quickly compiled for testing, not able to be printed.")

	# 
	parser.add_argument('-s', '--start-from', action = 'store', type = int, default = 0, metavar = 'FIRST_LINE',
		help = "Start compilation from line %(metavar)s in the .csv file.")

	# 
	parser.add_argument('-f', '--finish-at', action = 'store', type = int, default = 0, metavar = 'LAST_LINE',
		help = "Finish compilation at line %(metavar)s in the .csv file.")
	
	# 
	parser.add_argument('-d', '--doc-dir', action = 'store', default = False, metavar = "DIR",
		type = argparse.FileType('w'),
		help = "Assembly instructions directory (OUTPUT_DIR/doc by default).")

	# 
	parser.add_argument('-ns', '--no-stl', action = 'store_false', default = True, dest = "stl",
		help = "Doesn't compile stl files, only build csv tables.")

	# 
	parser.add_argument('-nd', '--no-doc', action = 'store_false', default = True, dest = "doc",
		help = "Doesn't build assembly instructions.")
	
	# 
	parser.add_argument('-ni', '--no-infos', action = 'store_false', default = True, dest = "infos",
		help = "Doesn't make a text file containing informations about the model.")

	# 
	parser.add_argument('-na', '--no-assembly', action = 'store_false', default = True, dest = "assembly",
		help = "Doesn't create the 3d model of the assembly.")

	# 
	parser.add_argument('-nf', '--no-shuffle', action = 'store_false', default = True, dest = "shuffle",
		help = "Doesn't shuffle the lists of corners, polygons and edges.")

	# 
	parser.add_argument('-V', '--verbose', action = 'store', nargs = '?',
		type = int, choices = xrange(1, 4), default = 0, const = 1,
		help = "Verbose level: 1 = OpenScad calls (default value), 2 = OpenScad warnings, 3 = all OpenScad messages.")

	# 
	parser.add_argument('-j', '--jobs', action = 'store', nargs = '?', metavar = "NB_JOBS_SLOTS",
		type = int, default = multiprocessing.cpu_count(),
		help = "Compile %(metavar)s files simultaneously (the number of cores on your computer by default).")

	# 
	parser.add_argument('-v', '--version', action='version',
		version = "Zazouck version " + version, help = "Show program version and exit.")

	return parser.parse_args()