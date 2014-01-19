#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazouck is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see <http://www.gnu.org/licenses/>.

class Polygon:
	def __init__(self, polygon_id):
		self.id = polygon_id
		self.corners_id = []
		self.normal = (0,0,0)
	
	def get_corners(self): return self.corners_id
	def get_id(self): return self.id
	def get_normal(self): return self.normal
	
	def add_corner(self, corner_id):
		self.corners_id.append(corner_id)

	def set_normal(self, positions):
		p1 = positions[0]
		p2 = positions[1]
		p3 = positions[2]

		x = (p2[1]-p1[1])*(p3[2]-p1[2]) - (p2[2]-p1[2])*(p3[1]-p1[1])
		y = (p2[2]-p1[2])*(p3[0]-p1[0]) - (p2[0]-p1[0])*(p3[2]-p1[2])
		z = (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])

		# S1S2(x2-x1,y2-y1,z2-z1)
		# S1S3(x3-x1,y3-y1,z3-z1)

		# N(X,Y,Z)
		# X = (y2-y1)*(z3-z1) - (z2-z1)*(y3-y1)
		# Y = (z2-z1)*(x3-x1) - (x2-x1)*(z3-z1)
		# Z = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1) 
		self.normal = (x,y,z)

	def __str__(self):
		return str(self.get_id()) + " - " + str(self.get_corners())