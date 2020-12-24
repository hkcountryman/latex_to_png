from tkinter import *
from tkinter import ttk
import tkinter.simpledialog

import compile_convert
import fileIO

class text_scroll_combo(ttk.Frame):
    """A ttk.Frame with a scroll bar.

    Attributes:
        txt (tkinter.Text object): text box to hold user input.
        scrollb (ttk.Scrollbar object): scroll bar within text box.
    """
    def __init__(self, *args, **kwargs):
        """Create the ttk.Frame with text box and scroll bar."""
        super().__init__(*args, **kwargs)
    
        # Consistent GUI size and stretchability
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create Text widget
        self.txt = Text(self)
        self.txt.pack()
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.txt.focus_set()

        # Create Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky="nsew")
        self.txt["yscrollcommand"] = scrollb.set

class PNG_dialog(tkinter.simpledialog.Dialog):
    """A dialog box for generating PNGs.
    
    Attributes:
        f (str): name of the file being edited.
        VERBOSE (bool): determines verbosity.
        clean_logs (bool): whether to clean log files generated during compilation:
            True: delete log files.
            False: keep log files.
        clean_PDFs (bool): whether to clean PDF files and their crops:
            True: delete PDFs and their crops.
            False: keep PDFs and their crops.
    """
    # Initialize static variables to default values; may change later
    f = ""
    VERBOSE = False
    clean_logs = True
    clean_PDFs = True

    def __init__(self, *args, **kwargs):
        """Instantiates with same arguments the superclass constructor accepts."""
        super().__init__(*args, **kwargs)

    def body(self, win):
        """Adds checkbuttons to the dialog to indicate if texdir should be cleaned.
        
        Args:
            win (tkinter.Tk object): the window from which the dialog originates.
        """
        # Whether to keep log files
        self.logs = Checkbutton(win, text="Keep log files", command=lambda:clean(logs=True))
        self.logs.grid(row=1, columnspan=2, sticky=W)

        # Whether to keep PDF files
        self.PDFs = Checkbutton(win, text="Keep PDF files", command=lambda:clean(logs=False))
        self.PDFs.grid(row=2, columnspan=2, sticky=W)

    def apply(self):
        """Saves and generates a PNG when OK is pressed."""
        compile_convert.generatePNG(self.f, self.clean_logs, self.clean_PDFs, self.VERBOSE)

def clean(logs=True):
    """Setter method for PNG_dialog.clean_logs, .clean_PDFs.
    Args:
        logs (bool): which to set:
            True: clean_logs.
            False: clean_PDFs.
    """
    if logs:
        PNG_dialog.clean_logs = False
    else:
        PNG_dialog.clean_PDFs = False

def save(txt_obj, file_name, verbose, new=True):
    """Save the contents of the text box.

    Args:
        txt_obj (tkinter.Text object): the text box in question.
        file_name (str): the name to save it under (no extension).
        verbose (bool): determines verbosity.
        new (bool): whether file_name.tex is new or existing:
            True: file is new.
            False: file exists and is being edited.
    """
    # Gather the text
    text = txt_obj.get("1.0", "end-1c")

    # Make the file
    if new:
        file_name = file_name + ".tex"
    my_path = fileIO.dirExists()/file_name
    my_file = open(my_path, "w")
    my_file.write(text)
    my_file.close()

    if verbose == True:
        print(file_name+".tex saved.")

def makePNG(win, txt_obj, file_name, verbose, new=True):
    """Save the contents of the text box and generate a PNG.

    Args:
        win (tkinter.Tk object): the window that spawns a dialog.
        txt_obj (tkinter.Text object): the text box in question.
        file_name (str): the name to save it under (no extension).
        verbose (bool): determines verbosity.
        new (bool): whether file_name.tex is new or existing:
            True: file is new.
            False: file exists and is being edited.
    """
    PNG_dialog.f = file_name
    PNG_dialog.VERBOSE = verbose
    save(txt_obj, file_name, new)
    d = PNG_dialog(win, title="Create a PNG")

def init_win(file_name, verbose, new=True):
    """Create a window to edit a file.

    Args:
        file_name (str): the name of the file (no extension).
        verbose (bool): determines verbosity.
        new (bool): whether this file is new or existing:
            True: file is new.
            False: file exists and is being edited.
    """
    # Make a window
    win = Tk()
    win.title("LaTeX Thing!")

    # Add scrolling text box
    combo = text_scroll_combo(win)
    combo.pack(fill="both", expand=True)
    combo.config(width=600, height=600)
    combo.txt.config(font=("consolas", 12), undo=True, wrap='word')
    combo.txt.config(borderwidth=3, relief="sunken")
    
    # Style options
    style = ttk.Style()
    style.theme_use("clam")

    # Is the file existing?
    if not new:
        with_extension = file_name + ".tex"
        my_path = fileIO.dirExists()/with_extension
        combo.txt.insert(INSERT, fileIO.readFile(my_path))

    # Buttons panel
    buttons = ttk.Frame(win)
    buttons.pack(side=BOTTOM, pady=25)
    # Save button
    s = ttk.Button(win, text="Save",
        command=lambda:save(combo.txt, file_name, verbose, new))
    s.pack(in_=buttons, side=LEFT, padx=10)
    # Generate PNG button
    p = ttk.Button(win, text="Save and generate PNG",
        command=lambda:makePNG(win, combo.txt, file_name, verbose, new))
    p.pack(in_=buttons, side=RIGHT, padx=10)

    # Make it all appear
    win.mainloop()
