# -*- coding: utf-8 -*-
# !/usr/bin/python

import os, shutil, re, pickle, math, time

export_directory = "./stl/" # idem + auto
f_stl_path = "./example.stl" # à remplacer par argument
f_csv_parts_path = "./corners.csv" # changer par rep. temp
f_cleaned_path = "./cleaned"
f_solid_path = "./solid"
f_scad_path = "./ouack.scad"

verbose = False

_corners = []
_solid_id = []
_friends = []

def main() :
	clean_file(f_stl_path, f_cleaned_path)
	pikle_file(f_cleaned_path, f_solid_path)
	solid_to_corners()
	solid_to_id()
	find_friend()
	build_csv(f_csv_parts_path)
	os.remove(f_solid_path)
	os.remove(f_cleaned_path)

def aff() :
	print "\n*** Corners ***"
	for i in range(len(_corners)) :
		print i , ":" , _corners[i]

	print "\n*** Polygons ***"
	for i in range(len(_solid_id)) :
		print i , ":" , _solid_id[i]

	print "\n*** Linked corners ***"
	for i in range(len(_friends)) :
		print i , ":" , _friends[i]

	print "\n*** Parameters ***"
	for i in range(len(_corners)) :
		print i , ":" , id_to_txt(i),

def test() :
	print "\n*** Test ***"
	print "5,0 :", get_angle(5, 0)
	print "7,2 :", get_angle(7, 2)

def clean_file(f_input, f_output) :
	f_in = open(f_input, "r")
	f_out = open(f_output, "w")

	for line in f_in :
		line = re.sub('^facet.*', '|', line.lstrip())
		if line == '|\n' :
			f_out.write('\n')
			continue
		else : line = re.sub('[^0-9. ]', '', line) + ';'
		line = re.sub(' ', ',', line.lstrip())
		if line == ';' : continue
		f_out.write(line)

	f_in.close()
	f_out.close()

def pikle_file(cleaned_file_path, solid_path) :
	f = open(cleaned_file_path, "r")

	f.readline()
	solid = []

	for line in f :
		line = re.sub('[;\n]$', '', line)
		p = []
		for point in line.split(';') :
			pos_str = point.split(',')
			pos_int = []
			for nb in pos_str :
				pos_int.append(int(nb))
			p.append(pos_int)
		
		solid.append(p)

	f.close()
	pickle.dump( solid, open( solid_path, "wb" ))

def nb_occ(tab, elt) :
	occ = 0

	for tab_elt in tab :
		if tab_elt == elt :
			occ += 1
	return occ

def solid_to_corners() :
	solid = pickle.load(open( "solid", "rb" ))
	positions = []
	
	for poly in solid :
		for point in poly :
			if nb_occ(positions, point) == 0:
				positions.append(point)

	for c in positions :
		_corners.append(c)

def position_to_id (position) :
	i = 0
	for c in _corners :
		if c == position : 
			return i
		i+=1
	return -1

def solid_to_id() :
	poly_id = []
	solid = pickle.load(open( "solid", "rb" ))
	
	for poly in solid :
		poly_id = []
		for point in poly :
			poly_id.append(position_to_id(point))
		_solid_id.append(poly_id)

def find_friend() :
	for i in range(len(_corners)) :
		occ = []
		for poly in _solid_id :
			if nb_occ(poly, i) != 0 :
				for p in poly :
					if p != i and nb_occ(occ, p) == 0 :
						occ.append(p)
		_friends.append(occ)

def get_angle(init_id, target_id) :
	init_pos = _corners[init_id]
	target_pos = _corners[target_id]
	
	relative_pos = [target_pos[0]-init_pos[0], target_pos[1]-init_pos[1], target_pos[2]-init_pos[2]]
	
	# calcul angle_h avec cas particuliers
	if relative_pos[0] == 0 :
		angle_h = 90 if relative_pos[1] >= 0 else -90
	elif relative_pos[1] == 0 :
		angle_h = 0 if relative_pos[0] >= 0 else 180
	else :
		angle_h = math.degrees(math.atan(relative_pos[0] / relative_pos[1]))
		if relative_pos[0] < 0 and relative_pos[1] < 0 : angle_h -= 180

	angle_h = angle_h+360 if angle_h < 0 else angle_h
	
	hypot = math.hypot(relative_pos[0], relative_pos[1])
	
	if hypot == 0 :
		angle_v = 0 if relative_pos[2] > 0 else 180
	else :
		angle_v = 90-math.degrees(math.atan(relative_pos[2] / hypot))
	
	return (angle_h, angle_v)

def id_to_txt(part_id) :
	txt = ""
	txt += param_to_txt(part_id, 5)
	for i in range(len(_friends[part_id])) :
		txt += "," + param_to_txt(get_angle(part_id, _friends[part_id][i])[0], 3)
		txt += "," + param_to_txt(get_angle(part_id, _friends[part_id][i])[1], 3)
	return txt + "\n"

def param_to_txt (nb, size) :
	max_nb = pow(10, size)-1
	nb = max_nb if nb > max_nb else nb
	word = str(int(round(nb)))

	while len(word) < size:
		word = "0" + word
	return word

def build_csv(f_output) :
	f_parts = open(f_output, "w")
	
	labels = "Name,rod1-H,rod1-V,rod2-H,rod2-V,rod3-H,rod3-V,rod4-H,rod4-V,rod5-H,rod5-V,rod6-H,rod6-V,rod7-H,rod7-V,rod8-H,rod8-V\n"
	
	f_parts.write(labels)
	for i in range(len(_corners)) :
		f_parts.write(id_to_txt(i))
	
	f_parts.close()

def make_parts(f_input, start=0) :
	print "\n*** Compilation ***"
	f_parts = open(f_input, "r")
	f_parts.readline()
	
	path = os.path.dirname(export_directory)
	if os.path.exists(path):
		shutil.rmtree(export_directory)
	os.makedirs(path)
	
	#for i in range(start) :
	#	f_parts.readline() # À compléter
	redirection = "" if verbose else "> /dev/null 2> /dev/null"
	i = 0
	t = time.time()
	
	for line in f_parts :
		name = line[0:5]
		print "Compiling file " + str(i+1) + "/" + str(len(_corners)),
		print "(" + str(i/float(len(_corners))*100) + "%)",
		if i==0 :
			print "- please wait... "
		else :
			print "for " + time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t)) + ", please wait", time.strftime("%Hh%Mm%Ss", time.gmtime((time.time()-t)/i*(len(_corners)-i))) + "."
		os.system("openscad " + f_scad_path + " -D 'data=\"" + line.rstrip('\n') + "\"' -o " + export_directory + name + ".stl" + redirection)
		# ne pas rediriger sorties si mode verbeux
		i+=1
	f_parts.close()
	print "\n*** Finished! ***"
	print i, "stl files successfully created in " + time.strftime("%Hh%Mm%Ss", time.gmtime(time.time()-t)) + "."

main()
aff()
make_parts(f_csv_parts_path)
