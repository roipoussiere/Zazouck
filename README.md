Zazouck
=====
## Work in progress
The first release of Zazouck is not yet finished.

Comming soon... please be patient. ;)

## Description
**Z**azouck is an **A**ma<b>Z</b>ing **O**pensource **U**niversal **C**onstruction **K**it

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
- Go where you want to install Zazouck: `$ cd your_favorite_path`

- Install dependencies:

    - **Git** (version control system): To get the sources. You can also download the files manually from the [GitHub page](https://github.com/roipoussiere/Zazouck).
    - **Svn** (version control system): To get the latest version of Jsc3d. You can also download the files manually from the [web page](https://code.google.com/p/jsc3d/).
    - **Openscad** (CAD software): To create the files. v2013.05+ is required to generate images for the documentation.
    - **Imagemagick** (image editor): To process images for the documentation.
	- **Jsc3d** (HTML5 stl viewer): To display stl files on a web page (not yet used)

```
sudo apt-get install git svn openscad imagemagick
svn checkout --non-recursive http://jsc3d.googlecode.com/svn/trunk/jsc3d jsc3d
```

- Get the sources

```
$ git clone https://github.com/roipoussiere/zazouck.git
$ mv jsc3d zazouck
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
usage: zazouck [-h] [-o PROJECT_DIR] [-p PARAM_PATH] [-t] [-i] [-d DIR] [-na]
               [-V [{1,2,3}]] [-j [NB_JOBS_SLOTS]] [-v]
               input_path

                               *** Zazouck ***
This program allows you to build constructions, by generating 3D files
from your model. It works in 2 times: first, it build .csv table files
describing the parts (very fast), then it compile this one into a lot
of .stl files (can be long). See README.md for getting started.

positional arguments:
  input_path            3d model (stl file) or model directory if you want to
                        continue a compilation.

optional arguments:
  -h, --help            show this help message and exit
  -o PROJECT_DIR, --output-dir PROJECT_DIR
                        Directory where all the files will be exported
                        (current dir. by default)
  -p PARAM_PATH, --param-path PARAM_PATH
                        Load a parameters file from PARAM_PATH, containing the
                        parts parameters.
  -t, --test            The files are quickly compiled for testing, not able
                        to be printed.
  -i, --infos           Get some informations about the model.
  -d DIR, --doc-dir DIR
                        Assembly instructions directory (OUTPUT_DIR/doc by
                        default).
  -na, --no-assembled   Do not build the assembled model (save time).
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

If you discover a bug or if you have any suggestion, please report it by [opening an issue](https://github.com/roipoussiere/Zazouck/issues). If you have other comments to make about Zazouck, you can contact me directly:

Nathanaël Jourdane : nathanael at jourdane dot net
