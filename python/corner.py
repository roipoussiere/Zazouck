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
		self.connected_corners = list()
	
	def get_id(self): return self.id
	def get_position(self): return self.position
	def get_connected_corners(self): return self.connected_corners
	
	def set_connected_corners(self, polygons):
		for poly in polygons:
			if poly.get_corners().count(self.id) != 0:
				for corner_id in poly.get_corners():
					if corner_id != self.id and self.connected_corners.count(corner_id) == 0:
						self.connected_corners.append(corner_id)

	def get_dist(self, corner):
		px = pow(self.position[0] - corner.get_position()[0], 2)
		py = pow(self.position[1] - corner.get_position()[1], 2)
		pz = pow(self.position[2] - corner.get_position()[2], 2)
		return math.sqrt(px + py + pz)

	def __str__(self):
		return str(self.get_id()) + " - " + str(self.get_position()) + \
				" - " + str(self.get_connected_corners())