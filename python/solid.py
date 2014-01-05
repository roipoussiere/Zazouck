#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Ouack.
# Ouack is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Ouack is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Ouack. If not, see <http://www.gnu.org/licenses/>.

import random, math
import corner, polygon, edge

class Solid: #singleton
#	def __init__(self): # marche pas
	polygons = []
	corners = []
	edges = []
	
	def get_nb_corners(self): return len(self.corners)	
	def get_nb_polygons(self): return len(self.polygons)
	
	#retirer les id, c'est pourri
	def get_position_by_corner_id(self, corner_id):
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
		
		i=0
		for position in positions:
			self.corners.append(corner.Corner(position, i))
			i+=1
	
	def fill_polygons(self, _model):
		i=0
		for polygon_model in _model:
			poly = polygon.Polygon(i)
			for position in polygon_model:
				for corner in self.corners:
					if corner.get_position() == position:
						corner_id = corner.get_id()
						break
				poly.add_corner_id(corner_id)
			self.polygons.append(poly)
			i+=1
		
	def set_connected_corners(self):
		for corner in self.corners:
			corner.set_connected_corners(self.polygons)
	
	def set_angles(self):
		for corner in self.corners:
			for target in corner.get_connected_corners():
				corner.set_angles(self.get_position_by_corner_id(target))
	
	def set_datas(self):
		for corner in self.corners:
			corner.set_data()
	
	def fill_edges(self):
		edge_id = 0
		for i in range(self.get_nb_corners()):
			for cc in self.corners[i].get_connected_corners():
				add = True
				for ed in self.edges:
					if (i,cc) == ed.get_extremities() or (cc,i) == ed.get_extremities():
						add = False
						break;
				if add:
					edge_id += 1
					px = pow(self.get_position_by_corner_id(cc)[0] - self.get_position_by_corner_id(i)[0], 2)
					py = pow(self.get_position_by_corner_id(cc)[1] - self.get_position_by_corner_id(i)[1], 2)
					pz = pow(self.get_position_by_corner_id(cc)[2] - self.get_position_by_corner_id(i)[2], 2)
					#deplacer dans corner: d = c1.dist(c2)
					dist = math.sqrt( px + py + pz)
					e = edge.Edge(edge_id, (i, cc), dist)
					self.edges.append(e)

	def shuffle(self):
		random.shuffle(self.corners)
		random.shuffle(self.polygons)
		random.shuffle(self.edges)

#	def merge_coplanar_polygons():
#		for poly in polygons():
#			poly.merge_coplanar()
	
	def display(self, debug_path):
		with open(debug_path, 'w') as f_debug:
			f_debug.write("*** Corners position and connexions ***\n\n")
			for corner in self.corners:
				f_debug.write(str(corner.get_id()) + ": " + str(corner.get_position()))
				f_debug.write(" - " + str(corner.get_connected_corners()) + "\n")

			f_debug.write("\n*** Polygons connexions ***\n\n")
			for polygon in self.polygons:
				f_debug.write(str(polygon.get_id()) + ": " + str(polygon.get_corners()) + "\n")

			f_debug.write("\n*** Edges length and connexions ***\n\n")
			for edge in self.edges:
				f_debug.write(str(edge.get_id()) + ": " + str(edge.get_extremities()) + " - " + str(edge.get_length()) + "\n")

			f_debug.write("\n*** Parameters ***\n\n")
			for corner in self.corners:
				f_debug.write(str(corner.get_id()) + ": " + str(corner.get_data()))

	def build_csv(self, f_table_path):
		infos = "Model details: " + str(self.get_nb_corners()) + " corners, " + str(self.get_nb_polygons()) + " polygons.\n"
		labels = "Name,rod 1-H,rod 1-V,rod 2-H,rod 2-V,rod 3-H,rod 3-V,rod 4-H,rod 4-V,rod 5-H,rod 5-V,rod 6-H,rod 6-V,rod 7-H,rod 7-V,rod 8-H,rod 8-V\n"
		with open(f_table_path, 'w') as f_table:
			f_table.write(infos)
			f_table.write(labels)
			for corner in self.corners:
				f_table.write(corner.get_data())
