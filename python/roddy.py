#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

from os import path as op
import math
import solid

class Roddy:

	def __init__(self, input_stl_path, output_dir, cmd_dir):
		self.input_stl_path = input_stl_path
		self.output_dir = output_dir
		self.cmd_dir = cmd_dir

		self.solid = solid.Solid(input_stl_path)
		self.solid.display(op.join(self.output_dir, "details.txt"))

		self._corners()
	# 	self._edges()

	def _corners(self):

		self._build_corners_table(op.join(self.cmd_dir, "corners.csv"))
		self._build_edges_table(op.join(self.cmd_dir, "edges.csv"))

		print "Successfully created building files in " + self.output_dir + "."


	# def _edges(self):
	# 	export = export.Export(output_dir)

	# TODO: à déplacer
	# def set_corners_data(self):
	# 	for corner in solid.corners:
	# 		for target in corner.get_connected_corners():
	# 			corner.set_angles(self._get_corner_by_id(target).get_position())

	# 	for corner in self.corners:
	# 		corner.set_data()

	# def set_edges_data(self):
	# 	for edge in self.edges:
	# 		edge.set_data()

	def _build_corners_table(self, corners_table_path):
		infos = str(self.solid.get_nb_corners()) + " corners," + str(self.solid.get_nb_polygons()) \
				+ " polygons," + str(self.solid.get_nb_edges()) + " edges\n"

		labels = "id,posX,posY,posZ,rod 1-V,rod 1-H,rod 2-V,rod 2-H,rod 3-V,rod 3-H," + \
				"rod 4-V,rod 4-H,rod 5-V,rod 5-H,rod 6-V,rod 6-H,rod 7-V,rod 7-H,rod 8-V,rod 8-H\n"

		with open(corners_table_path, 'w') as table:
			table.write(infos)
			table.write(labels)

			for corner in self.solid.corners:   # ugly!!!
				table.write(self._corner_data(corner))

	def _build_edges_table(self, edges_table_path):
		infos = str(self.solid.get_nb_corners()) + " corners," + str(self.solid.get_nb_polygons()) \
				+ " polygons," + str(self.solid.get_nb_edges()) + " edges\n"
		labels = "id,posX,posY,posZ,rotX,rotY,rotZ,length\n"

		with open(edges_table_path, 'w') as table:
			table.write(infos)
			table.write(labels)
			for edge in self.solid.edges:	# ugly!!!
				table.write(self._edge_data(edge))

	def _corner_data(self, corner):
		data = self._number_to_txt(corner.get_id(), 5)
		angles = list()

		for p in corner.get_position():
			data += "," + str(p)

		for target in corner.get_connected_corners():
			angles += self.positions_to_angles(corner.get_position(), \
					self.solid._get_corner_by_id(target).get_position())

		for angle in angles:
			data += "," + self._number_to_txt(angle, 3)
		data += "\n"

		return data

	def _edge_data(self, edge):
		data = str(edge.get_id()) + ","

		for p in edge.get_position():
			data += str(p) + ","

		for r in edge.get_rotation():
			data += str(r) + ","

		data += str(edge.get_length()) + "\n"

		return data

	def positions_to_angles(self, init_position, target_position):
		#for i in range(3):
		init_x = target_position[0] - init_position[0]
		init_y = target_position[1] - init_position[1]
		init_z = target_position[2] - init_position[2]

		relative_pos = (init_x, init_y, init_z)
		
		#calcul angle_v
		hypot = math.hypot(relative_pos[0], relative_pos[1])
		if hypot == 0:
			angle_v = 0 if relative_pos[2] > 0 else 180
		else:
			angle_v = 90-math.degrees(math.atan(relative_pos[2] / hypot))

		# calcul angle_h
		if relative_pos[0] == 0:
			angle_h = 90 if relative_pos[1] >= 0 else -90
		elif relative_pos[1] == 0:
			angle_h = 0 if relative_pos[0] >= 0 else 180
		else:
			angle_h = math.degrees(math.atan(relative_pos[0] / relative_pos[1]))
			if relative_pos[0] < 0 and relative_pos[1] < 0: angle_h -= 180
		angle_h = angle_h+360 if angle_h < 0 else angle_h
		
		return int(round(angle_v)), int(round(angle_h))

	# corner
	def _number_to_txt(self, nb, size):
		nb = "err" if nb > pow(10, size)-1 else str(nb)

		while len(nb) < size:
			nb = "0" + nb
		return nb