file = "stl/00000.stl";

tx=0;
ty=0;
tz=0;

rx=0;
ry=0;
rz=0;

translate([tx,ty,tz]) rotate([rx,ry,rz]) import(file);