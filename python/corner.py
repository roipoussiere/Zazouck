#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import math, random

class Corner:
	def __init__(self, corner_id, position):
		self.id = corner_id
		self.position = position
		self.connected_corners = []
		self.angles = []
		self.data = ""
	
	def get_id(self): return self.id
	def get_position(self): return self.position
	def get_connected_corners(self): return self.connected_corners
	def get_angles(self): return self.angles
	def get_data(self): return self.data
	
	def set_connected_corners(self, polygons):
		for poly in polygons:
			if poly.get_corners().count(self.id) != 0:
				for corner_id in poly.get_corners():
					if corner_id != self.id and self.connected_corners.count(corner_id) == 0:
						self.connected_corners.append(corner_id)
	
	def set_angles(self, target_position):
		init_pos = self.position
		
		#for i in range(3):
		
		relative_pos = (target_position[0] - init_pos[0], target_position[1] - init_pos[1], target_position[2] - init_pos[2])
		
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
			
		self.angles.append(int(round(angle_v)))
		self.angles.append(int(round(angle_h)))
	
	def set_data(self):
		self.data += self._number_to_txt(self.id, 5)

		self.data += "," + str(self.position[0])
		self.data += "," + str(self.position[1])
		self.data += "," + str(self.position[2])

		for angle in self.angles:
			self.data += "," + self._number_to_txt(angle, 3)
		self.data += "\n"

	def _number_to_txt(self, nb, size):
		nb = "err" if nb > pow(10, size)-1 else str(nb)

		while len(nb) < size:
			nb = "0" + nb
		return nb
