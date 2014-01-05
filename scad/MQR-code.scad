// Uncomment this block to see how to use MQR-Code

id = 1234;
width = 6;
size = 4;
height = 1; // Set to 0 if you want to export in 2D DXF.
inter = -0.1; // Don't set to 0 because it could create polygon intersections errors.

// 3D printer :
translate([0, 0,-1]) %cube([width, width, 1]);
mqr_code(id, width, size, height, inter);

// CNC :
// mqr_code(id, width, size, 0, inter);

module mqr_code(code, w, s, h=1, i=-0.1)
{
	for(it = [0:s*s-2])
		if (int2bin(code, it) == 1) translate([floor(it/s)*(w+i)/s, (it%s)*(w+i)/s, 0])
			mqr_square((w+i)/s, h, i);
	
	if (paritybit(code) == 1) translate([(s-1)*(w+i)/s, (s-1)*(w+i)/s, 0])
		mqr_square((w+i)/s, h, i);
}

module mqr_square(w, h, i)
{
	if (h > 0) cube([w-i, w-i, h]);
	else square(w-i, w-i);
}

function paritybit(code, pb=0) = (code==0) ? pb : paritybit(floor(code/2), (code%2+pb)%2);
function int2bin(nb, i) = floor( nb/pow(2, i) ) % 2;
