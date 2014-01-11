Zazoucko
=====

## Description :
ZAZOUCK generatOr - Zazouck is an AmaZing Opensource Construction Kit

This program generates stl files to build a wonderful construction, from a 3D model.

This project is licenced under GNU GPLv3 : see COPYING.txt for details.

##Installation instuctions :

### On Linux platforms :
- Install dependencies :

```shell
$ sudo apt-get install git openscad
```

- Get the sources :

```shell
$ cd your_favorite_path
$ git clone https://github.com/roipoussiere/zazoucko.git
```

- Make it easy to use :

```shell
$ cd zazoucko
$ chmod +xX *.py
$ export PATH=$PATH:your_favorite_path/zazoucko_python/ >> ~/.bashrc
```

##Usage
-> see ./examples to get 3D model examples

- To create a table describing each file, without generate them :

```shell
$ zazoucko cube.stl -b ./table.csv
$ zazoucko cube.stl -b # will create cube.csv
```

- To generate a directory containing all the .stl files :

```shell
$ zazoucko cube.stl # from a 3D model
$ zazoucko cube.csv -c # from a table
```

Use zazoucko -h to see all available options.

##Contact :

natha[AT]jourdane[DOT]net
