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

'Exports the model files (stl fo 3D and dxf for 2D) to build the construction.'

import os, signal
from os import path as op
import xml.etree.ElementTree as ET
import process

class Export: # TODO : singleton
    'Exports the model files (stl fo 3D and dxf for 2D) to build the construction.'

    def __init__(self, xml_path, param_path, project_dir, openscad_path, 
    			scad_dir, nb_job_slots, verbose_lvl, test):
        self.xml_path = xml_path
        self.param_path = param_path
        self.openscad_path = openscad_path
        self.project_dir = project_dir
        self.scad_dir = scad_dir
        self.nb_job_slots = nb_job_slots
        self.verbose_lvl = verbose_lvl
        self.test = test
        self.params = list()
        signal.signal(signal.SIGINT, self.signal_handler)

        self.root = ET.parse(xml_path).getroot()

    def make_stl(self):
        'Make the stl files'
        
        for family in self.root:
            print "\n*** Creating", len(family), family.get('id') + "s ***"

            part_scad_name = family.get('light_file') if self.test and \
                    'light_file' in family.attrib else family.get('file')
            part_scad_path = op.join(self.scad_dir, part_scad_name)

            export_path = op.join(self.project_dir, family.get('id'))
            param = self.root.get('data')

            if not os.path.exists(export_path):
                os.makedirs(export_path)
            process.Process(part_scad_path, family, param, export_path, self.nb_job_slots,
            		self.openscad_path, self.verbose_lvl)

        self._save_xml()

    def make_assembly(self):
        'Build a new model representing the assembled model as should be.'

        assembly_path = op.join(self.project_dir, 'assembled')
        os.makedirs(assembly_path)

        print "\n*** Creating assembled model ***\n"
        print "This file will be created in " + assembly_path

        for family in self.root:
            part_scad_name = family.get('light_file') if self.test and \
                    'light_file' in family.attrib else family.get('file')

            part_scad_path = op.join(self.scad_dir, part_scad_name)
            param = self.root.get('data')

            process.Process(part_scad_path, family, param, assembly_path, self.nb_job_slots,
            		self.openscad_path, self.verbose_lvl, is_assembly = True)
        self._save_xml()

    def _save_xml(self):
        'Save the xml building file.'
        ET.ElementTree(self.root).write(self.xml_path, encoding = "UTF-8", xml_declaration = True)

    def signal_handler(self):
        'Called when a SIGINT (ctrl-c) is recieved. Displays messages and save the xml then quit.'
        import sys
        print "\n\nCompilation interrupted by the user."

        # TODO : compter le nombre de fichiers crées

        # print self.nb_created, "file" + ('s' if self.nb_created > 1 else '') + " were created."
        print "You can continue this job later with this command:"
        print "zazouck " + self.project_dir
        self._save_xml()
        sys.exit(0)
