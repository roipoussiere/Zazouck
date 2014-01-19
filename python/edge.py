#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

class Edge:
	def __init__(self, edge_id, p1, p2):
		self.id = edge_id
		self.p1 = p1
		self.p2 = p2
		self.position = (0,0,0)
		self.rotation = (0,0,0)
		self.length = 0
		self.data = ""

	def get_id(self): return self.id
	def get_p1(self): return self.p1
	def get_p2(self): return self.p2
	def get_length(self): return self.length
	def get_position(self): return self.position
	def get_rotation(self): return self.rotation
	def get_data(self):	return self.data

	def set_data(self):
		self.data = str(self.id) + ","
		for p in self.position: self.data += str(p) + ","
		for r in self.rotation: self.data += str(r) + ","
		self.data += str(self.length) + "\n"

	def set_length():
		#deplacer dans corner: d = c1.dist(c2)
		px = pow(p1[0] - p2[0], 2)
		py = pow(p1[1] - p2[1], 2)
		pz = pow(p1[2] - p2[2], 2)
		self.length = math.sqrt( px + py + pz)

	def set_position():
		tx = 0
		ty = 0
		tz = 0
		self.position = (tx, ty, tz)

	def set_rotation():
		rx = 0
		ry = 0
		rz = 0
		self.rotation = (rx, ry, rz)
