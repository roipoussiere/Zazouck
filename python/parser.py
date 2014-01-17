#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazoucko.
# Zazoucko is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazoucko is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazoucko. If not, see <http://www.gnu.org/licenses/>.

import argparse, multiprocessing, tempfile, os
from datetime import datetime as date
from os import path as op
tmp_dir = tempfile.gettempdir()
cwd_dir = os.getcwd()

def _correct_input(string):
	if not op.exists(string):
		raise argparse.ArgumentTypeError("Filename %r doesn\'t exists in this directory." % string)

	if not op.isdir(string) and op.splitext(string)[1] not in (".stl", ".csv"):
		raise argparse.ArgumentTypeError("%r is not a .stl, a .csv file or a foler." % string)
	return string


def parser(): 
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description = """\
                               *** Zazoucko ***
This program allows you to build constructions, with generating files to print
from your model. It works in 2 times: first, it build a .csv table file (very
fast) describing the parts, then it compile this one into a lot of .stl files
(can be long).""",
		epilog = """\
Author: Nathanaël Jourdane - nathanael@jourdane.net
Zazoucko is licensed under GNU GPLv3: www.gnu.org/licenses/gpl-3.0.html""")
	
	# ok
	parser.add_argument('input_path', action = 'store',
		type = _correct_input,
		help = '3d model (.stl) or table (.csv) path of your model or model directory if it\'s already compiled. The program will automatically generates the .stl files according to the file type.')

	# ok
	parser.add_argument('-v', '--version', action='version',                    
		version = "Zazoucko version " + str(date.now().year-2013) + "." + str(date.now().month) + "." + str(date.now().day), help = 'Show program version and exit.')

	# ok
	parser.add_argument('-b', '--build-only', action = 'store', nargs = '?',
		dest = 'table_path', type = argparse.FileType('w'), default = None, const = op.join(tmp_dir, "_"),
		help = 'Build only table (.csv) as TABLE_PATH (projet_name.csv by default), without compile stl files.')
	
	# ok
	parser.add_argument('-e', '--export-dir', action = 'store',
		dest = 'export_dir', default = None,
		help = 'Directory where .stl files will be exported (./projet_name/ by default)')
	
	# TODO
	parser.add_argument('-p', '--param-path', action = 'store',
		dest = 'parameter_path', type = argparse.FileType('r'), default = None,
		help = 'Parameters file path, containing parts parameters.')
	
	# ok
	parser.add_argument('-t', '--test', action = 'store_true',
		dest = 'test', default = False,
		help = 'The files are quickly compiled for testing, not able to be print.')

	# ok
	parser.add_argument('-S', '--sort', action = 'store_false',
		dest = 'shuffle', default = True,
		help = 'Doesn\'t shuffle the list of corners and polygons in random order.')
	
	# ok
	parser.add_argument('-s', action = 'store',
		dest = 'start_from', type = int, default = 0,
		help = 'Start compilation from line xx in the .csv file.')

	# ok
	parser.add_argument('-f', action = 'store',
		dest = 'finish_at', type = int, default = 0,
		help = 'Finish compilation at line xx in the .csv file.')
	
	# ok
	parser.add_argument('-d', '--documentation', action = 'store', nargs = '?',
		dest = 'doc_dir', default = None, const = op.join(tmp_dir, "_"),
		help = 'Build a nice document in DOC_DIR (./doc by default), to help you to build your construction easily.')
	
	# ok
	parser.add_argument('-V', '--verbose-cmd', action = 'store', nargs = '?',
		dest = 'verbose', type=int, choices=xrange(0, 4), default = 0, const = 1,
		help = 'Verbose level: 0 = nothing, 1 = OpenScad calls (default value), 2 = OpenScad warning messages, 3 = all OpenScad messages.')

	# ok
	parser.add_argument('-D', '--details', action = 'store', nargs = '?',
		dest = 'details_path', type = argparse.FileType('w'), default = None, const = op.join(cwd_dir, "details.txt"),
		help = 'Export details about the model (corners position, polygons, corners_network, edges, etc.) in DETAILS_PATH (./details.txt by default).')
	
	parser.add_argument('-m', '--make_full_model', action = 'store', nargs = '?',
		dest = 'full_model_path', type = argparse.FileType('w'), default = None, const = op.join(tmp_dir, "_"),
		help = 'Create the 3d model of the construction in FULL_MODEL_PATH (./full_model.stl by default).')

	# ok
	parser.add_argument('-j', '--jobs', action = 'store', nargs = '?',
		dest = 'nb_job_slots', type = int, default = 1, const = multiprocessing.cpu_count(),
		help = 'Compile NB_JOB_SLOTS parts simultaneously (the number of cores on your computer by default).')

	return parser.parse_args()