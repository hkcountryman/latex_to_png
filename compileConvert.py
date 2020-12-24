import os
from pathlib import Path
import re
from shutil import copyfile
import subprocess

import fileIO

def texDirContents():
    """Runs ls in the shell to assemble a list of files in texDir.

    Returns:
        a list of all file names in texDir.
    """
    # Navigate to texDir
    os.chdir(os.path.abspath(fileIO.dirExists()))

    # Assemble and format ls output in a list
    ls = subprocess.Popen(["ls"], stdout=subprocess.PIPE, universal_newlines=True)
    out = ls.stdout.readlines()
    i = 0
    while i < len(out):
        end = len(out[i]) - 1
        out[i] = out[i][:end]
        i += 1
    return out

def garbageFiles(fileName, ls, comp=True):
    """Identifies files to remove.
    Args:
        fileName (str): names of files to clean (no extensions).
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
        nameRegex = re.compile(r"^({})(\.)((aux)|(dvi)|(fls)|(log))$".format(fileName))
    else:
        # Looking for fileName.pdf and fileName-crop.pdf
        nameRegex = re.compile(r"^({})(-crop)?(\.pdf)$".format(fileName))

    # Collect the garbage
    i = 0
    while i < len(ls):
        mo = nameRegex.match(ls[i])
        if mo:
            garbage.append(mo.group())
        i += 1
    return garbage

def cleanUp(fileName, verbose=True, comp=True):
    """Cleans directory of certain file types given their name.

    Args:
        fileName (str): names of files to remove (no extensions).
        verbose (bool): determines verbosity.
        comp (bool): which files to delete:
            True: files generated during compilation.
            False: pdf files and their crops.
    """
    # Find out what's garbage
    ls = texDirContents()
    garbage = garbageFiles(fileName, ls, comp)

    # Delete it
    for f in garbage:
        rm = subprocess.run(["rm", f])
        if verbose:
            print("Deleting "+f)
    if verbose:
        print()

def generatePDF(fileName, clean=True, verbose=True):
    """Generates a pdf using pdflatex.

    Args:
        fileName (str): name for the .tex and .pdf files (no extensions).
        clean (bool): whether to remove non-pdf files after compiling:
            True: remove non-pdf files.
            False: keep non-pdf files.
        verbose (bool): determines verbosity.
    Raises:
        FileNotFoundError: if fileName does not correspond to an existing file.
        Exception: if the compilation otherwise fails when running pdflatex.
    """
    # Navigate to texDir
    os.chdir(os.path.abspath(fileIO.dirExists()))

    # Use pdflatex
    argsList = ["pdflatex", fileName+".tex"]
    try:
        comp = subprocess.run(argsList, stdout=subprocess.PIPE,
            universal_newlines=True)
    except FileNotFoundError:
        print("File could not be found.")
        quit()
    except:
        print("Compilation failed.")
        quit()
    else:
        if verbose:
            print(comp.stdout)

    # Clean directory
    if clean:
        cleanUp(fileName, verbose, comp=True)

def generatePNG(fileName, cleanLogs=True, cleanPDFs=True, verbose=True):
    """Generates a png given a pdf using pdfcrop and pnmtopng.

    Args:
        fileName (str): name for the .pdf and .png files (no extensions).
        clean (bool): whether to remove pdf files and their crops after compiling:
            True: remove pdf files and their crops.
            False: keep pdf files and their crops.
        verbose (bool): determines verbosity.
    """
    # Compile to pdf
    if cleanLogs:
        generatePDF(fileName, clean=True, verbose=verbose)
    else:
        generatePDF(fileName, clean=False, verbose=verbose)

    # Crop the pdf
    argsList = ["pdfcrop", fileName+".pdf"]
    if verbose:
        argsList.append("--verbose")
    crop = subprocess.run(argsList)
    
    # Convert to png
    argsList = ["pdftoppm", "-png", fileName+"-crop.pdf", fileName]
    img = subprocess.run(argsList)
    
    # Change name from fileName-1.png to fileName.png
    argsList = ["mv", fileName+"-1.png", fileName+".png"]
    rename = subprocess.run(argsList)
    if verbose:
        print(fileName+".png created.")
        print()

    # Clean directory
    if cleanPDFs:
        cleanUp(fileName, verbose, comp=False)