data = "00000,000,000";
// max id = 16383 : 14 bits de data et 2 bits de parité

width = 6.5;
edge_length = 8;
hole_width = 3.5;
hole_deep = 5;

csv = search(",", data, 20)[0];
id = longStrToNumber(str(data[0], data[1], data[2], data[3], data[4]));
v = [p2i(0), p2i(1), p2i(2), p2i(3), p2i(4), p2i(5), p2i(6), p2i(7), p2i(8), p2i(9), p2i(10), p2i(11)];

part([[v[0],v[1]], [v[2],v[3]], [v[4],v[5]], [v[6],v[7]], [v[8],v[9]], [v[10],v[11]]]);

// function int_to_bin(code, i=0, v) = (i>0) ? int_to_bin(code, i-1, v) : v[i]=;

module code(code)
{
	square_width = hole_width/4;

	// À remplacer par une fonction recursive
	tab = [int2bin(code, 0), int2bin(code, 1), int2bin(code, 2), int2bin(code, 3),
			int2bin(code, 4), int2bin(code, 5), int2bin(code, 6), int2bin(code, 7),
			int2bin(code, 8), int2bin(code, 9), int2bin(code, 10), int2bin(code, 11),
			int2bin(code, 12), int2bin(code, 13)];

	pb0 = int2bin(sumv(tab, 13), 0);
	pb1 = int2bin(sumv(tab, 13), 1);
	
	translate([-hole_width/2, -hole_width/2, edge_length-hole_deep-1]) linear_extrude(height = edge_length) {
		for(i = [0:13]) {
			if (int2bin(code, i) == 1)
				translate([(i%4)*square_width, floor(i/4)*square_width, 0])
					square(square_width);
		}
		
		if (pb0 == 1)
			translate([2*square_width, 3*square_width, 0]) square(square_width);
		if (pb1 == 1)
			translate([3*square_width, 3*square_width, 0]) square(square_width);
	}
}

module part(v)
{
	$fn = 50;
	
	rotate([0,0,90]) intersection() {
		sphere(r = edge_length);
		union() {
			sphere(width/2);
			difference() {
				for(i = [0:len(v)-1])
					if (v[i][1] != -1 && v[i][0] != -1)
						rotate([v[i][1], 0, v[i][0]])
							block(width, edge_length, circular=true);
		
			for(i = [0:len(v)-1])
					if (v[i][1] != -1 && v[i][0] != -1)
						rotate([v[i][1], 0, v[i][0]]) code(id);
		
				for(i = [0:len(v)-1])
					if (v[i][1] != -1 && v[i][0] != -1)
						rotate([v[i][1], 0, v[i][0]]) translate([0, 0, edge_length - hole_deep + 1])
							block(hole_width, hole_deep);
			}
		}
	}
}

module block(block_width, length, circular = false)
{
	length = (length == 0) ? width : length;
	translate ([0, 0, length/2-0.1])
		if (circular)
			cylinder(r=block_width/2, h=length, center=true);			
		else
			cube([block_width, block_width, length], center=true);
}

function bevel(type, ref) = (type == "thin") ? ref*0.2 : (type == "medium") ? ref*0.3 : (type == "large") ? ref*0.6 : 0;

function sumv(v,i,s=0) = (i==s ? v[i] : v[i] + sumv(v,i-1,s));

function int2bin(nb, i) = floor( nb/pow(2, i) ) % 2;

function p2i(index) = (index >= len(csv)) ? -1 : strToNumber(str(
		data[csv[index]+1],
		data[csv[index]+2],
		data[csv[index]+3]));

function strToNumber(str) = (
		search(str[2],"0123456789")[0] +
		10 * search(str[1],"0123456789")[0] +
		100 * search(str[0],"0123456789")[0]);

function longStrToNumber(str) = (
		search(str[4],"0123456789")[0] +
		10 * search(str[3],"0123456789")[0] +
		100 * search(str[2],"0123456789")[0] +
		1000 * search(str[1],"0123456789")[0] +
		10000 * search(str[0],"0123456789")[0]);
