#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Ouack.
# Ouack is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Ouack is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Ouack. If not, see <http://www.gnu.org/licenses/>.
    
import argparse, os
import solid, stl, export

tmp_path = "/tmp/"
openscad_path = "openscad"
f_scad_path = "./ouack.scad"

def parser() :
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description = 'Ouack : the Open-source Universal Awesome Construction Kit. This program allows you to build constructions, with generating files to print from your model. It works in 2 times : first, it build a .csv table file (very fast), then it compile this one into a lot of .stl files (can be long).',
			epilog = '')
	
	parser.add_argument('input_path', action = 'store',
		type = argparse.FileType('r'),
		help = '.stl (3d model) or .csv (table) path of your model.')
	
	parser.add_argument('-b', '--build-only', action = 'store_false',
		dest = 'build_only', default = None,
		help = 'Only build table (.csv), without compiling stl files.')
	
	parser.add_argument('-c', '--compile-only', action = 'store',
		dest = 'table_path', type = argparse.FileType('r'), default = None,
		help = 'Compile stl files from TABLE_PATH table.')
	
	parser.add_argument('-e', '--export-path', action = 'store',
		dest = 'export_path', type = argparse.FileType('w'), default = None,
		help = 'Path where .stl files will be exported (./stl/ by default)')
	
	parser.add_argument('-p', '--param-path', action = 'store',
		dest = 'parameter_path', type = argparse.FileType('r'), default = None,
		help = 'Parameters file path, containing parts parameters.')
	
	parser.add_argument('-r', action = 'store_true',
		dest = 'shuffle', default = False,
		help = 'Shuffle lists of corners, polygons and edges in random order.')
		
	parser.add_argument('-s', action = 'store',
		dest = 'start_from', type = int, default = None,
		help = 'Start compilation from line xx in the .csv file.')

	parser.add_argument('-f', action = 'store',
		dest = 'finish_at', type = int, default = None,
		help = 'Finish compilation at line xx in the .csv file.')
	
	parser.add_argument('-d', '--doc', action = 'store',
		dest = 'doc_path', type = argparse.FileType('w'), default = None,
		help = 'Build pictures of generated parts.')
	
	parser.add_argument('-v', '--verbose', action = 'store_true',
		dest = 'verbose', default = False,
		help = 'Enable OpenScad messages.')

	parser.add_argument('-D', '--debug', action = 'store',
		dest = 'debug_path', type = argparse.FileType('w'), default = None,
		help = 'Export details about the model (corners position, polygons, corners_network, edges, etc.) in DETAILS_PATH.')
	
	return parser.parse_args()

def make_csv(stl_path, table_path, shuffle, debug_path) :
	cleaned_path = tmp_path + "ouack_cleaned"

	stl.clean_file(stl_path, cleaned_path)
	_model = stl.file_to_model(cleaned_path)
	os.remove(cleaned_path)
	
	s = solid.Solid()
	s.fill_corners(_model)
	s.fill_polygons(_model)
	del _model
	
	s.set_connected_corners()
	s.set_angles()
	s.set_datas()
	#s.merge_coplanar_polygons()
	if shuffle :
		s.shuffle()
	s.build_csv(table_path)
	
	if debug_path != None :
		s.display(debug_path)

def main() :
	opt = parser()
	
	input_path = opt.input_path.name
	table_path = None if opt.table_path == None else opt.table_path.name
	export_path = None if opt.export_path == None else opt.export_path.name
	parameter_path = None if opt.parameter_path == None else opt.parameter_path.name
	doc_path = None if opt.doc_path == None else opt.doc_path.name
	debug_path = None if opt.debug_path == None else opt.debug_path.name
	
	if table_path != None :
		table_path = input_path
	else :
		if not opt.build_only :
			table_path = tmp_path + "table.csv"
		make_csv(input_path, table_path, opt.shuffle, debug_path)

	if not opt.build_only :
		export_path = "./stl/" if export_path == None else export_path
		export.make_parts(table_path, export_path, opt.verbose, openscad_path, f_scad_path)

main()
