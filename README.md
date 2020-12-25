# LaTeX PNG Creator Beta
This program lets you generate PNGs from LaTeX commands, which are saved as .tex files should you wish to edit your PNG. All created files can be found in ~/Documents/texdir.

Right now the program is functional but shitty. You have been warned.

## Setup
Use the setup.sh bash script to install dependencies (the ./setup_dev.sh script is intended only for developers who want to tweak the code in a virtual environment). Navigate to your local latex_to_png directory and use
```
sudo ./setup.sh
```
If you prefer, everything can also be installed manually, in which case you'll want the following packages:
  - python3-tk
  - poppler-utils
  - texlive-latex-base
  - texlive-latex-extra
  - texlive-extra-utils
  
All can be installed using apt:
```
sudo apt install [package name here]
```
You might want to install some other texlive packages if you want more functionality. To find all the texlive stuff you don't yet have installed, use
```
apt search texlive | grep -v "installed"
```
Now you can run the program.

## Instructions
Once you've followed the setup instructions, you can run it from the command line. It has optional flags -h/--help, -v/--version, and -vb/--verbose. If you use --verbose or no flags, you will need to provide a file name (alphanumeric characters and underscores, with either .tex or no extension). It can either be a new file or the name of an existing file you wish to edit. A window will pop up where you can type your code. For the time being, it is recommended you use this format to ensure that the image contains only what you typed:
```
\documentclass{article}
\thispagestyle{empty}

% any packages you like, with \usepackage{[insert package name]}

\begin{document}

% start a math environment--anything from inline $x=4$ to the equation* environment from amsmath
% or just type outside of math mode for beautiful LaTeX formatting
% just don't forget your packages!

\end{document}
```
There are buttons to save the .tex file and to save it and generate a PNG from it. If you select the latter, you will be given the option to keep log files and PDF files. I don't recommend you check those boxes, since it tends to clutter up your directory, but you do you.

## Plans for the future
In the next release, my hope is to add the following:
  - Prompt to save when closing the text editor
  - Dialog on opening informing the user they can now enter math mode however they prefer
  - PNGs will have transparent backgrounds
  - The program will force all that aforementioned formatting stuff so you don't have to remember how to begin a LaTeX document, etc.
  - Add some way to clean up the texdir directory of specific file types
  
At some point I hope to make everything work without leaving the terminal window, but we'll see.
