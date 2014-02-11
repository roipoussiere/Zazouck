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

'The edges of the model.'

class Edge:
    'The edges of the model.'
    
    def __init__(self, edge_id, corner_start, corner_end):
        self.edge_id = edge_id
        self.corner_start = corner_start
        self.corner_end = corner_end
        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.length = 0

    def get_id(self):
        'id getter'
        return self.edge_id
    
    def get_corner_start(self):
        '1st corner getter'
        return self.corner_start
    
    def get_corner_end(self):
        '2nd corner getter'
        return self.corner_end
    
    def get_length(self):
        'length getter'
        return self.length
    
    def get_position(self):
        'position getter'
        return self.position
        
    def get_rotation(self):
        'rotetion getter'
        return self.rotation

    def set_length(self):
        'Calculate the length'
        self.length = self.corner_start.get_dist(self.corner_end)

    # position au centre
    def set_position(self):
        'Calculate the position'
        x_pos = (self.corner_start.get_position()[0] + self.corner_end.get_position()[0])/2
        y_pos = (self.corner_start.get_position()[1] + self.corner_end.get_position()[1])/2
        z_pos = (self.corner_start.get_position()[2] + self.corner_end.get_position()[2])/2
        self.position = (x_pos, y_pos, z_pos)

    def set_rotation(self):
        'calculate the rotation'
        x_rot = 0
        y_rot = 0
        z_rot = 0
        self.rotation = (x_rot, y_rot, z_rot)
    
    def __str__(self):
        'Return '
        return str(self.edge_id) + " - " + str(self.position) + ' - ' + str(self.length)
