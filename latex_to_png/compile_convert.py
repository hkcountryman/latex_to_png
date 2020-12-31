import os
from pathlib import Path
from PIL import Image
import re
import subprocess

import file_IO

def tex_dir_contents():
    """Runs ls in the shell to assemble a list of files in texdir.

    Returns:
        a list of all file names in texdir.
    """
    # Navigate to texdir
    os.chdir(os.path.abspath(file_IO.dir_exists()))

    # Assemble and format ls output in a list
    ls = subprocess.Popen(["ls"], stdout=subprocess.PIPE, universal_newlines=True)
    out = ls.stdout.readlines()
    i = 0
    while i < len(out):
        end = len(out[i]) - 1
        out[i] = out[i][:end]
        i += 1
    return out

def garbage_files(file_name, ls, comp=True):
    """Identifies files to remove.
    Args:
        file_name (str): names of files to clean (no extensions).
        ls (list of str): list of file names (with extensions) to sort.
        comp (bool): which files to look for:
            True: files generated during compilation.
            False: pdf files and their crops.
    Returns:
        a list of all file names to be deleted.
    """
    # Declare a list to hold the garbage
    garbage = []

    if comp:
        # Looking for .aux, .dvi, .fls, and .log files
        name_regex = re.compile(r"^({})(\.)((aux)|(dvi)|(fls)|(log))$".format(file_name))
    else:
        # Looking for file_name.pdf and file_name-crop.pdf
        name_regex = re.compile(r"^({})(-crop)?(\.pdf)$".format(file_name))

    # Collect the garbage
    i = 0
    while i < len(ls):
        mo = name_regex.match(ls[i])
        if mo:
            garbage.append(mo.group())
        i += 1
    return garbage

def clean_up(file_name, verbose=True, comp=True):
    """Cleans directory of certain file types given their name.

    Args:
        file_name (str): names of files to remove (no extensions).
        verbose (bool): determines verbosity.
        comp (bool): which files to delete:
            True: files generated during compilation.
            False: pdf files and their crops.
    """
    # Find out what's garbage
    ls = tex_dir_contents()
    garbage = garbage_files(file_name, ls, comp)

    # Delete it
    for f in garbage:
        subprocess.run(["rm", f])
        if verbose:
            print("Deleting "+f)
    if verbose:
        print()

def generate_PDF(file_name, clean=True, verbose=True):
    """Generates a pdf using pdflatex.

    Args:
        file_name (str): name for the .tex and .pdf files (no extensions).
        clean (bool): whether to remove non-pdf files after compiling:
            True: remove non-pdf files.
            False: keep non-pdf files.
        verbose (bool): determines verbosity.
    Raises:
        FileNotFoundError: if file_name does not correspond to an existing file.
        Exception: if the compilation otherwise fails when running pdflatex.
    """
    # Use pdflatex
    args_list = ["pdflatex", file_name+".tex"]
    try:
        comp = subprocess.run(args_list, stdout=subprocess.PIPE,
            universal_newlines=True)
    except FileNotFoundError:
        print("File could not be found.")
        quit()
    except:
        print(" Compilation failed.")
        quit()
    else:
        if verbose:
            print(comp.stdout)

    # Clean directory
    if clean:
        clean_up(file_name, verbose, comp=True)

def transparent(file_name):
    """Changes white pixels to transparent pixels.

    Args:
        file_name (str): PNG to modify.
    """
    # Navigate to texdir
    os.chdir(os.path.abspath(file_IO.dir_exists()))

    img = Image.open(file_name+".png")
    img = img.convert("RGBA")
    input_data = img.getdata()

    # Change white to transparent--this left grey pixels around black edges
    '''output_data = []
    for datum in input_data:
        if datum[0] == datum[1] == datum[2] == 255:
            output_data.append((255, 255, 255, 0))
        else:
            output_data.append(datum)
    img.putdata(output_data)
    img.save(file_name+".png", "PNG")'''

    # Change non-black to transparent--this will mean only greyscale can be transparent
    output_data = []
    for datum in input_data:
        if not (datum[0] == datum[1] == datum[2] == 0):
            output_data.append((255, 255, 255, 0))
        else:
            output_data.append(datum)
    img.putdata(output_data)
    img.save(file_name+".png", "PNG")
    
def generatePNG(file_name, transparency, clean_logs=True, clean_pdfs=True, verbose=True):
    """Generates a png given a pdf using pdfcrop and pnmtopng.

    Args:
        file_name (str): name for the .pdf and .png files (no extensions).
        transparency (bool): whether to give PNG a transparent background.
            True: transparent background.
            False: white background.
        clean_logs (bool): whether to remove files generated during compilation.
        clean_pdfs (bool): whether to remove pdf files and their crops after compiling.
        verbose (bool): determines verbosity.
    """
    # Navigate to texdir
    os.chdir(os.path.abspath(file_IO.dir_exists()))

    # Compile to pdf
    if clean_logs:
        generate_PDF(file_name, clean=True, verbose=verbose)
    else:
        generate_PDF(file_name, clean=False, verbose=verbose)

    # Crop the pdf
    args_list = ["pdfcrop", file_name+".pdf"]
    if verbose:
        args_list.append("--verbose")
    subprocess.run(args_list)

    # Convert to png
    resolution = "1000"
    args_list = ["pdftoppm", "-png", "-r", resolution, file_name+"-crop.pdf",
        file_name]
    subprocess.run(args_list)
    
    # Change name from file_name-1.png to file_name.png
    args_list = ["mv", file_name+"-1.png", file_name+".png"]
    subprocess.run(args_list)
    if verbose:
        print(file_name+".png created.")
        print()

    # Make transparent
    if transparency:
        transparent(file_name)

    # Clean directory
    if clean_pdfs:
        clean_up(file_name, verbose, comp=False)