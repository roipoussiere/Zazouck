#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013-2014 Nathanaël Jourdane
# This file is part of Zazouck.
# Zazouck is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. Zazouck is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Zazouck. If not, see
# <http://www.gnu.org/licenses/>.

'The polygons of the models.'

class Polygon:
    'The polygons of the models.'

    def __init__(self, polygon_id):
        self.polygon_id = polygon_id
        self.corners_id = list()
        self.normal = (0, 0, 0)
    
    def get_corners(self):
        'Corners list getter.'
        return self.corners_id
    
    def get_id(self):
        'Id getter.'
        return self.polygon_id
    
    def get_normal(self):
        'Normal getter.'
        return self.normal
    
    def add_corner(self, corner_id):
        'Adds a corner in the corner list of the polygon.'
        self.corners_id.append(corner_id)

    def set_normal(self, positions):
        'Calculate the normal of the polygon.'
        p_1 = positions[0]
        p_2 = positions[1]
        p_3 = positions[2]

        pos_x = (p_2[1]-p_1[1]) * (p_3[2]-p_1[2]) - (p_2[2]-p_1[2]) * (p_3[1]-p_1[1])
        pos_y = (p_2[2]-p_1[2]) * (p_3[0]-p_1[0]) - (p_2[0]-p_1[0]) * (p_3[2]-p_1[2])
        pos_z = (p_2[0]-p_1[0]) * (p_3[1]-p_1[1]) - (p_2[1]-p_1[1]) * (p_3[0]-p_1[0])

        # S1S2(x2-x1,y2-y1,z2-z1)
        # S1S3(x3-x1,y3-y1,z3-z1)

        # N(X,Y,Z)
        # X = (y2-y1)*(z3-z1) - (z2-z1)*(y3-y1)
        # Y = (z2-z1)*(x3-x1) - (x2-x1)*(z3-z1)
        # Z = (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1) 
        self.normal = (pos_x, pos_y, pos_z)

    def __str__(self):
        'Return informations about the polygons to print it.'
        return str(self.polygon_id) + " - " + str(self.corners_id)
