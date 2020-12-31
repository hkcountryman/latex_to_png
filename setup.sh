#!/bin/bash

# Confirm Python is 3.6+
python_ver_check() {
	echo checking for the correct version of Python . . .
	if ! python3 --version 2>&1 | grep -E "^(Python 3\.)(([6-9])|([1-9])([0-9]))"
	then	
		echo Make sure you are using Python version 3.6+	
		exit
	fi
}
python_ver_check

# Install requisite packages
PACKAGES=(
	python3-tk	# tkinter
	poppler-utils	# pdf -> png
	texlive-latex-base	# latex things...
	texlive-latex-extra
	texlive-extra-utils
)
for item in ${PACKAGES[*]}
do
	apt install $item -y
done

# Ask for directory location
echo Where would you like to install the directory that will contain the files you produce with this program?
# Check if it's a directory
filepath=
while true ; do
	read -r -p "Path: " filepath
	if [ -d "$filepath" ] ; then
		break
	fi
	echo "$filepath is not a directory."
done
# Save location for texdir inside child latex_to_png directory
echo -n "texdir = \"$filepath/texdir\"" > ./latex_to_png/file_path.py
echo "After you first run ltxpng, you will be able to find the directory at $filepath/texdir."

# Create symbolic link to run program
cp -r latex_to_png /usr/local
cd /usr/local/bin
ln -s ../latex_to_png/ltxpng.py ltxpng