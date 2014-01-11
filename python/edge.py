#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Nathanaël Jourdane
# This file is part of Zazoucko.
# Zazoucko is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Zazoucko is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazoucko. If not, see <http://www.gnu.org/licenses/>.

class Edge:
	def __init__(self, _id, _extremities, _length):
		self.id = _id
		self.extremities = _extremities
		self.length = _length

	def get_id(self): return self.id
	def get_extremities(self): return self.extremities
	def get_length(self): return self.length