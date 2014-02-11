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

'The corners of the model.'

import math

class Corner:
    'The corners of the model.'

    def __init__(self, corner_id, position):
        self.corner_id = corner_id
        self.position = position
        self.connected_corners = list()
    
    def get_id(self):
        'Returns the id of the corner.'
        return self.corner_id

    def get_position(self):
        'Returns the position of the corner.'
        return self.position

    def get_connected_corners(self):
        'Returns the corners connected to the corner.'
        return self.connected_corners
    
    def set_connected_corners(self, polygons):
        'Search the corners connected to the corner.'
        for poly in polygons:
            if poly.get_corners().count(self.corner_id) != 0:
                for corner_id in poly.get_corners():
                    if corner_id != self.corner_id and self.connected_corners.count(corner_id) == 0:
                        self.connected_corners.append(corner_id)

    def get_dist(self, corner):
        'Calculate the distance between the corner and an other one.'
        pos_x = pow(self.position[0] - corner.get_position()[0], 2)
        pos_y = pow(self.position[1] - corner.get_position()[1], 2)
        pos_z = pow(self.position[2] - corner.get_position()[2], 2)
        return math.sqrt(pos_x + pos_y + pos_z)

    def __str__(self):
        'Return informations about the corner.'
        return str(self.get_id()) + " - " + str(self.get_position()) + \
                " - " + str(self.get_connected_corners())