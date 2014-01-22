#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import solid
from os import path as op

class Roddy:

	def __init__(self, input_stl_path, output_dir):
		self.input_stl_path = input_stl_path
		self.solid = solid
		self.output_dir = output_dir
		self.solid = solid.Solid(input_stl_path)
		
		#export.Export(openscad_path, output_dir, scad_dir, opt.jobs, opt.verbose, opt.test)

	def make_tables(self):
		self.solid.build_corners_table(op.join(self.output_dir, "corners.csv"))
		self.solid.build_edges_table(op.join(self.output_dir, "edges.csv"))

		print "Successfully created table files in " + self.output_dir + "."

		self.solid.display(op.join(self.output_dir, "details.txt"))