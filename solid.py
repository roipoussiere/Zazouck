#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Ouack.
# Ouack is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Ouack is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Ouack. If not, see <http://www.gnu.org/licenses/>.

import corner, polygon

class Solid : #singleton
#	def __init__(self) : # marche pas
	polygons = []
	corners = []
	
	def get_nb_corners(self) : return len(self.corners)	
	def get_nb_polygons(self) : return len(self.polygons)
	
	#retirer les id, c'est pourri
	def get_position_by_corner_id(self, corner_id) :
		position = False
		for corner in self.corners :
			if corner.get_id() == corner_id :
				position = corner.get_position()
				break
		return position

	def fill_corners(self, _model) :
		positions = []
		
		for polygon_model in _model :
			for point in polygon_model :
				if positions.count(point) == 0:
					positions.append(point)
		
		i=0
		for position in positions :
			self.corners.append(corner.Corner(position, i))
			i+=1
	
	def fill_polygons(self, _model) :
		i=0
		for polygon_model in _model :
			poly = polygon.Polygon(i)
			for position in polygon_model :
				for corner in self.corners :
					if corner.get_position() == position :
						corner_id = corner.get_id()
						break
				poly.add_corner_id(corner_id)
			self.polygons.append(poly)
			i+=1
		
	def set_connected_corners(self) :
		for corner in self.corners :
			corner.set_connected_corners(self.polygons)
	
	def set_angles(self) :
		for corner in self.corners :
			for target in corner.get_connected_corners() :
				corner.set_angles(self.get_position_by_corner_id(target))
	
	def set_datas(self) :
		for corner in self.corners :
			corner.set_data()
	
	def shuffle(self) :
		random.shuffle(self.corners)

#	def merge_coplanar_polygons() :
#		for poly in polygons() :
#			poly.merge_coplanar()
	
	def display(self, debug_path) :
		with open(debug_path, 'w') as f_debug :
			f_debug.write("*** Corners ***\n\n")
			for corner in self.corners :
				f_debug.write(str(corner.get_id()) + " : " + str(corner.get_position()) + "\n")

			f_debug.write("\n*** Polygons ***\n\n")
			for i in range(self.get_nb_polygons()) :
				f_debug.write(str(i) + " : " + str(self.polygons[i].get_corners()) + "\n")

			f_debug.write("\n*** Connected corners ***\n\n")
			for corner in self.corners :
				f_debug.write(str(corner.get_id()) + " : " + str(corner.get_connected_corners()) + "\n")

			f_debug.write("\n*** Parameters ***\n\n")
			for corner in self.corners :
				f_debug.write(str(corner.get_id()) + " : " + str(corner.get_data()))
	
	def build_csv(self, f_table_path) :
		labels = "Name,rod1-H,rod1-V,rod2-H,rod2-V,rod3-H,rod3-V,rod4-H,rod4-V,rod5-H,rod5-V,rod6-H,rod6-V,rod7-H,rod7-V,rod8-H,rod8-V\n"
		
		with open(f_table_path, 'w') as f_table:
			f_table.write(labels)
			for corner in self.corners :
				f_table.write(corner.get_data())
