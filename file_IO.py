from pathlib import Path
import re

import compileConvert

def validFileName(fileName):
    """Confirms that a file name is valid.

    Args:
        fileName (str): potential name for .tex file (extension optional).
    Returns:
        a str of alphanumeric/underscore characters (without extension).
    Raises:
        Exception: if the file name is invalid.
    """
    # Must have 1+ alphanumeric/underscore characters; may end in .tex
    nameRegex = re.compile(r"^(\w+)(\.tex)?$")
    mo = nameRegex.search(fileName)

    # Return file name (without .tex extension) or raise exception
    if mo:
        return mo.group(1)
    else:
        raise Exception("Invalid file name. Be sure the extension is .tex.")

def dirExists():
    """Confirm the program directory exists or create it.

    Returns:
        pathlib.PosixPath object (equiv. to str) representing program directory.
    """
    myPath = Path.home()/"Documents"/"texdir"
    if not myPath.exists():
        myPath.mkdir()
    return myPath

def fileExists(fileName):
    """Checks if fileName.tex exists in texdir.

    Args:
        fileName (str): name of file to look for (no extension).
    Returns:
        False: if a file of that name does not exist.
        True: if a file of that name exists.
    """
    fileName = fileName + ".tex"
    ls = compileConvert.texDirContents()
    try:
        ls.index(fileName)
    except ValueError:
        # File does not exist so it's not in ls
        return False
    else:
        # File exists so it appears in ls
        return True

def readFile(filePath):
    """Parse existing file to locate past user input.

    Args:
        fileName (pathlib.PosixPath object): .tex file and its full path.
    Returns:
        str of the text in the file.
    """
    contents = ""
    with open(filePath, "r") as f:
        lines = f.readlines()
        for line in lines:
            contents += line
    return contents
