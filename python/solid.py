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

'Calculate informations about the model, like edges, corners and polygons, to make processes on it.'

import random, re, tempfile, os
from os import path as op
import corner, polygon, edge

MAX_ID = 32766 # Identification number for edges, polygons and corners.

class Solid: # TODO : singleton
    """Calculate informations about the model, like edges, corners and polygons,
    to make processes on it."""
    def __init__(self, input_stl_path):
        self.input_stl_path = input_stl_path
        self.polygons = list()
        self.corners = list()
        self.edges = list()
        self.id_list = list()
        self._create_solid()
    
    def get_nb_corners(self):
        'Returns the number of corners.'
        return len(self.corners)
    
    def get_nb_polygons(self):
        'Returns the number of polygons.'
        return len(self.polygons)
    
    def get_nb_edges(self):
        'Returns the number of edges.'
        return len(self.edges)
    
    def _create_solid(self):
        'Calculate all the informations about the model.'

        cleaned_path = op.join(tempfile.gettempdir(), "zazouck_cleaned")
        self._clean_file(cleaned_path)

        model = _file_to_model(cleaned_path)
        os.remove(cleaned_path)

        self._fill_corners(model)
        self._fill_polygons(model)
        del model
        
        for parsed_corner in self.corners:
            parsed_corner.set_connected_corners(self.polygons)
        
        self._fill_edges()
        #s.merge_coplanar_polygons() # TODO

    def get_corner_by_id(self, corner_id):
        'Allows to get a corner in the solid by its id.'

        needed_corner = None
        for parsed_corner in self.corners:
            if parsed_corner.get_id() == corner_id:
                needed_corner = parsed_corner
        return needed_corner

    def _get_random_id(self):
        'Choose a random id for the edges, corners or polygons.'
        
        while True:
            random_id = random.randint(1, MAX_ID)
            if random_id not in self.id_list:
                self.id_list.append(random_id)
                return random_id
        return False

    def _fill_corners(self, _model):
        'Fill the corners list.'

        positions = list()

        for polygon_model in _model:
            for point in polygon_model:
                if positions.count(point) == 0:
                    positions.append(point)
        
        for position in positions:
            self.corners.append(corner.Corner(self._get_random_id(), position))
    
    def _fill_polygons(self, _model):
        'Fill the polygons list.'

        for polygon_model in _model:

            poly = polygon.Polygon(self._get_random_id())
            corners_pos = []
            for position in polygon_model:
                for parsed_corner in self.corners:
                    if parsed_corner.get_position() == position:
                        corner_id = parsed_corner.get_id()
                        corners_pos.append(parsed_corner.get_position())
                        break
                poly.add_corner(corner_id)
            poly.set_normal(corners_pos)
            self.polygons.append(poly)

    def _fill_edges(self):
        'Fill the polygons list.'

        extremities = list()

        for corner_1 in self.corners:
            for corner_2 in corner_1.get_connected_corners():
                if (corner_1.get_id(), corner_2) not in extremities and \
                        (corner_2, corner_1.get_id()) not in extremities:
                    extremities.append((corner_1.get_id(), corner_2))
                    self.edges.append(edge.Edge(
                            self._get_random_id(), corner_1, self.get_corner_by_id(corner_2)))

        for parsed_edge in self.edges:
            parsed_edge.set_length()
            parsed_edge.set_position()
            parsed_edge.set_rotation()

    def _find_coplanar_polygons(self):
        'Find the coplanar polygons on the model to merge it.'

        normals = []
        coplanar_polys = []
        for poly in self.polygons:
            normal = poly.get_normal()
            for i, parsed_normal in enumerate(normals):
                if parsed_normal == normal:
                    coplanar_polys.append((poly.get_id(), self.polygons[i].get_id()))
            else:
                normals.append(normal)
        return coplanar_polys

    #def merge_coplanar_polygons(self): # TODO
    #    print "coplanar_polygons:", self._find_coplanar_polygons();
    
    def display(self, details_path):
        'Displays informations about the model.'

        with open(details_path, 'w') as f_details:
            f_details.write("*** Corners position and connexions ***\n\n")
            for i, solid_corner in enumerate(self.corners):
                f_details.write(str(i+1) + ": " + str(solid_corner) + "\n")

            f_details.write("\n*** Polygons connexions ***\n\n")
            for i, solid_polygon in enumerate(self.polygons):
                f_details.write(str(i+1) + ": " + str(solid_polygon) + "\n")

            f_details.write("\n*** Edges position and length ***\n\n")
            for i, solid_edge in enumerate(self.edges):
                f_details.write(str(i+1) + ": " + str(solid_edge) + "\n")

    def _clean_file(self, cleaned_path):
        'Clean the stl file to exploit it.'

        words = 'vertex', 'endloop'
        with open(self.input_stl_path, 'r') as f_stl:
            with open(cleaned_path, 'w') as f_cleaned_stl:
                for line in f_stl:
                    if any(word in line for word in words):
                        line = re.sub('^endloop.*', '|', line.lstrip())
                        line = line.replace("vertex", "")
                        line = line.lstrip().replace(" ", ",")
                        line = line.replace("\n", ";")
                        line = line.replace("|;", "\n")
                        f_cleaned_stl.write(line)

def _file_to_model(cleaned_path):
    'Return an instance of the model from the stl cleaned file.'
    
    model = list()
    with open(cleaned_path) as f_cleaned_stl:
        for line in f_cleaned_stl:
            line = re.sub('[;\n]$', '\n', line)
            point_list = list()
            for point in line.split(';'):
                pos_str = point.split(',')
                pos_int = list()
                for number in pos_str:
                    pos_int.append(float(number))
                    point_list.append(pos_int)
            
                model.append(point_list)

        return model
