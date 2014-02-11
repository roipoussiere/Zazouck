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

'Build the documentation of the construction (images and html files).'

IMG_SIZE = 200

from os import path as op
import xml.etree.ElementTree as ET
import os, distutils.core, shutil
import utils, process

class Doc:
    'Build the documentation of the construction (images and html files).'
    def __init__(self, xml_path, zazouck_dir, doc_dir, scad_dir, jobs, openscad_path, verbose_lvl):
        self.doc_dir = doc_dir
        self.jobs = jobs
        self.openscad_path = openscad_path
        self.verbose_lvl = verbose_lvl
        self.scad_dir = scad_dir
        self.root = ET.parse(xml_path).getroot()

        doc_files_dir = op.join(zazouck_dir, 'doc_generation')
        distutils.dir_util.copy_tree(doc_files_dir, doc_dir)

        os.makedirs(op.join(self.doc_dir, 'parts_html'))
        self.make_pictures()
        self.make_html_menu()
        self.make_html_details(self.root)
        self.replace_html_index()

    def replace_html_index(self):
        """Replace several string, like "__TITLE__" on the index html file by
        the corresponding information in the model."""

        import time
        index = op.join(self.doc_dir, 'index.html')
        os.rename(index, index + '~')
        model_id = self.root.get('id')
        
        with open(index, 'w') as fout:
            with open(index + '~', 'r') as fin:
                for line in fin:
                    line = line.replace('__TITLE__', (model_id + ' documentation').capitalize())
                    line = line.replace('__MODEL_PATH__', './parts_html/' + model_id)
                    line = line.replace('__TIME__', time.strftime('on %b %d, %Y at %l:%M%p'))
                    fout.write(line)

        os.remove(index + '~')

    def make_html_menu(self):
        'Make the html menu.'
        content = ET.Element('summary')

        menu = ET.SubElement(content, 'div')
        menu.set('id', 'menu')

        link = ET.SubElement(menu, 'a')
        link.text = self.root.get('id').capitalize()
        link.set('class', 'focus')
        link.set('href', './parts_html/' + self.root.get('id') + '.html')
        link.set('id', self.root.get('id'))
        link.set('target', 'detail')

        self.feed_menu(self.root, menu)

        file_path = op.join(self.doc_dir, 'menu.html')
        make_html(file_path, content, 'stylesheet.css')

    def feed_menu(self, tree, menu):
        'Recursive. Adds the tree to the menu.'
        list_ul = ET.SubElement(menu, 'ul')
        for elmt in tree:
            list_li = ET.SubElement(list_ul, 'li')

            link = ET.SubElement(list_li, 'a')
            link.text = elmt.get('id').capitalize()
            link.set('href', './parts_html/' + elmt.get('id') + '.html')
            link.set('id', elmt.get('id'))
            link.set('target', 'detail')
            
            if len(elmt) > 0:
                self.feed_menu(elmt, list_li)

    def make_html_details(self, elmt):
        'Recursive. Make the html file of the specified elmt for the details page.'

        for sub_elmt in elmt:
            self.make_html_details(sub_elmt)

        content = ET.Element('article')

        family_infos = ET.SubElement(content, 'div')
        family_infos.set('id', 'infos')
        
        img_path = '../parts_img/' + elmt.get('id') + '.png' if elmt.tag == 'part' or \
                elmt.tag == 'model' else '../img/group.png' if elmt.tag == 'family' else ''

        if img_path != '':
            img = ET.SubElement(family_infos, 'img')
            img.set('class', 'large')
            img.set('src', img_path)

        family_infos.append(self._html_infos(elmt))

        if len(elmt) != 0:
            childrens = ET.SubElement(content, 'div')
            ET.SubElement(childrens, 'hr')
            childrens.set('class', 'elements')

            ET.SubElement(childrens, 'h3').text = 'Elements'

            for element in elmt:
                childrens.append(html_elements(element.get('id')))

            clear_div = ET.SubElement(content, 'div')
            clear_div.set('class', 'separator')

        if 'connections' in elmt.attrib:
            connections = ET.SubElement(content, 'div')
            ET.SubElement(connections, 'hr')
            connections.set('class', 'elements')

            ET.SubElement(connections, 'h3').text = 'Connected to'

            for connection_id in elmt.get('connections').split(';'):
                connections.append(html_elements(connection_id))

            clear_div = ET.SubElement(content, 'div')
            clear_div.set('class', 'separator')

        file_path = op.join(self.doc_dir, 'parts_html', elmt.get('id') + '.html')
        make_html(file_path, content, '../stylesheet.css')

    def _html_infos(self, elmt):
        'Some textual informations about the element.'
    
        element_text = ET.Element('div')
        element_text.set('id', 'text')

        family_name = self.get_family_attribute(elmt, 'id')
        title = family_name.capitalize() + ' ' if elmt.tag == 'part' else ''
        ET.SubElement(element_text, 'h2').text = title + elmt.get('id').capitalize()

        if family_name != '':
            parent = ET.SubElement(element_text, 'p')
            parent.text = 'Parent: '
            link = ET.SubElement(parent, 'a')
            link.set('href', family_name + '.html')
            link.set('class', 'link_info')
            ET.SubElement(link, 'b').text = family_name.capitalize()

        if len(elmt) != 0:
            text_data = ET.SubElement(element_text, 'p')
            text_data.text = 'Number of elements: '
            ET.SubElement(text_data, 'b').text = str(len(elmt))

        # (Label, key, print on part page, is unit)
        infos = (('Description', 'desc', False),
                ('Type', 'type', True), ('Position', 'pos', True), ('Rotation','rot', True),
                ('Generated by', 'file', False), ('Light version', 'light_file', False))

        for info in infos:
            parent_data = self.get_family_attribute(elmt, info[1])
            data = elmt.get(info[1]) if info[1] in elmt.attrib else parent_data
            if data != '' and (elmt.tag != 'part' or elmt.tag == 'part' and info[2]):
                text_data = ET.SubElement(element_text, 'p')
                text_data.text = info[0] + ': '
                ET.SubElement(text_data, 'b').text = data.replace(',', ', ')

        if 'thickness' in self.root.attrib and (elmt.get('type') == 'dxf' or elmt.tag == 'model'):
            text_data = ET.SubElement(element_text, 'p')
            text_data.text = 'Material thickness: '
            ET.SubElement(text_data, 'b').text = self.root.get('thickness') + self.root.get('unit')

        parent_data = self.get_family_attribute(elmt, 'data') if elmt.tag != 'family' else ''
        curent_data = elmt.get('data') if 'data' in elmt.attrib else ''
        datas = parent_data + curent_data
        if datas != '':
            list_ul = ET.SubElement(element_text, 'p').text = 'Datas:'
            list_ul = ET.SubElement(element_text, 'ul')
            for data in datas.split(';'):
                tab_data = data.replace("'", '').replace(',', ', ').split('=')
                list_li = ET.SubElement(list_ul, 'li')
                list_li.text = tab_data[0].capitalize() + ': '
                ET.SubElement(list_li, 'b').text = tab_data[1].capitalize()

        return element_text

    def get_family_attribute(self, elmt, attribute):
        'Get the specified attribute of the elmt family.'
        value = None

        if elmt.tag != 'model':
            parent_map = dict((c, p) for p in self.root.getiterator() for c in p)
            value = parent_map[elmt].get(attribute)

        return value if value != None else ''

    def make_pictures(self):
        'Generates pictures for the documentation.'
        import tempfile

        print "\n*** Creating pictures ***"

        img_opt = "--imgsize=" + str(IMG_SIZE * 2) + "," + str(IMG_SIZE * 2)

        img_dir = op.join(self.doc_dir, 'parts_img')
        os.makedirs(img_dir)

        cube_path = op.join(tempfile.gettempdir(), self.root.get('id') + '.scad')
        with open(cube_path, 'w') as scad_file:
            scad_file.write('import("' + op.join(op.dirname(self.doc_dir), 'original.stl') + '");')
        
        # TODO: bug fix option d'images pour le modèle
        # img_opt = img_opt + (" --camera=" + self.root.get('img')
        # if self.root.get('img') != 'yes' else '')

        command = 'openscad ' + cube_path + ' -o ' + op.join(img_dir, self.root.get('id') + '.png')
        os.system(command) # marche pas avec popen
        os.remove(cube_path)

        # TODO: ajouter recursivité + s'il pas d'img dans le noeud courant on regarde dans family

		# pour toutes les familles où il faut une image:
        for family in (family for family in self.root if 'img' in family.attrib):
            part_scad_path = op.join(self.scad_dir, family.get('file'))
            tmp_dxf = op.join(tempfile.gettempdir(), 'tmp_dxf')
            export_dir = img_dir if family.get('type') == 'stl' else tmp_dxf

            if family.get('type') == 'dxf':
                utils.create_dir(tmp_dxf, self.verbose_lvl)

            family_img = family.get('img')
            part_img_opt = img_opt + (" --camera=" + family_img if family_img != 'yes' else '')
                    # if family.get('type') == 'stl' else False
            param = self.root.get('data')

            process.Process(part_scad_path, family, param, export_dir, self.jobs,
            		self.openscad_path, self.verbose_lvl, part_img_opt)

            if family.get('type') == 'dxf':
                parts_list = list()
                for part in family:
                    dxf_file = op.join(tmp_dxf, part.get('id') + '.dxf')
                    scad_file = op.join(self.scad_dir, 'dxf2stl.scad')
                    thickn = self.root.get('thickness') if 'thickness' in self.root.attrib else '1'

                    command = 'openscad ' + scad_file + ' -D \'file="' + dxf_file + '"; thickness='\
                            + thickn + "'" + ' -o ' + op.join(img_dir, part.get('id') + '.png')

                    parts_list.append(utils.cmd(command, self.verbose_lvl))

                while (parts_list):
                    for i, part in enumerate(parts_list):
                        if part.poll() == 0:
                            del parts_list[i]

                shutil.rmtree(tmp_dxf)

        dimentions = str(IMG_SIZE) + 'x' + str(IMG_SIZE)
        command = 'mogrify -trim +repage -resize ' + dimentions + \
                ' -background "#FFFFE5" -gravity center -extent ' + dimentions + \
                ' -fuzz 15% -transparent "#FFFFE5" ' + op.join(img_dir, '*.png')
        # shadow_cmd = 'for f in ' + op.join(img_dir, '*.png') + '; do convert $f -trim ' + \
        # '\( +clone -background black -shadow 80x5+5+5 \) +swap -background none
        # -layers merge $f; done'

        utils.cmd(command, self.verbose_lvl)

def make_html(file_path, content, css_path):
    'Create an html file and write on it the specified content.'

    html = ET.Element('html')
    head = ET.SubElement(html, 'head')

    link = ET.SubElement(head, 'link')
    link.set('rel', 'stylesheet')
    link.set('href', css_path)

    body = ET.SubElement(html, 'body')
    body.set('id', os.path.splitext(os.path.basename(file_path))[0])
    #body.set('onload', 'menu.getElementsById(' + element.get('id') + ') = "focus";')
    body.append(content)
    utils.indent(html)

    with open(file_path, 'w') as html_file:
        html_file.write('<!DOCTYPE html>\n')
        ET.ElementTree(html).write(html_file, 'utf-8')

def html_elements(elmt_id):
    'Create an html div for an element, like children or connected element.'

    file_path = elmt_id + '.html'

    elmt = ET.Element('a')
    elmt.set('href', file_path)
    elmt.set('class', 'element')

    part_div = ET.SubElement(elmt, 'div')
    part_div.set('class', 'icon')
    ET.SubElement(part_div, 'h3').text = elmt_id.capitalize()

    img_path = '../parts_img/' + elmt_id + '.png'
    img = ET.SubElement(part_div, 'img')
    img.set('class', 'thumbnail')
    img.set('src', img_path)

    return elmt