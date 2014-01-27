use <string.scad>;

angles = "090,180,090,225,090,270,000,090";

width = 7.5;
edge_length = 11;  // Set 0 if you want than edge length equals Width.

pos = [0,0,0];

translate(pos)
	part([[d(0),d(1)], [d(2),d(3)], [d(4),d(5)], [d(6),d(7)], [d(8),d(9)], [d(10),d(11)]]);

module part(v)
{
	length = (edge_length < width) ? width : edge_length+width/2;

	translate([0,0,width/2]) {
			sphere(width/2, $fn=8);
			for(i = [0:len(v)-1]) {
				if (v[i][0] != -1)
					rotate([v[i][0], 0, v[i][1]]) translate([0,0,-width/8])
						translate ([0, 0, length/2-0.1]) rotate([0,0,22.5])
							cylinder(r=width/2, h=length, center=true, $fn=8);
		}
	}
}

function d(i) = (strToInt(getsplit(angles, i, ",")) == undef) ? -1 : strToInt(getsplit(angles, i, ","));