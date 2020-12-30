from pathlib import Path
import re

import compile_convert

# Formatting string constants
class_style = ("\\documentclass{article}\n" + "\\thispagestyle{empty}\n" +
    "% Import packages:\n")
begin_doc = "\n\\begin{document}\n" + "% Enter math mode as desired:\n"
end_doc = "\n\\end{document}"

def valid_file_name(file_name):
    """Confirms that a file name is valid.

    Args:
        file_name (str): potential name for .tex file (extension optional).
    Returns:
        a str of alphanumeric/underscore characters (without extension).
    Raises:
        Exception: if the file name is invalid.
    """
    # Must have 1+ alphanumeric/underscore characters; may end in .tex
    name_regex = re.compile(r"^(\w+)(\.tex)?$")
    mo = name_regex.search(file_name)

    # Return file name (without .tex extension) or raise exception
    if mo:
        return mo.group(1)
    else:
        raise Exception("Invalid file name. Be sure the extension is .tex.")

def dir_exists():
    """Confirm the program directory exists or create it.

    Returns:
        pathlib.PosixPath object (equiv. to str) representing program directory.
    """
    my_path = Path.home()/"Documents"/"texdir"
    if not my_path.exists():
        my_path.mkdir()
    return my_path

def file_exists(file_name):
    """Checks if file_name.tex exists in texdir.

    Args:
        file_name (str): name of file to look for (no extension).
    Returns:
        False: if a file of that name does not exist.
        True: if a file of that name exists.
    """
    file_name = file_name + ".tex"
    ls = compile_convert.tex_dir_contents()
    try:
        ls.index(file_name)
    except ValueError:
        # File does not exist so it's not in ls
        return False
    else:
        # File exists so it appears in ls
        return True

def read_file(file_path, packages=True):
    """Parse existing file to locate past user input.

    Args:
        file_path (pathlib.PosixPath object): .tex file and its full path.
        packages (bool): what part of the file we're reading:
            True: reading packages
            False: reading math
    Returns:
        str of the text in the file.
    """
    if packages:
        start = "% Import packages:\n"
        end = "\\begin{document}\n"
    else:
        start = "\\begin{document}\n"
        end = "\\end{document}"
    contents = ""
    with open(file_path, "r") as f:
        lines = f.readlines()
        begin_idx = lines.index(start) + 1
        end_idx = lines.index(end)
        for line in lines[begin_idx:end_idx]:
            contents += line
    return contents