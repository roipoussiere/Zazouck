Zazouck
=====

## Description
**Z**azouck is an A**ma__Z__ing **O**pensource **U**niversal **C**onstruction **K**it

This program generates stl files to build a wonderful construction, from a 3D model. Here is an example of a generated part :

![A generated part](https://raw2.github.com/roipoussiere/Zazouck/master/pictures/generated_part.png "A generated part")

### The 3d printable parts
The generated files are 3d printable connectors to connect wood, platic or metal rods together.

If you want to create corners with specific angles, you can also use Zazouck manually, without the generator : just use [the Openscad file](scad/corner.scad) or simply go on the [Thingiverse page](http://www.thingiverse.com/thing:179597).

![Zazouck](https://raw2.github.com/roipoussiere/Zazouck/master/pictures/Zazouck_wide.png "Zazouck")

### The generator
The program works in 2 steps:
- First, it creates a table file (.csv) which containing the connectors parameters.
- Then, it creates stl files of the connectors, from the table.

##Installation instuctions

### On Linux platforms
- Install dependencies:

    - **git** : You need it to get sources, but you can also download them manually on the GiHub page.
    - **openscad** : The CAD software used to create the files. v2013.05+ is required to generate documentation.
    - **imagemagick** : An image editor, only used to generate the documentation.

```
sudo apt-get install git openscad imagemagick
```

- Get the sources

```
$ cd your_favorite_path
$ git clone https://github.com/roipoussiere/zazouck.git
```

- Make it easy to use

```
$ chmod +xX zazouck/python/*.py
$ echo export PATH=$PATH:your_favorite_path/zazouck/python/ >> ~/.bashrc
```

### On Windows and MacOS platforms

Comming soon...

You can try to build from the sources, but it has never tested on these platforms yet.

##Usage
See [examples folder](examples/) to get 3D model examples

- To create a table describing each file, without generate them

```
$ zazouck cube.stl -b ./table.csv # will create file 'table.csv'
$ zazouck cube.stl -b # will create file 'cube.csv'
```

- To generate a directory containing all the .stl files

```
$ zazouck cube.stl # from a 3D model
$ zazouck cube.csv # from a table
```

- To generate a nice documentation:

```
$ zazoucko cube.stl -d
```
##Options
Use zazoucko -h to see all available options :

```
usage: zazouck [-h] [-o OUTPUT_DIR] [-p PARAM_PATH] [-t] [-s FIRST_LINE]
               [-f LAST_LINE] [-d DIR] [-ns] [-nd] [-ni] [-na] [-nf]
               [-V [{1,2,3}]] [-j [NB_JOBS_SLOTS]] [-v]
               input_path

                               *** Zazouck ***
This program allows you to build constructions, by generating 3D files
from your model. It works in 2 times: first, it build .csv table files
describing the parts (very fast), then it compile this one into a lot
of .stl files (can be long). See README.md for getting started.

positional arguments:
  input_path            3d model (stl file) or model directory if it's already
                        created.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory where all the files will be exported
                        (current dir. by default)
  -p PARAM_PATH, --param-path PARAM_PATH
                        Load a parameters file from PARAM_PATH, containing the
                        parts parameters.
  -t, --test            The files are quickly compiled for testing, not able
                        to be printed.
  -s FIRST_LINE, --start-from FIRST_LINE
                        Start compilation from line FIRST_LINE in the .csv
                        file.
  -f LAST_LINE, --finish-at LAST_LINE
                        Finish compilation at line LAST_LINE in the .csv file.
  -d DIR, --doc-dir DIR
                        Assembly instructions directory (OUTPUT_DIR/doc by
                        default).
  -ns, --no-stl         Doesn't compile stl files, only build csv tables.
  -nd, --no-doc         Doesn't build assembly instructions.
  -ni, --no-infos       Doesn't make a text file containing informations about
                        the model.
  -na, --no-assembly    Doesn't create the 3d model of the assembly.
  -nf, --no-shuffle     Doesn't shuffle the lists of corners, polygons and
                        edges.
  -V [{1,2,3}], --verbose [{1,2,3}]
                        Verbose level: 1 = OpenScad calls (default value), 2 =
                        OpenScad warnings, 3 = all OpenScad messages.
  -j [NB_JOBS_SLOTS], --jobs [NB_JOBS_SLOTS]
                        Compile NB_JOBS_SLOTS files simultaneously (the number
                        of cores on your computer by default).
  -v, --version         Show program version and exit.

Author: Nathanaël Jourdane - nathanael@jourdane.net
Zazouck is licensed under GNU GPLv3: www.gnu.org/licenses/gpl-3.0.html
```

##Contact

If you discover a bug or if you have any suggestion, please report it by [opening an issue](https://github.com/roipoussiere/Zazouck/issues).

If you have other comments to make about Zazouck, you can contact me directly:

Nathanaël Jourdane : nathanael at jourdane dot net

This project is licenced under [GNU GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).
