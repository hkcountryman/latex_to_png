import argparse
import textwrap

import compileConvert
import fileIO
import guiStuff
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
    # Implement later
    '''parser.add_argument(
        "-ng", "--nogui",
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
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
        help="show program version number"
        )
    parser.add_argument(
        "-vb", "--verbose",
        action="store_true", default=False,
        help="increase output verbosity in the shell"
        )
    parser.add_argument(
        "fileName",
        help="name of the file to create or edit (no extension)"
        )
    args = parser.parse_args()

    # Will we be using --verbose?
    VERBOSE = False
    if args.verbose:
        VERBOSE = True

    # Confirm fileName is valid
    fileName = fileIO.validFileName(args.fileName)
    
    # Is file new or existing?
    if fileIO.fileExists(fileName):
        # Edit existing file
        guiStuff.initWin(fileName, VERBOSE, new=False)
    else:
        # Create new file
        guiStuff.initWin(fileName, VERBOSE, new=True)

if __name__ == "__main__":
    main()