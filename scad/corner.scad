use <string.scad>;
use <MQR-code.scad>;

data = "12345,000,000,090,000,090,090";

edge_shape = "rectangular"; // [rectangular, circular, sphere]
edge_hole_shape = "rectangular"; // [rectangular, circular, none]
main_hole_shape = "none"; // [rectangular, circular, none]

width = 7.5;
edge_length = 11;  // Set 0 if you want than edge length equals Width.
notch_size = 1.5;
microhole_width = 2;
microhole_position = 4.5;

hole_width = 4.5; // edges hole width size.
hole_deep = 8.5; // Set 0 if you want than edge length equals Width.
main_hole_slack = 0.2; // Difference between the main hole size and the edges hole size.

edge_bevel = "none"; // [none, thin, medium, large, sphere]
external_bevel = "sphere"; // [none, sphere]
holes_bevel = "none"; // [none, thin, medium, large]

csv = search(",", data, 20)[0];
v = [p2i(0), p2i(1), p2i(2), p2i(3), p2i(4), p2i(5), p2i(6), p2i(7), p2i(8), p2i(9), p2i(10), p2i(11)];

part([[v[0],v[1]], [v[2],v[3]], [v[4],v[5]], [v[6],v[7]], [v[8],v[9]], [v[10],v[11]]]);

echo([[v[0],v[1]], [v[2],v[3]], [v[4],v[5]], [v[6],v[7]], [v[8],v[9]], [v[10],v[11]]]);
//echo(d(1), d(2), d(3), d(4), d(5), d(6), d(7), d(8), d(9), d(10), d(11), d(12), d(13));
// ajouter getnbargs() dans string.scad puis modifier part() pour générer directement à partir de data.

module part(v)
{
	$fn = 50;
	edge_length = (edge_length < width) ? width : edge_length;
	hole_width = (hole_width >= width) ? width-1 : hole_width;
	main_hole_width = hole_width + main_hole_slack;
	hole_deep = (hole_deep <=0) ? edge_length : hole_deep;

	translate([0,0,width/2]) intersection() {
		if (external_bevel == "sphere") 
			sphere(edge_length);

		difference() {
			if (edge_shape == "sphere") {
				sphere(edge_length);
			} else {
				union() {
					sphere(width/2);
					for(i = [0:len(v)-1]) {
						if (v[i][0] != -1)
							rotate([v[i][0], 0, v[i][1]])
							translate([0,0,-width/8]) intersection() {
								cylinder(r1=width/2-width/64, r2=width, h=edge_length+width/8);
								block(width, edge_length+width/2, edge_shape, bevel = "ext");
						}
					}

				}
			}
	
			for(i = [0:len(v)-1]) {
					if (v[i][0] != -1)
						rotate([v[i][0], 0, v[i][1]]) {
							translate([0, 0, edge_length - hole_deep + 0.1])
								block(hole_width, hole_deep, edge_hole_shape, bevel = "int");
							translate([hole_width/4, -notch_size/2, edge_length-notch_size*0.6])
								cube([width/2, notch_size, notch_size]);
							translate([0, 0.5, edge_length-hole_deep+microhole_position+1]) rotate([90,0,0]) translate([0, 0, -width/2])
								cylinder(r=microhole_width/2, h=width+1);
						}
			}

			block(main_hole_width, width+1, main_hole_shape);
		}
	}
	
	translate([0,0,width/2])
		for(i = [0:len(v)-1])
			if (v[i][0] != -1)
				rotate([v[i][0], 0, v[i][1]])
				translate([-hole_width/2, -hole_width/2, edge_length-hole_deep-0.1])
					mqr_code(d(0), hole_width, 4);
}

module block(block_width, length, shape, bevel)
{
	ext_bevel = bevel(edge_bevel, block_width)/2;
	int_bevel = bevel(holes_bevel, hole_width)*1.5;

	length = (length == 0) ? width : length;

	translate ([0, 0, length/2-0.1]) /*intersection()*/ {
		union() {
			if (shape=="rectangular")
				cube([block_width, block_width, length], center=true);
			else if (shape=="circular")
				cylinder(r=block_width/2, h=length, center=true);
			else if (shape=="hexagonal")
				rotate([0,0,22.5]) cylinder(r=block_width/2, h=length, center=true, $fn=8);
	
			if (bevel == "int")
				translate([0, 0, length/2 - block_width/2]) rotate([0,0,45])
					cylinder(r1=0, r2 = (edge_hole_shape == "rectangular") ? block_width*0.707 + int_bevel : block_width/2 + int_bevel, h=block_width/2, $fn = (edge_hole_shape == "rectangular") ? 4 : $fn);
		}
		
		/*union() {
			if (bevel == "ext") {
				translate([0, 0, length*1.5 - block_width*0.28 - ext_bevel]) rotate([180,0,45])
					cylinder(r1=0, r2 = block_width+0.1, h=block_width+0.1, $fn = (edge_hole_shape == "rectangular") ? 4 : $fn);
				translate([0, 0, -length/2]) cube([block_width+0.1, block_width+0.1, length*1.5+0.1], center=true);
			}
		}*/
	}
}

function bevel(type, ref) = (type == "thin") ? ref*0.2 : (type == "medium") ? ref*0.3 : (type == "large") ? ref*0.6 : 0;

function d(i) = strToInt(getsplit(data, i, ",")); // just to save space

function sumv(v,i,s=0) = (i==s ? v[i] : v[i] + sumv(v,i-1,s));

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