#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import random, math
from random import randint
import corner, polygon, edge

class Solid: # TODO : singleton
	# def __init__(self): # à tester
	# 	self.polygons = []
	# 	self.corners = []
	# 	self.edges = []
	polygons = []
	corners = []
	edges = []
	
	def get_nb_corners(self): return len(self.corners)	
	def get_nb_polygons(self): return len(self.polygons)
	
	def _get_position_by_corner_id(self, corner_id):
		position = False
		for corner in self.corners:
			if corner.get_id() == corner_id:
				position = corner.get_position()
				break
		return position

	def fill_corners(self, _model):
		positions = []
		
		for polygon_model in _model:
			for point in polygon_model:
				if positions.count(point) == 0:
					positions.append(point)
		
		id_list = []
		for position in positions:
			while True:
				id = randint(1,32766) # values 0 and 32767 are not visible on a MQRcode
				if id not in id_list:
					id_list.append(id)
					break

			self.corners.append(corner.Corner(position, id))
	
	def fill_polygons(self, _model):
		id_list = []
		for polygon_model in _model:

			while True:
				id = randint(1,32766)
				if id not in id_list:
					id_list.append(id)
					break

			poly = polygon.Polygon(id)
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
	
	def set_angles(self):
		for corner in self.corners:
			for target in corner.get_connected_corners():
				corner.set_angles(self._get_position_by_corner_id(target))
	
	def set_datas(self):
		for corner in self.corners:
			corner.set_data()
	
	def fill_edges(self):
		id_list = []
		for i in range(self.get_nb_corners()):
			for cc in self.corners[i].get_connected_corners():
				add = True
				for ed in self.edges:
					if (i,cc) == ed.get_extremities() or (cc,i) == ed.get_extremities():
						add = False
						break;
				if add:
					while True:
						id = randint(1,32766)
						if id not in id_list:
							id_list.append(id)
							break
					px = pow(self._get_position_by_corner_id(cc)[0] - self.corners[i].get_position()[0], 2)
					py = pow(self._get_position_by_corner_id(cc)[1] - self.corners[i].get_position()[1], 2)
					pz = pow(self._get_position_by_corner_id(cc)[2] - self.corners[i].get_position()[2], 2)
					#deplacer dans corner: d = c1.dist(c2)
					dist = math.sqrt( px + py + pz)
					e = edge.Edge(id, (i, cc), dist)
					self.edges.append(e)

	def shuffle(self):
		random.shuffle(self.corners)
		random.shuffle(self.polygons)
		random.shuffle(self.edges)

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
				f_debug.write(str(i+1) + ": " + str(corner.get_id()) + " - " + str(corner.get_position()) + " - " + str(corner.get_connected_corners()) + "\n")

			f_debug.write("\n*** Polygons connexions ***\n\n")
			for i, polygon in enumerate(self.polygons):
				f_debug.write(str(i+1) + ": " + str(polygon.get_id()) + " - " + str(polygon.get_corners()) + "\n")

			f_debug.write("\n*** Edges connexions and length ***\n\n")
			for i, edge in enumerate(self.edges):
				f_debug.write(str(i+1) + ": " + str(edge.get_id()) + " - " + str(edge.get_extremities()) + " - " + str(edge.get_length()) + "\n")

			f_debug.write("\n*** Angles ***\n\n")
			for i, corner in enumerate(self.corners):
				f_debug.write(str(i+1) + ": " + str(corner.get_id()) + " - " + str(corner.get_angles()) + "\n")

	def build_corners_table(self, f_table_path, start_from, finish_at, shuffle):
		infos = str(self.get_nb_corners()) + " corners," + str(self.get_nb_polygons()) + " polygons\n"
		labels = "id,x,y,z,rod 1-V,rod 1-H,rod 2-V,rod 2-H,rod 3-V,rod 3-H,rod 4-V,rod 4-H,rod 5-V,rod 5-H,rod 6-V,rod 6-H,rod 7-V,rod 7-H,rod 8-V,rod 8-H\n"
		finish_at = self.get_nb_corners() if finish_at == 0 else finish_at+1

		right_limit = self.get_nb_corners()-finish_at
		for i in range(start_from):
			self.corners.pop(0)
		for i in range(right_limit):
			self.corners.pop()

		if shuffle:
			self.shuffle()

		with open(f_table_path, 'w') as f_table:
			f_table.write(infos)
			f_table.write(labels)
			for corner in self.corners:
				f_table.write(corner.get_data())

				################### TODO ##############
	def build_edges_table(self, f_table_path, start_from, finish_at, shuffle):
		print "build_edges_table()"