#!/usr/bin/env python3

import argparse
import os
import subprocess
import textwrap

import compile_convert
import file_IO
import gui_stuff
from _version import __version__

def flags():
    """Creates flags and positional arguments to call.

    Returns:
        argparse.Namespace object.
    """
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
        help="file name to create, edit, or clean (no extension)"
    )
    parser.add_argument(
        "-c", "--clean",
        action="store_true",
        default=False,
        help="clean texdir of PDF, .aux, .dvi, .fls, and .log files of specified name"
    )
    parser.add_argument(
        "-cl", "--clean-logs",
        action="store_true",
        default=False,
        help="clean texdir of .aux, .dvi, .fls, and .log files of specified name"
    )
    parser.add_argument(
        "-cp", "--clean-pdfs",
        action="store_true",
        default=False,
        help="clean texdir of PDF files and their crops of specified name"
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
    return args

def clean_up(args):
    """Tests whether we are calling the program to clean the directory.

    Args:
        args (argparse.Namespace object): where we check flag and argument values.
    Returns:
        True: if the clean-up flags were used.
    """
    # Navigate to texdir
    os.chdir(os.path.abspath(file_IO.dir_exists()))

    # What to delete
    args_list = ["rm", "-f"]
    logs_list = [".aux", ".dvi", ".fls", ".log"]
    pdf_list = [".pdf", "-crop.pdf"]
    if args.clean or args.clean_logs:
        for extension in logs_list:
            args_list.append(args.file_name+extension)
    if args.clean or args.clean_pdfs:
        for extension in pdf_list:
            args_list.append(args.file_name+extension)

    # Delete unwanted files
    if args.clean or args.clean_logs or args.clean_pdfs:
        subprocess.run(args_list, stdout=subprocess.PIPE)
        return True
    return False

def open_win(args):
    """Launches a window to edit a new or existing file.

    Args:
        args (argparse.Namespace object): where we check flag and argument values.
    """
    # Is file new or existing?
    if file_IO.file_exists(args.file_name):
        # Edit existing file
        gui_stuff.init_win(args.file_name, args.verbose, new=False)
    else:
        # Create new file
        gui_stuff.init_win(args.file_name, args.verbose, new=True)

def main():
    # Create flags
    args = flags()

    # Confirm file_name is valid
    file_IO.valid_file_name(args.file_name)

    # Clean up?
    if clean_up(args):
        return
    
    # Create window
    open_win(args)

if __name__ == "__main__":
    main()