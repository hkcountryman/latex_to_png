![header](https://github.com/hkcountryman/latex_to_png/blob/assets/header_blue.png)
# ltxpng
This program lets you generate PNGs from LaTeX commands, which are saved as .tex files should you wish to edit your PNG. All created files can be found in a directory called texdir.

## Requirements
You must be running a Debian-based Linux distribution and you must have Python 3.5 or newer.

## First-time setup
The setup_dev.sh script is intended only for developers who want to tweak the code in a virtual environment.

Before using the program, you must run the setup.sh bash script. Navigate to the parent latex_to_png directory that you cloned and type
```
sudo ./setup.sh
```
This installs dependencies via apt, creates a python module containing a directory location of your choice in which to save all created files, creates a symbolic link to the executable in /usr/local/bin, and copies the child latex_to_png directory, which contains the related modules, into /usr/local. Afterwards, it is safe to delete the entire cloned directory if desired. You will now be able to call the program from anywhere. A good place to start would be the help message:
```
ltxpng -h
```
You might want to install some other texlive packages if you want more functionality. To find all the texlive stuff you don't yet have installed, use
```
apt search texlive | grep -v "installed"
```
and install them with
```
sudo apt install [package name here]
```

## Instructions
Once you've followed the setup instructions, you can run ltxpng from the command line. It has some optional flags as well as one positional argument: a file name (alphanumeric characters and underscores, no extension). It can either be a new file or the name of an existing file. Provided you did not use the optional --no-gui flag, a window will pop up where you can type LaTeX commands, entering math mode however you like.

![new_tex](https://github.com/hkcountryman/latex_to_png/blob/assets/new_tex.png)

Before you generate a PNG from your math, decide whether you want a transparent or a white background and select the appropriate radio button at the bottom of the window. Beside that, there are buttons to save the .tex file as well as to save it and generate a PNG from it. If you select the former, a .tex file will be saved in texdir. If you select the latter, the .tex file will be saved along with its PNG. You will also be given the option to save log files and PDF files. If you ever want to delete those extraneous files, there are optional flags to clean them from the directory.

![new_img](https://github.com/hkcountryman/latex_to_png/blob/assets/new_img.png)

If you ever edit your generated .tex files through any means but the program's GUI, it is inadvisable to touch anything but the math you entered yourself. At best, you might cause the PNG to be formatted incorrectly. At worst you could make the file unreadable by the program.

## Limitations
Unfortunately, right now transparent images MUST be black and white because any pixels that are not black will be made transparent. This is because of [anti-aliasing](https://en.wikipedia.org/wiki/Spatial_anti-aliasing) on the PNGs prior to removing the background: in addition to white pixels in the background, pixels that are almost white but a little grey surround the black text. When the white pixels are replaced by transparent pixels, these grey pixels are missed, resulting in an apparent "white" outline around the text that is very visible on dark backgrounds. The easiest way to fix this was to only leave the black pixels intact, but I will experiment with ways to mitigate the harsh outline without restricting available colors.
