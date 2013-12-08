#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Ouack.
# Ouack is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Ouack is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Ouack. If not, see <http://www.gnu.org/licenses/>.

class Polygon :
	def __init__(self, polygon_id) :
		self.id = polygon_id
		self.corners_id = []
	
	def get_corners(self) : return self.corners_id
	
	def add_corner_id(self, corner_id) :
		self.corners_id.append(corner_id)
