#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import random, math, re, tempfile, os
from random import randint
from os import path as op
import corner, polygon, edge

class Solid: # TODO : singleton
	def __init__(self, input_stl_path):
		self.input_stl_path = input_stl_path
		self.polygons = list()
		self.corners = list()
		self.edges = list()

		self._create_solid()
	
	def get_nb_corners(self): return len(self.corners)	
	def get_nb_polygons(self): return len(self.polygons)
	def get_nb_edges(self): return len(self.edges)
	
	def _create_solid(self):
		cleaned_path = op.join(tempfile.gettempdir(), "zazouck_cleaned")
		self._clean_file(cleaned_path)
		model = self._file_to_model(cleaned_path)
		
		os.remove(cleaned_path)

		self.fill_corners(model)
		self.fill_polygons(model)
		del model
		
		self.set_connected_corners()
		self.set_corners_data()

		self.fill_edges()
		self.set_edges_data()

		#s.merge_coplanar_polygons() # TODO


	def _get_corner_by_id(self, corner_id):
		corner = False
		for c in self.corners:
			if c.get_id() == corner_id:
				corner = c
		return corner

	def _get_random_id(self, id_list):
		MAX_ID = 32766 # values 0 and 32767 are not visible on a MQRcode
		while True:
			id = randint(1, MAX_ID)
			if id not in id_list:
				id_list.append(id)
				return id
		return False

	def fill_corners(self, _model):
		positions = list()
		id_list = list()

		for polygon_model in _model:
			for point in polygon_model:
				if positions.count(point) == 0:
					positions.append(point)
		
		for position in positions:
			self.corners.append(corner.Corner(self._get_random_id(id_list), position))
	
	def fill_polygons(self, _model):
		id_list = list()

		for polygon_model in _model:

			poly = polygon.Polygon(self._get_random_id(id_list))
			corners_pos = []
			for position in polygon_model:
				for corner in self.corners:
					if corner.get_position() == position:
						corner_id = corner.get_id()
						corners_pos.append(corner.get_position())
						break
				poly.add_corner(corner_id)
			poly.set_normal(corners_pos)
			self.polygons.append(poly)
		
	def set_connected_corners(self):
		for corner in self.corners:
			corner.set_connected_corners(self.polygons)
	
	# TODO: à déplacer
	def set_corners_data(self):
		for corner in self.corners:
			for target in corner.get_connected_corners():
				corner.set_angles(self._get_corner_by_id(target).get_position())

		for corner in self.corners:
			corner.set_data()

	def set_edges_data(self):
		for edge in self.edges:
			edge.set_data()

	def fill_edges(self):
		id_list = list()
		extremities = list()

		for c1 in self.corners:
			for c2 in c1.get_connected_corners():
				if (c1.get_id(),c2) not in extremities and (c2,c1.get_id()) not in extremities:
					extremities.append((c1.get_id(), c2))
					self.edges.append(edge.Edge(
							self._get_random_id(id_list), c1, self._get_corner_by_id(c2)))

		for e in self.edges:
			e.set_length()
			e.set_position()
			e.set_rotation()

	def _find_coplanar_polygons(self):
		normals = []
		coplanar_polys = []
		for poly in self.polygons:
			normal = poly.get_normal()
			for i, n in enumerate(normals):
				if n == normal:
					coplanar_polys.append((poly.get_id(), self.polygons[i].get_id()))
			else:
				normals.append(normal)
		return coplanar_polys

	#def merge_coplanar_polygons(self): # TODO
	#	print "coplanar_polygons:", self._find_coplanar_polygons();
	
	def display(self, debug_path):
		with open(debug_path, 'w') as f_debug:
			f_debug.write("*** Corners position and connexions ***\n\n")
			for i, corner in enumerate(self.corners):
				f_debug.write(str(i+1) + ": " + str(corner) + "\n")

			f_debug.write("\n*** Polygons connexions ***\n\n")
			for i, polygon in enumerate(self.polygons):
				f_debug.write(str(i+1) + ": " + str(polygon) + "\n")

			f_debug.write("\n*** Edges position and length ***\n\n")
			for i, edge in enumerate(self.edges):
				f_debug.write(str(i+1) + ": " + str(edge) + "\n")

			f_debug.write("\n*** Angles ***\n\n")
			for i, corner in enumerate(self.corners):
				f_debug.write(str(i+1) + ": " + corner.print_angles() + "\n")

	def build_corners_table(self, corners_table_path):
		infos = str(self.get_nb_corners()) + " corners," + str(self.get_nb_polygons()) + \
				" polygons," + str(self.get_nb_edges()) + " edges\n"

		labels = "id,posX,posY,posZ,rod 1-V,rod 1-H,rod 2-V,rod 2-H,rod 3-V,rod 3-H,\
				rod 4-V,rod 4-H,rod 5-V,rod 5-H,rod 6-V,rod 6-H,rod 7-V,rod 7-H,rod 8-V,rod 8-H\n"

		with open(corners_table_path, 'w') as table:
			table.write(infos)
			table.write(labels)
			for corner in self.corners:
				table.write(corner.get_data())

	def build_edges_table(self, edges_table_path):
		infos = str(self.get_nb_corners()) + " corners," + \
				str(self.get_nb_polygons()) + " polygons," + str(self.get_nb_edges()) + " edges\n"
		labels = "id,posX,posY,posZ,rotX,rotY,rotZ,length\n"

		with open(edges_table_path, 'w') as table:
			table.write(infos)
			table.write(labels)
			for edge in self.edges:
				table.write(edge.get_data())

	def _clean_file(self, cleaned_path):
		words = 'vertex', 'endloop'
		with open(self.input_stl_path, 'r') as f_stl, open(cleaned_path, 'w') as f_cleaned_stl:
			for line in f_stl:
				if any(word in line for word in words):
					line = re.sub('^endloop.*', '|', line.lstrip())
					line = line.replace("vertex", "")
					line = line.lstrip().replace(" ", ",")
					line = line.replace("\n", ";")
					line = line.replace("|;", "\n")
					f_cleaned_stl.write(line)

	def _file_to_model(self, cleaned_path):
		model = list()
		with open(cleaned_path) as f_cleaned_stl:
			for line in f_cleaned_stl:
				line = re.sub('[;\n]$', '\n', line)
				p = []
				for point in line.split(';'):
					pos_str = point.split(',')
					pos_int = []
					for nb in pos_str:
						pos_int.append(float(nb))
					p.append(pos_int)
			
				model.append(p)

		return model