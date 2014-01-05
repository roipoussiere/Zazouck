ouack
=====

## Description :
Generate stl files to build a wonderful construction, from an stl file.

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
$ git clone https://github.com/roipoussiere/ouack.git
```

- Make it easy to use :

```shell
$ cd ouack
$ chmod +xX *.py
$ export PATH=$PATH:your_favorite_path/ouack_python/ >> ~/.bashrc
```

##Usage
-> see ./examples to get 3D model examples

- To create a table describing each file, without generate them :

```shell
$ ouack cube.stl -b ./table.csv
$ ouack cube.stl -b # will create cube.csv
```

- To generate a directory containing all the .stl files :

```shell
$ ouack cube.stl # from a 3D model
$ ouack cube.csv -c # from a table
```

Use ouack -h to see all available options.

##Contact :

natha[AT]jourdane[DOT]net
