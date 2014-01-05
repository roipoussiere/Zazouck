data = "00000,00000,00000"; // id tige, id left connector, id right connector
// max id = 16383 : 14 bits de data et 2 bits de parité

thickness = 3.5;
hole_width = 1;
length = 100;

csv = search(",", data, 20)[0];
id = longStrToNumber(str(data[0], data[1], data[2], data[3], data[4]));
v = [p2i(0), p2i(1), p2i(2), p2i(3), p2i(4), p2i(5), p2i(6), p2i(7), p2i(8), p2i(9), p2i(10), p2i(11)];

//part([[v[0],v[1]], [v[2],v[3]], [v[4],v[5]], [v[6],v[7]], [v[8],v[9]], [v[10],v[11]]]);

square([length, thickness]);


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

//str = "1234";
//echo(len(str));
function strToNbr(str, i=0, nb) = (i == len(str)) ? nb : strToNbr(str, i+1, search(str[i],"0123456789")[0]);

function longStrToNumber(str) = (
		search(str[4],"0123456789")[0] +
		10 * search(str[3],"0123456789")[0] +
		100 * search(str[2],"0123456789")[0] +
		1000 * search(str[1],"0123456789")[0] +
		10000 * search(str[0],"0123456789")[0]);
