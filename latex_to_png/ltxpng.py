#!/usr/bin/env python3

import argparse
import os
import subprocess
import textwrap

import compile_convert
import file_IO
import gui_stuff
from _version import __version__

def main():
    # Create flags
    parser = argparse.ArgumentParser(
        prog="LaTeX PNG Creator Beta",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            A WIP tool to convert LaTeX equations to PNGs.
            While the setup script contains the bare minimum for basic functionality,
            if you want to do more with LaTeX you may need to install other packages.
            You might want to check out the TeX Users Group (tug.org). For a list of
            new packages to install to extend the functionality of this tool, try
                apt search texlive | grep -v "installed"
            """))
    parser.add_argument(
        "file_name",
        help="name of the file to create or edit (.tex or no extension)"
    )
    parser.add_argument(
        "-c", "--clean",
        action="store_true",
        default=False,
        help="clean texdir of PDF, .aux, .dvi, .fls, and .log files"
    )
    parser.add_argument(
        "-cl", "--clean-logs",
        action="store_true",
        default=False,
        help="clean texdir of .aux, .dvi, .fls, and .log files"
    )
    parser.add_argument(
        "-cp", "--clean-pdfs",
        action="store_true",
        default=False,
        help="clean texdir of PDF files and their crops"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
        help="show program version number"
    )
    parser.add_argument(
        "-vb", "--verbose",
        action="store_true",
        default=False,
        help="increase output verbosity in the shell"
    )
    # Implement later
    '''parser.add_argument(
        "-ng", "--no-gui",
        action="store_true", default=False,
        help="use the program without launching the GUI text editor"
        )
    parser.add_argument(
        "-l", "--logs",
        action="store_true", default=False,
        help="keep non-pdf/png files created during compilation"
        )
    parser.add_argument(
        "-p", "--pdfs",
        action="store_true", default=False,
        help="keep pdf files created by compilation"
        )'''
    args = parser.parse_args()

    # Will we be using --verbose?
    VERBOSE = False
    if args.verbose:
        VERBOSE = True

    # Confirm file_name is valid
    file_name = file_IO.valid_file_name(args.file_name)

    # Clean up?
    # Navigate to texdir
    os.chdir(os.path.abspath(file_IO.dir_exists()))
    # What to delete
    args_list = ["rm", "-f"]
    logs_list = [".aux", ".dvi", ".fls", ".log"]
    pdf_list = [".pdf", "-crop.pdf"]
    if args.clean or args.clean_logs:
        for extension in logs_list:
            args_list.append(file_name+extension)
    if args.clean or args.clean_pdfs:
        for extension in pdf_list:
            args_list.append(file_name+extension)
    # Delete unwanted files
    if args.clean or args.clean_logs or args.clean_pdfs:
        subprocess.run(args_list, stdout=subprocess.PIPE)
        return
    
    # Is file new or existing?
    if file_IO.file_exists(file_name):
        # Edit existing file
        gui_stuff.init_win(file_name, VERBOSE, new=False)
    else:
        # Create new file
        gui_stuff.init_win(file_name, VERBOSE, new=True)

if __name__ == "__main__":
    main()