#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

import math

class Edge:
	def __init__(self, edge_id, corner_start, corner_end):
		self.id = edge_id
		self.corner_start = corner_start
		self.corner_end = corner_end
		self.position = (0,0,0)
		self.rotation = (0,0,0)
		self.length = 0
		self.data = ""

	def get_id(self): return self.id
	def get_corner_start(self): return self.corner_start
	def get_corner_end(self): return self.corner_end
	def get_length(self): return self.length
	def get_position(self): return self.position
	def get_rotation(self): return self.rotation
	def get_data(self):	return self.data

	def set_data(self):
		self.data = str(self.id) + ","

		for p in self.position:
			self.data += str(p) + ","

		for r in self.rotation:
			self.data += str(r) + ","

		self.data += str(self.length) + "\n"

	def set_length(self):
		self.length = self.corner_start.get_dist(self.corner_end)

	def set_position(self):
		tx = 1
		ty = 1
		tz = 1
		self.position = (tx, ty, tz)

	def set_rotation(self):
		rx = 1
		ry = 1
		rz = 1
		self.rotation = (rx, ry, rz)
	
	def __str__(self):
		return str(self.get_id()) + " - " + str(self.get_position()) + \
				" - " + str(self.get_length())